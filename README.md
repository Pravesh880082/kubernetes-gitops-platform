# 🚀 Kubernetes GitOps Platform

A containerized FastAPI application deployed on **Kubernetes (K3s)** running on **AWS EC2**, with an automated **CI/CD pipeline using GitHub Actions and Docker Hub**.

The main goal of this project is to demonstrate how application code can move from **GitHub → Docker → Docker Hub → AWS EC2 → Kubernetes** automatically without manually deploying the application after every code change.

---

## 📌 Project Overview

This project demonstrates a practical DevOps deployment workflow.

Whenever new code is pushed to the `main` branch:

1. GitHub Actions starts automatically.
2. The application Docker image is built.
3. The image is pushed to Docker Hub.
4. GitHub Actions connects to the AWS EC2 server through SSH.
5. Kubernetes deployment is restarted.
6. K3s pulls the latest Docker image.
7. New application pods are created.
8. Kubernetes maintains 2 running replicas.

This creates an automated deployment pipeline for the application.

---

## 🏗️ Architecture

```text
                    Developer
                        │
                        │ git push
                        ▼
                   ┌─────────┐
                   │ GitHub  │
                   └────┬────┘
                        │
                        ▼
                ┌───────────────┐
                │ GitHub Actions│
                └───────┬───────┘
                        │
                 Docker Build
                        │
                        ▼
                 ┌────────────┐
                 │ Docker Hub │
                 └─────┬──────┘
                       │
                       │ Latest Image
                       ▼
                ┌──────────────┐
                │   AWS EC2    │
                │    Ubuntu    │
                └──────┬───────┘
                       │
                       ▼
                    ┌─────┐
                    │ K3s │
                    └──┬──┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
          Pod 1               Pod 2
             │                   │
             └─────────┬─────────┘
                       ▼
              Kubernetes Service
                       │
                       ▼
               Traefik Ingress
                       │
                       ▼
                  FastAPI App
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Application development |
| **FastAPI** | REST API framework |
| **Docker** | Containerization |
| **Docker Hub** | Container image registry |
| **Kubernetes** | Container orchestration |
| **K3s** | Lightweight Kubernetes distribution |
| **AWS EC2** | Cloud server |
| **GitHub Actions** | CI/CD automation |
| **Traefik** | Kubernetes Ingress |
| **Linux / Ubuntu** | Server environment |
| **Git & GitHub** | Version control |

---

## 📂 Project Structure

```text
kubernetes-gitops-platform/
│
├── .github/
│   └── workflows/
│       ├── ci-cd.yml
│       └── deploy.yml
│
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
├── helm/
│
└── .gitignore
```

---

# ⚙️ Application

The application is a simple **FastAPI-based API** designed to demonstrate containerization and Kubernetes deployment.

### Available endpoints

### `/`

Returns the application status.

```json
{
  "message": "Kubernetes GitOps Platform is running!",
  "version": "1.0"
}
```

### `/health`

Health-check endpoint.

```json
{
  "status": "healthy"
}
```

### `/info`

Returns basic application information.

```json
{
  "application": "DevOps Task API",
  "environment": "development"
}
```

FastAPI also automatically provides:

```text
/docs
/redoc
/openapi.json
```

---

# 🐳 Docker

The application is packaged into a Docker image.

### Build locally

```bash
docker build -t kubernetes-gitops-platform .
```

### Run locally

```bash
docker run -p 8000:8000 kubernetes-gitops-platform
```

The application can then be accessed at:

```text
http://localhost:8000
```

---

# ☸️ Kubernetes Deployment

The application is deployed to a K3s Kubernetes cluster running on AWS EC2.

The deployment is configured with **2 replicas**:

```yaml
spec:
  replicas: 2
```

This results in two application pods running at the same time.

```text
Kubernetes Deployment
        │
   ┌────┴────┐
   ▼         ▼
 Pod 1     Pod 2
```

### Kubernetes resources

The project uses:

- Deployment
- Service
- Ingress

### Check deployment

```bash
sudo k3s kubectl get deployment
```

### Check pods

```bash
sudo k3s kubectl get pods
```

### Check service

```bash
sudo k3s kubectl get service
```

### Check ingress

```bash
sudo k3s kubectl get ingress
```

---

# 🌐 Kubernetes Service

The application is exposed internally through a Kubernetes `ClusterIP` service.

```text
FastAPI Pods
     │
     ▼
gitops-api-service
```

This allows Kubernetes to route traffic to the application pods.

---

# 🚦 Traefik Ingress

Traefik is used as the Kubernetes Ingress controller.

Traffic flows through:

```text
Client
  ↓
Traefik
  ↓
Ingress
  ↓
Kubernetes Service
  ↓
FastAPI Pods
```

This demonstrates basic Kubernetes networking and ingress configuration.

---

# 🔄 CI/CD Pipeline

One of the main purposes of this project is to automate application deployment.

The GitHub Actions workflow runs whenever code is pushed to the `main` branch.

```text
git push
   ↓
