resource "aws_db_subnet_group" "recipe_db_subnet" {
  name = "recipe-db-subnet-group"
  subnet_ids = [
    aws_subnet.private_subnet_1.id,
    aws_subnet.private_subnet_2.id
  ]

  tags = {
    Name = "Recipe DB Subnet Group"
  }
}

resource "aws_security_group" "rds_access" {
  name        = "allow_rds"
  description = "Allow Postgres access from EC2"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ssh_access.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_db_instance" "recipe_db" {
  allocated_storage   = 20
  engine              = "postgres"
  engine_version      = "15.13"
  instance_class      = "db.t3.micro"
  db_name             = var.db_name
  username            = var.db_user
  password            = var.db_password
  skip_final_snapshot = true

  vpc_security_group_ids = [aws_security_group.rds_access.id]
  db_subnet_group_name   = aws_db_subnet_group.recipe_db_subnet.id

  publicly_accessible = true
}
