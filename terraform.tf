terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.66.0"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_key_pair" "ssh_key" {
  key_name   = "ssh_key"
  public_key = file(var.ssh_pub_key)
}

resource "aws_security_group" "ec2_security_ports" {
  name = "ec2_security_ports"

  dynamic "ingress" {
    for_each = var.connection_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "ec2_security_ports" }
}

resource "aws_instance" "site_deploy" {
  ami             = "ami-07d02ee1eeb0c996c"
  key_name        = aws_key_pair.ssh_key.key_name
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.ec2_security_ports.name]

  tags = {
    Name = "Site"
  }

  provisioner "file" {
    source = "./blog/config.auth.json"
    destination = "/home/${var.username}/config.auth.json"
    on_failure = fail
    connection {
      type        = "ssh"
      user        = var.username
      private_key = file(var.ssh_priv_key)
      host        = self.public_ip
    }
  }

  provisioner "file" {
    source = "./js-bot/config.admin.js.json"
    destination = "/home/${var.username}/config.admin.js.json"
    on_failure = fail
    connection {
      type        = "ssh"
      user        = var.username
      private_key = file(var.ssh_priv_key)
      host        = self.public_ip
    }
  }
  
  provisioner "file" {
    source = "./js-bot/config.auth.js.json"
    destination = "/home/${var.username}/config.auth.js.json"
    on_failure = fail
    connection {
      type        = "ssh"
      user        = var.username
      private_key = file(var.ssh_priv_key)
      host        = self.public_ip
    }
  }

  provisioner "remote-exec" {
    inline = ["sudo apt update",
      "sudo apt install git ffmpeg webp ca-certificates curl gnupg lsb-release apt-transport-https -y",
      "curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg",
      "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
      "sudo apt-get update",
      "sudo apt-get install docker-ce docker-ce-cli containerd.io -y",
      "git clone https://github.com/kamuridesu/kamublog.git && cd kamublog/blog",
      "cp /home/${var.username}/config.auth.json .",
      "sudo docker build -t site .",
      "sudo docker run -d --name site -p 80:8080 site",
      "cd ../.. && git clone https://github.com/kamuridesu/js-bot.git",
      "cd js-bot",
      "cp /home/${var.username}/config.auth.js.json ./config.auth.json",
      "cp /home/${var.username}/config.admin.js.json ./config.admin.json",
      "sudo docker build -t bot .",
      "sudo docker run -d --name bot -p 5000:5000 bot"
    ]
    on_failure = fail

    connection {
      type        = "ssh"
      user        = var.username
      private_key = file(var.ssh_priv_key)
      host        = self.public_ip
    }
  }

}

resource "aws_default_vpc" "default" {
  enable_dns_hostnames = true
  tags = {
    Name = "Default VPC"
  }
}


resource "aws_eip" "static_ip" {
  instance = aws_instance.site_deploy.id
  vpc = true
}
