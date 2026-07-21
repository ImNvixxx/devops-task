# Monitoring Runbook

## Service Down

Check:

kubectl get pods

kubectl describe pod

kubectl logs

Restart:

kubectl rollout restart deployment app

--------------------------------

## High CPU

kubectl top pods

kubectl top nodes

Check running requests

Scale deployment

kubectl scale deployment app --replicas=4

--------------------------------

## High Latency

Check database

Check network

Increase replicas

--------------------------------

## High Error Rate

kubectl logs

kubectl describe pod

Rollback if needed

kubectl rollout undo deployment app
