# Accounts REST API

A Flask service for creating, reading, updating, and deleting customer accounts.

[![CI Build](https://github.com/InFERNo00000/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/InFERNo00000/devops-capstone-project/actions/workflows/ci-build.yaml)

## Run locally

```powershell
python -m pip install -r requirements.txt
python run.py
```

The service listens on `http://localhost:8080`. `GET /health` reports service health.

## API

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/accounts` | Create an account |
| `GET` | `/accounts` | List accounts |
| `GET` | `/accounts/{id}` | Read an account |
| `PUT` | `/accounts/{id}` | Update account fields |
| `DELETE` | `/accounts/{id}` | Delete an account |

JSON account fields are `name`, `email`, `phone_number`, `address`, and
`account_type`. `name` and `email` are required at creation; email addresses are
unique. Responses use JSON, and invalid input, duplicate emails, and missing
accounts return appropriate 4xx responses.

## Test and lint

```powershell
flake8 service tests run.py
pylint service tests run.py
nosetests
```

## Security and deployment

Talisman adds security headers, while Flask-CORS only allows configured origins.
Set `CORS_ALLOWED_ORIGINS` to a comma-separated origin list and set
`FORCE_HTTPS=true` behind a correctly configured HTTPS ingress. The Dockerfile
runs as a non-root user. Kubernetes manifests are in `k8s/`; update the image
reference in `k8s/deployment.yaml` to the image published by your registry before
deploying. The SQLite volume is ephemeral and is intended only for the capstone
demonstration, not a production deployment.

Tekton definitions are in `tekton/`. Install the Tekton Catalog `git-clone` Task
and apply `tekton/tasks.yaml` and `tekton/pipeline.yaml` to a cluster. A PipelineRun
must bind a writable source workspace, a registry-auth Secret containing
`config.json`, and a kubeconfig Secret containing `config`. The cluster must permit
the Buildah step's privileged security context. These credentials and a successful
PipelineRun are environment-specific and are not included here.
