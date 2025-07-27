provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket = "soattc-auth-app"
    key    = "auth-microservice/terraform.tfstate"
    region = "us-east-1" # ajuste para sua região
  }
}

# data "terraform_remote_state" "aws" {
#   backend = "s3"
#   config = {
#     bucket = "soattc-aws-infra"
#     key    = "aws-infra/terraform.tfstate"
#     region = "us-east-1"
#   }
# }

# data "terraform_remote_state" "rds" {
#   backend = "s3"
#   config = {
#     bucket = "soattc-auth-db"
#     key    = "auth-microservice/terraform.tfstate"
#     region = "us-east-1"
#   }
# }

provider "kubernetes" {
  host                   = data.terraform_remote_state.aws.outputs.eks_cluster_endpoint
  cluster_ca_certificate = base64decode(data.terraform_remote_state.aws.outputs.eks_cluster_ca)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

data "aws_eks_cluster_auth" "cluster" {
  name = var.cluster_name
}

resource "kubernetes_deployment" "auth_app" {
  metadata {
    name      = "auth-app"
    namespace = "default"
    labels = {
      app = "auth-app"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "auth-app"
      }
    }
    template {
      metadata {
        labels = {
          app = "auth-app"
        }
      }
      spec {
        container {
          name  = "auth-app"
          image = "086134737169.dkr.ecr.us-east-1.amazonaws.com/soattc-auth-app:latest"
          env {
            name  = "MYSQL_HOST"
            value = replace(data.terraform_remote_state.rds.outputs.db_endpoint, ":3306", "")
          }
          env {
            name  = "MYSQL_USER"
            value = var.db_username
          }
          env {
            name  = "MYSQL_PASSWORD"
            value = var.db_password
          }
          env {
            name  = "MYSQL_PORT"
            value = "3306"
          }
          env {
            name  = "SECRET_KEY"
            value = var.secret_key
          }
          env {
            name = "MYSQL_DATABASE"
            value = data.terraform_remote_state.rds.outputs.db_name
          }
          port {
            container_port = 8005
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "auth_app_lb" {
  depends_on = [kubernetes_deployment.auth_app]
  metadata {
    name      = "auth-app-lb"
    namespace = "default"
  }
  spec {
    selector = {
      app = "auth-app"
    }
    type = "LoadBalancer"
    port {
      port        = 80
      target_port = 8005
    }
  }
}