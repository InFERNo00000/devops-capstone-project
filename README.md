# DevOps Capstone Project: Accounts REST API

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
flake8 service tests tools run.py
pylint service tests tools run.py
$env:PYTHONPATH = "tools/nose_compat"
nosetests
```

The `PYTHONPATH` entry provides compatibility aliases for Nose's deprecated
standard-library APIs when running on Python 3.11.

## Security and deployment

Talisman adds security headers, while Flask-CORS only allows configured origins.
Set `CORS_ALLOWED_ORIGINS` to a comma-separated origin list and set
`FORCE_HTTPS=true` behind a correctly configured HTTPS ingress. The Dockerfile
runs as a non-root user. Kubernetes manifests are in `k8s/`; build and load the
`accounts-service:capstone` image into your cluster before deploying. The SQLite
volume is ephemeral and is intended only for the capstone demonstration, not a
production deployment.

Tekton definitions are in `tekton/`. The `accounts-cd` Pipeline clones the
repository, lints and tests it, builds and pushes an image with Buildah, then
updates the Kubernetes Deployment. A PipelineRun needs the Tekton Catalog
`git-clone` Task, a writable source workspace, a registry-auth Secret containing
`config.json`, and a kubeconfig Secret containing `config`. The target cluster
must permit the Buildah step's privileged security context and pull from the
configured registry.
