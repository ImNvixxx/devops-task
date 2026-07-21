# DevOps Task 2

Production-ready deployment of a **FastAPI** application with **PostgreSQL** on **Kubernetes**.

The project demonstrates containerization, orchestration, health checks, rolling updates, monitoring, alerting, backup & restore, and load testing using common DevOps tools.

---

# Architecture

```text
                    +----------------------+
                    |   NGINX Ingress      |
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
                    Persistent Volume Claim
```

---

# Features

- FastAPI application
- PostgreSQL database
- Docker & Docker Compose
- Kubernetes Deployments
- Rolling Updates
- Resource Requests & Limits
- Startup, Readiness & Liveness Probes
- ConfigMap & Secret
- PersistentVolumeClaim
- NGINX Ingress
- Database Migration Job
- Prometheus Monitoring
- Grafana Dashboard
- Alertmanager
- Backup & Restore Scripts
- Load Testing using k6

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

Install the following software before running the project.

- Docker
- Kubernetes (Minikube or Kind)
- kubectl
- NGINX Ingress Controller
- k6 (optional, for load testing)

Verify your installation:

```bash
docker --version
kubectl version --client
minikube version
```

---

# Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/ImNvixxx/devops-task.git
cd devops-task
```

---

## 2. Create the environment file

Create a `.env` file in the project root.

Example:

```env
DB_HOST=postgres
DB_NAME=appdb
DB_USER=appuser
DB_PASSWORD=password
```

Adjust the values if your database configuration is different.

---

## 3. Build the application image

### Minikube

```bash
eval $(minikube docker-env)

docker build -t devops-task-2-app:latest ./app
```

### Kind

```bash
docker build -t devops-task-2-app:latest ./app

kind load docker-image devops-task-2-app:latest
```
---

## 4. Deploy the application

Deploy all Kubernetes resources.

```bash
kubectl apply -f k8s/
```

Wait until every Pod is running.

```bash
kubectl get pods -n devops-task -w
```

---

## 5. Verify the deployment

```bash
kubectl get deployments -n devops-task

kubectl get svc -n devops-task

kubectl get ingress -n devops-task
```

---

## 6. Access the application

Using Port Forward:

```bash
kubectl port-forward -n devops-task svc/app-service 8000:8000
```

Application:

```
http://localhost:8000
```

Health Check:

```
http://localhost:8000/live
```

Metrics:

```
http://localhost:8000/metrics
```

---

# Database Migration

Verify that the migration job completed successfully.

```bash
kubectl get jobs -n devops-task
```

View migration logs.

```bash
kubectl logs job/db-migration -n devops-task
```

---

# Health Checks

The application exposes the following endpoints.

| Endpoint | Purpose |
|----------|---------|
| `/live` | Liveness Probe |
| `/health/ready` | Readiness Probe |
| `/metrics` | Prometheus Metrics |

---

# Monitoring

Deploy the monitoring stack.

```bash
kubectl apply -f k8s/monitoring/
```

---

## Prometheus

```bash
kubectl port-forward -n monitoring svc/prometheus 9091:9090
```

Open:

```
http://localhost:9091
```

---

## Grafana

```bash
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

Open:

```
http://localhost:3000
```

Default credentials:

```
Username: admin

Password: admin
```

---

# Alertmanager

Trigger an alert by scaling the application to zero replicas.

```bash
kubectl scale deployment app \
  -n devops-task \
  --replicas=0
```

Verify alert rules.

```bash
curl http://localhost:9091/api/v1/rules
```

View application logs.

```bash
kubectl logs -n devops-task -l app=app
```

---

# Load Testing

Run the load test.

```bash
k6 run k8s/monitoring/load-test.js
```

---

# Backup

Create a PostgreSQL backup.

```bash
./scripts/backup.sh
```

---

# Restore

Restore the database.

```bash
./scripts/restore.sh
```

---

# Validation

Check application status.

```bash
kubectl get pods -n devops-task

kubectl get deployments -n devops-task

kubectl get svc -n devops-task

kubectl get ingress -n devops-task

kubectl get pvc -n devops-task
```

Expected result:

- All Pods are **Running**
- Deployments are **Available**
- Services are created
- PVC is **Bound**
- The application responds with **HTTP 200**
- Prometheus is scraping metrics
- Grafana displays dashboards

---

# Failure Scenarios

## Service Selector Failure

```bash
kubectl get endpoints -n devops-task
```

Expected:

- Service has no endpoints.
- Application becomes unavailable.

---

## Rolling Update

```bash
kubectl rollout restart deployment/app -n devops-task
```

Verify rollout.

```bash
kubectl rollout status deployment/app -n devops-task
```

Expected:

- Zero downtime
- New Pods become Ready before old Pods terminate

---

## OOMKilled

Deploy the stress workload.

```bash
kubectl apply -f k8s/oom-test.yaml
```

Inspect the Pod.

```bash
kubectl describe pod <OOM_POD_NAME> -n devops-task
```

Expected:

```
Reason: OOMKilled
Exit Code: 137
```

---

## Rollback

Rollback the deployment.

```bash
kubectl rollout undo deployment/app -n devops-task
```

Verify.

```bash
kubectl rollout status deployment/app -n devops-task
```

---

# Troubleshooting

Check Pod details.

```bash
kubectl describe pod <pod-name> -n devops-task
```

View application logs.

```bash
kubectl logs -n devops-task <pod-name>
```

Check cluster events.

```bash
kubectl get events -n devops-task --sort-by=.metadata.creationTimestamp
```

Restart the deployment.

```bash
kubectl rollout restart deployment/app -n devops-task
```

---

# Technologies

- Kubernetes
- Docker
- FastAPI
- PostgreSQL
- Python 3.12
- Prometheus
- Grafana
- Alertmanager
- NGINX Ingress
- k6

---

# Assumptions

- Docker is installed and running.
- A Kubernetes cluster (Minikube or Kind) is available.
- kubectl is configured correctly.
- NGINX Ingress Controller is installed.

---

# Author

**Navid Mardani**

GitHub: https://github.com/ImNvixxx
