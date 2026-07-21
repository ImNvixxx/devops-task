# DevOps Task 2

## Overview

This project demonstrates a production-oriented deployment of a **FastAPI** application with **PostgreSQL** on **Kubernetes**. It includes high availability, health checks, rolling updates, monitoring, alerting, backup/restore scripts, and load testing.

---

# Architecture

```text
                    +----------------------+
                    |  NGINX Ingress       |
                    +----------+-----------+
                               |
                        ClusterIP Service
                               |
                 +-------------+-------------+
                 |                           |
           FastAPI Pod #1              FastAPI Pod #2
                 |                           |
                 +-------------+-------------+
                               |
                      PostgreSQL Service
                               |
                         PostgreSQL Pod
                               |
                              PVC
```

---

# Features

* FastAPI application
* PostgreSQL database
* Kubernetes Deployments
* Rolling Updates
* Resource Requests & Limits
* Startup, Readiness and Liveness Probes
* ConfigMap & Secret
* PersistentVolumeClaim
* NGINX Ingress
* Database Migration Job
* Prometheus Monitoring
* Grafana Dashboard
* Alertmanager
* Backup & Restore Scripts
* Load Testing using k6

---

# Repository Structure

```text
.
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── k8s/
│   ├── namespace.yaml
│   ├── secret.yaml
│   ├── configmap.yaml
│   ├── postgres-*.yaml
│   ├── app-*.yaml
│   ├── ingress.yaml
│   ├── migration-job.yaml
│   ├── oom-test.yaml
│   └── monitoring/
│       ├── prometheus-*.yaml
│       ├── grafana-*.yaml
│       ├── alertmanager-*.yaml
│       ├── load-test.js
│       └── RUNBOOK.md
│
├── nginx/
├── prometheus/
├── scripts/
│   ├── backup.sh
│   └── restore.sh
│
├── docker-compose.yml
└── README.md
```

---

# Prerequisites

The following software is required:

* Docker
* Kubernetes (Minikube or Kind)
* kubectl
* NGINX Ingress Controller

Verify installation:

```bash
docker --version
kubectl version --client
```

---

# Build Application Image

If using **Minikube**:

```bash
eval $(minikube docker-env)
docker build -t app:latest ./app
```

If using **Kind**:

```bash
docker build -t app:latest ./app
kind load docker-image app:latest
```

---

# Deploy Application

Deploy all Kubernetes resources:

```bash
kubectl apply -f k8s/
```

Wait for deployments:

```bash
kubectl get pods -n devops-task
```

Check services:

```bash
kubectl get svc -n devops-task
```

Check ingress:

```bash
kubectl get ingress -n devops-task
```

---

# Database Migration

Verify migration job:

```bash
kubectl get jobs -n devops-task
```

Migration logs:

```bash
kubectl logs job/db-migration -n devops-task
```

---

# Health Checks

Startup Probe

```
GET /live
```

Readiness Probe

```
GET /health/ready
```

Liveness Probe

```
GET /live
```

---

# Monitoring

Deploy monitoring stack:

```bash
kubectl apply -f k8s/monitoring/
```

Port-forward Prometheus:

```bash
kubectl port-forward -n monitoring svc/prometheus 9091:9090
```

Open:

```
http://localhost:9091
```

Port-forward Grafana:

```bash
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

Open:

```
http://localhost:3000
```

Application metrics endpoint:

```
/metrics
```

---

# Alertmanager

Trigger an alert by scaling the application to zero replicas:

```bash
kubectl scale deployment app \
  -n devops-task \
  --replicas=0
```

Check Prometheus rules:

```bash
curl http://localhost:9091/api/v1/rules
```

Check application logs:

```bash
kubectl logs -n devops-task -l app=app
```

---

# Load Testing

Run the k6 load test:

```bash
k6 run k8s/monitoring/load-test.js
```

---

# Backup

Create PostgreSQL backup:

```bash
./scripts/backup.sh
```

---

# Restore

Restore database:

```bash
./scripts/restore.sh
```

---

# Validation

Pods

```bash
kubectl get pods -n devops-task
```

Services

```bash
kubectl get svc -n devops-task
```

Deployments

```bash
kubectl get deployments -n devops-task
```

Ingress

```bash
kubectl get ingress -n devops-task
```

PVC

```bash
kubectl get pvc -n devops-task
```

---

# Failure Scenarios

## 1. Service Selector Failure

Validation:

```bash
kubectl get endpoints -n devops-task
```

Expected:

* Service has no endpoints.
* Application becomes unavailable.

---

## 2. Rolling Update

Trigger rollout:

```bash
kubectl rollout restart deployment/app \
  -n devops-task
```

Validation:

```bash
kubectl rollout status deployment/app \
  -n devops-task
```

Expected:

* Zero downtime
* New Pods become Ready before old Pods terminate.

---

## 3. OOMKilled

Deploy stress workload:

```bash
kubectl apply -f k8s/oom-test.yaml
```

Describe pod:

```bash
kubectl describe pod <OOM_POD_NAME> \
  -n devops-task
```

Expected:

```
Reason: OOMKilled
Exit Code: 137
```

---

## 4. Rollback

Rollback deployment:

```bash
kubectl rollout undo deployment/app \
  -n devops-task
```

Verify:

```bash
kubectl rollout status deployment/app \
  -n devops-task
```

---

# Technologies

* Kubernetes
* Docker
* FastAPI
* PostgreSQL
* Python 3.12
* Prometheus
* Grafana
* Alertmanager
* NGINX Ingress
* k6

---

# Author

**Navid Mardani**

GitHub: https://github.com/ImNvixxx
