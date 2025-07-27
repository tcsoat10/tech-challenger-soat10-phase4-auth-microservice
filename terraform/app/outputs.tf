output "auth_app_lb_endpoint" {
  description = "Endpoint do Load Balancer do auth-app"
  value       = kubernetes_service.auth_app_lb.status[0].load_balancer[0].ingress[0].hostname
}