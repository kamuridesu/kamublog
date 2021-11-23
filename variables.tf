variable "username" {
    type = string
}

variable "ssh_pub_key" {
    type = string
}

variable "ssh_priv_key" {
    type = string
}

variable "connection_ports" {
  type = list
  default = [5000, 22, 80]
}