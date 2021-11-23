output "IP_Addr" {
    value = aws_instance.site_deploy.public_ip
}

output "DNS_Addr" {
    value = aws_instance.site_deploy.public_dns
}