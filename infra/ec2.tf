
resource "aws_security_group" "ssh_access" {
  name        = "allow_ssh"
  description = "Allow SSH access"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # For dev only!
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "web_access" {
  name        = "allow_web_access"
  description = "Allow web access"
  vpc_id      = aws_vpc.main.id


  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  subnet_id     = aws_subnet.public_subnet.id
  vpc_security_group_ids = [
    aws_security_group.ssh_access.id,
    aws_security_group.web_access.id
  ]

  tags = {
    Name = "app-server"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo DEBIAN_FRONTEND=noninteractive apt update -y",
      "sudo DEBIAN_FRONTEND=noninteractive apt install -y git python3-pip"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.private_key_path)
      host        = self.public_ip
    }
  }
}
