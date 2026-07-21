# DevOps Task 2

## Project Overview

This project demonstrates deploying a FastAPI application with PostgreSQL on Kubernetes using production-oriented best practices.

## Architecture

```
                 +----------------+
                 |    Ingress     |
                 +-------+--------+
                         |
                    ClusterIP Service
                         |
             +-----------+-----------+
             |                       |
        App Pod #1              App Pod #2
             |                       |
             +-----------+-----------+
                         |
                    PostgreSQL Service
                         |
                    PostgreSQL Pod
                         |
                         PVC
```

---

## Components

### Namespace

All resources are deployed inside:

- `devops-task`

---

### Application Deployment

Features:

- 2 replicas
- Rolling Updates
- Resource Requests/Limits
- Startup Probe
- Readiness Probe
- Liveness Probe

---

### Services

- App Service (ClusterIP)
- PostgreSQL Service (ClusterIP)

---

### Configuration

Configuration is managed using:

- ConfigMap
- Secret

---

### Persistent Storage

PostgreSQL uses a PersistentVolumeClaim (PVC).

---

### Ingress

Ingress resource exposes the application.

Host:

```
devops.local
```

Ingress Class:

```
nginx
```

---

### Database Migration

A Kubernetes Job simulates database initialization.

The Job:

- waits for PostgreSQL
- connects to the database
- creates the schema_version table
- inserts initial schema version

---

## Health Checks

### Startup Probe

```
GET /live
```

### Readiness Probe

```
GET /health/ready
```

### Liveness Probe

```
GET /live
```

---

# Deployment

Apply resources:

```bash
kubectl apply -f namespace.yaml
kubectl apply -f secret.yaml
kubectl apply -f configmap.yaml
kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f app-deployment.yaml
kubectl apply -f app-service.yaml
kubectl apply -f ingress.yaml
kubectl apply -f migration-job.yaml
```

---

# Validation

Check Pods

```bash
kubectl get pods -n devops-task
```

Check Services

```bash
kubectl get svc -n devops-task
```

Check Ingress

```bash
kubectl get ingress -n devops-task
```

Migration Logs

```bash
kubectl logs job/db-migration -n devops-task
```

---

# Failure Scenarios

## 1. Service Selector Failure

The Service selector was intentionally modified.

Result:

- Service lost all endpoints
- Application became unreachable

Validation:

```bash
kubectl get endpoints -n devops-task
```

---

## 2. Rolling Update

Deployment was updated.

Observed:

- Zero downtime
- Pods replaced gradually
- New Pods became Ready before old Pods terminated

Validation:

```bash
kubectl rollout status deployment/app -n devops-task
```

---

## 3. Resource Limit / OOMKilled

A dedicated deployment (`oom-test`) was created with:

```
Request:
16Mi

Limit:
32Mi
```

A Python process continuously allocated memory.

Observed:

- Exit Code 137
- OOMKilled
- CrashLoopBackOff
- Automatic restart

Validation:

```bash
kubectl describe pod <oom-pod> -n devops-task
```

Expected output:

```
Reason: OOMKilled
Exit Code: 137
```

---

## 4. Rollback

Deployment rollback was executed.

Validation:

```bash
kubectl rollout undo deployment/app -n devops-task

kubectl rollout status deployment/app -n devops-task
```

Result:

Deployment successfully restored to the previous stable revision.

---

# Monitoring

The application exposes Prometheus metrics at:

```
/metrics
```

---

# Technologies

- Kubernetes
- FastAPI
- PostgreSQL
- Prometheus Client
- Docker
- Python 3.12

## Running SVC/Prometheus on port 9091

- kubectl port-forward -n monitoring svc/prometheus 9091:9090
- http://localhost:9091/targets
## Alert Messenger Test

kubectl scale deployment app -n devops-task --replicas=0

curl http://localhost:9090/api/v1/rules

kubectl logs -n devops-task -l app=app
