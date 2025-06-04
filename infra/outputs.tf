output "public_ip" {
  value = aws_instance.app_server.public_ip
}

output "debug_key_name" {
  value = var.key_name
}
