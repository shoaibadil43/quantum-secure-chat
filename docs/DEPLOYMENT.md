"""
Deployment Guide
"""

# Deployment Guide - Quantum Secure Chat

## Table of Contents
1. [Local Development](#local-development)
2. [Staging Environment](#staging-environment)
3. [Production Deployment](#production-deployment)
4. [Cloud Providers](#cloud-providers)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Local Development

### Docker Compose (Recommended)
```bash
docker-compose up -d
```

This starts:
- PostgreSQL database
- Redis cache
- FastAPI backend
- Optional: Flutter web frontend

---

## Staging Environment

### 1. Virtual Private Server (VPS)

#### Setup Steps
```bash
# 1. SSH into VPS
ssh user@staging.example.com

# 2. Install dependencies
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install docker.io docker-compose nginx git

# 3. Clone repository
git clone https://github.com/yourusername/quantum-secure-chat.git
cd quantum-secure-chat

# 4. Configure environment
cp backend/.env.example backend/.env.staging
# Edit with staging credentials

# 5. Start services
docker-compose -f docker-compose.staging.yml up -d

# 6. Setup Nginx reverse proxy
sudo cp nginx/staging.conf /etc/nginx/sites-available/quantum-chat
sudo ln -s /etc/nginx/sites-available/quantum-chat /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### Nginx Configuration (nginx/staging.conf)
```nginx
upstream backend {
    server backend:8000;
}

server {
    listen 80;
    server_name staging.quantum-secure-chat.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name staging.quantum-secure-chat.com;
    
    ssl_certificate /etc/letsencrypt/live/staging.quantum-secure-chat.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/staging.quantum-secure-chat.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    client_max_body_size 10M;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /ws/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;
    }
}
```

#### SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --standalone -d staging.quantum-secure-chat.com
```

---

## Production Deployment

### AWS ECS + Load Balancer

#### 1. Push Docker Image to ECR
```bash
# Authenticate with ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Build and push image
docker build -t quantum-chat:latest ./backend
docker tag quantum-chat:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/quantum-chat:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/quantum-chat:latest
```

#### 2. Create ECS Task Definition
```json
{
  "family": "quantum-chat",
  "containerDefinitions": [
    {
      "name": "quantum-chat-api",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/quantum-chat:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/quantum-chat",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://user:password@rds-instance:5432/quantum_chat"
        },
        {
          "name": "REDIS_URL",
          "value": "redis://elasticache-endpoint:6379"
        }
      ],
      "secrets": [
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:quantum-chat/secret-key"
        }
      ]
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "512",
  "memory": "1024"
}
```

#### 3. Create ECS Service
```bash
aws ecs create-service \
  --cluster quantum-chat-prod \
  --service-name quantum-chat-api \
  --task-definition quantum-chat:1 \
  --desired-count 3 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx]}" \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=quantum-chat-api,containerPort=8000
```

---

### Kubernetes Deployment

#### 1. Create Namespace
```bash
kubectl create namespace quantum-chat
```

#### 2. Deploy Database
```bash
kubectl apply -f k8s/postgres-deployment.yaml -n quantum-chat
kubectl apply -f k8s/redis-deployment.yaml -n quantum-chat
```

#### 3. Deploy Backend
```bash
kubectl apply -f k8s/backend-deployment.yaml -n quantum-chat
kubectl apply -f k8s/backend-service.yaml -n quantum-chat
```

#### 4. Setup Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: quantum-chat-ingress
  namespace: quantum-chat
spec:
  ingressClassName: nginx
  rules:
  - host: api.quantum-secure-chat.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: quantum-chat-api
            port:
              number: 8000
```

---

## Cloud Providers Setup

### AWS
- **Database**: RDS PostgreSQL (Multi-AZ)
- **Cache**: ElastiCache Redis
- **Compute**: ECS Fargate or EC2
- **Load Balancing**: Application Load Balancer
- **DNS**: Route 53
- **Secrets**: AWS Secrets Manager
- **Monitoring**: CloudWatch

### Google Cloud
- **Database**: Cloud SQL PostgreSQL
- **Cache**: Cloud Memorystore (Redis)
- **Compute**: Cloud Run or GKE
- **Load Balancing**: Cloud Load Balancing
- **DNS**: Cloud DNS
- **Secrets**: Secret Manager
- **Monitoring**: Cloud Monitoring

### Azure
- **Database**: Azure Database for PostgreSQL
- **Cache**: Azure Cache for Redis
- **Compute**: Azure Container Instances or AKS
- **Load Balancing**: Azure Load Balancer
- **DNS**: Azure DNS
- **Secrets**: Key Vault
- **Monitoring**: Azure Monitor

---

## Monitoring & Maintenance

### Health Checks
```bash
# API Health
curl https://api.quantum-secure-chat.com/health

# Database Check
psql postgresql://user:password@host/quantum_chat -c "SELECT 1"

# Redis Check
redis-cli ping
```

### Backup Strategy
```bash
# Database Backup (Daily)
pg_dump quantum_chat | gzip > backup_$(date +%Y%m%d).sql.gz

# Upload to S3
aws s3 cp backup_*.sql.gz s3://quantum-chat-backups/

# Restore from backup
gunzip < backup_20240226.sql.gz | psql quantum_chat
```

### Log Monitoring
```bash
# View application logs
docker logs quantum-chat-api -f

# ECS Logs
aws logs tail /ecs/quantum-chat --follow

# CloudWatch Logs Insight
aws logs start-query \
  --log-group-name /ecs/quantum-chat \
  --start-time 1708940400 \
  --end-time 1708944000 \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | stats count() by @message'
```

### Performance Monitoring
- **CPU/Memory**: Monitor with CloudWatch/Prometheus
- **Database**: Monitor with RDS Performance Insights
- **API Response Time**: Track with APM tools (New Relic, Datadog)
- **Error Rate**: Alert on > 1% error rate

### Scaling Configuration

#### Auto-Scaling (AWS ECS)
```json
{
  "Policies": [
    {
      "PolicyName": "scale-up",
      "AutoScalingGroupName": "quantum-chat",
      "AdjustmentType": "PercentChangeInCapacity",
      "MetricAggregationType": "Average",
      "StepAdjustments": [
        {
          "MetricIntervalLowerBound": 0,
          "ScalingAdjustment": 50
        }
      ]
    }
  ],
  "Alarms": [
    {
      "AlarmName": "high-cpu",
      "MetricName": "CPUUtilization",
      "Threshold": 70
    }
  ]
}
```

---

## Maintenance Tasks

### Weekly
- [ ] Review error logs
- [ ] Check backup completion
- [ ] Monitor resource usage
- [ ] Security patch review

### Monthly
- [ ] Test backup restoration
- [ ] Review SSL certificates
- [ ] Performance analysis
- [ ] Cost optimization

### Quarterly
- [ ] Security audit
- [ ] Dependency updates
- [ ] Database optimization
- [ ] Disaster recovery drill

---

For more information, see [Setup Guide](./SETUP.md)