GitHub Actions
   ↓
Checkout source code
   ↓
Docker login
   ↓
Build image
   ↓
Push image to Docker Hub
   ↓
SSH into AWS EC2
   ↓
Restart Kubernetes deployment
   ↓
K3s pulls latest image
   ↓
New pods start
```

### GitHub Actions workflow

The pipeline performs:

### 1. Checkout

Gets the latest source code from GitHub.

### 2. Docker Hub Login

Authenticates using GitHub repository secrets.

### 3. Docker Build

Builds the application image.

### 4. Docker Push

Pushes the image to:

```text
pravesh880082/kubernetes-gitops-platform:latest
```

### 5. EC2 Deployment

GitHub Actions connects to the EC2 server using SSH.

It then runs:

```bash
sudo k3s kubectl rollout restart deployment/gitops-api-deployment
```

and waits for the deployment:

```bash
sudo k3s kubectl rollout status deployment/gitops-api-deployment
```

---

# 🔐 GitHub Secrets

Sensitive credentials are stored using **GitHub Actions Secrets**.

The project uses:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
EC2_HOST
EC2_SSH_KEY
```

No passwords, tokens, or private SSH keys are stored directly in the repository.

---

# ☁️ AWS Infrastructure

The Kubernetes cluster runs on an **AWS EC2 Ubuntu server**.

The server runs:

```text
Ubuntu
   ↓
K3s
   ↓
Kubernetes
   ↓
Traefik
   ↓
FastAPI application
```

The EC2 instance provides the cloud infrastructure required to host the Kubernetes application.

---

# 🧪 Testing

The deployment was tested directly through the Kubernetes/Ingress endpoint.

### Application test

```bash
curl http://<SERVER-IP>/
```

Expected:

```json
{
  "message": "Kubernetes GitOps Platform is running!",
  "version": "1.0"
}
```

### Health test

```bash
curl http://<SERVER-IP>/health
```

Expected:

```json
{
  "status": "healthy"
}
```

### Kubernetes status

The final deployment was verified with:

```bash
sudo k3s kubectl get pods
```

Result:

```text
NAME                                     READY   STATUS    RESTARTS
gitops-api-deployment-...                1/1     Running   0
gitops-api-deployment-...                1/1     Running   0
```

The deployment was also successfully rolled out:

```text
deployment "gitops-api-deployment" successfully rolled out
```

---

# 🎯 Main Purpose of the Project

The main purpose of this project is to demonstrate a practical **DevOps CI/CD deployment workflow**.

Instead of manually connecting to a server and deploying every application update, the process is automated:

```text
Code Change
     ↓
Git Push
     ↓
CI/CD
     ↓
Docker Image
     ↓
Docker Hub
     ↓
AWS EC2
     ↓
Kubernetes
     ↓
Updated Application
```

This demonstrates how modern DevOps workflows can reduce manual deployment work and make application delivery more consistent.

---

# 💡 What I Learned

While building this project, I gained hands-on experience with:

- Docker image creation and containerization
- Docker Hub image management
- GitHub Actions CI/CD
- GitHub repository secrets
- SSH-based automated deployment
- AWS EC2 server management
- Linux server administration
- K3s Kubernetes
- Kubernetes Deployments
- Kubernetes Services
- Kubernetes Ingress
- Traefik
- Kubernetes pod management
- Application health checks
- Deployment troubleshooting
- CI/CD pipeline debugging

---

# 🔧 Troubleshooting Experience

During development, I worked through real deployment issues including:

- Kubernetes API/TLS connection problems
- K3s service troubleshooting
- Docker Hub authentication errors
- GitHub Actions workflow failures
- Docker image pull problems
- Kubernetes `ImagePullBackOff`
- EC2 connectivity issues
- Deployment rollout verification

These issues helped me understand that DevOps is not only about writing configuration files but also about **debugging and maintaining the complete deployment pipeline**.

---

# 🚀 Future Improvements

Possible future improvements include:

- Use versioned Docker image tags instead of only `latest`
- Add automated application tests to CI
- Add Kubernetes readiness and liveness probes
- Add resource limits and requests
- Add Helm charts
- Implement Argo CD or Flux for a more complete GitOps workflow
- Add monitoring with Prometheus and Grafana
- Add centralized logging
- Add HTTPS/TLS through Traefik
- Add automated rollback strategies
- Use infrastructure-as-code with Terraform

---

# 👨‍💻 Author

**Pravesh Kumar**

DevOps / Cloud Engineering Enthusiast

Focused on building hands-on experience with:

```text
AWS
Docker
Kubernetes
K3s
GitHub Actions
Linux
CI/CD
Cloud
DevOps
```

---

## ⭐ Project Goal

> **Learn → Build → Break → Debug → Fix → Understand**

This project was built as a hands-on implementation of a real-world DevOps deployment pipeline rather than just a theoretical Kubernetes exercise.
