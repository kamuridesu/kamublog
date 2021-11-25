output "IP_Addr" {
  value = aws_instance.site_deploy.public_ip
}

output "DNS_Addr" {
  value = aws_instance.site_deploy.public_dns
}

output "static_ip" {
  value = aws_eip.static_ip.address
}

output "static_public_ip" {
  value = aws_eip.static_ip.public_ip
}

output "static_public_dns" {
  value = aws_eip.static_ip.public_dns
}

output "static_domain" {
  value = aws_eip.static_ip.domain
}