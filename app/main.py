from fastapi import FastAPI

app = FastAPI(title="Kubernetes GitOps Platform")


@app.get("/")
def home():
    return {
        "message": "Kubernetes GitOps Platform is running!",
        "version": "1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/info")
def info():
    return {
        "application": "DevOps Task API",
        "environment": "development"
    }