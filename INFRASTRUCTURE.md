# Cloud Infrastructure: Central Planner

This document details the cloud components and security layers used to deploy and protect the Central Planner application on Google Cloud Platform.

## Architecture Diagram

```mermaid
graph TD
    User([User / Web Browser]) --> Proxy[GCloud Run Proxy / IAP]
    Proxy -- Authentication --> CR[Cloud Run Service]
    CR -- Runtime Files --> Temp[/tmp/central_planner_repo]
    CR -- Pull/Push --> GitHub[GitHub Repository]
    CR -- Credentials --> SM[Secret Manager]
    SM -- GITHUB_TOKEN --> CR
    AR[Artifact Registry] -- Container Image --> CR
```

## Component Enumeration

| Component | Service | Purpose |
| :--- | :--- | :--- |
| **Compute** | **Google Cloud Run** | Hosts the Streamlit application as a serverless container. Scalable and only runs when requests are active. |
| **Registry** | **Artifact Registry** | Stores the Docker container images for the application. Repo: `central-planner-repo` |
| **Secret Management** | **Secret Manager** | Securely stores the GitHub Personal Access Token (`GITHUB_TOKEN`) used for repository synchronization. |
| **Persistence** | **Git / GitHub** | Acts as the source of truth for planning files. The app pulls content from GitHub to ephemeral storage on startup. |
| **Storage (Ephemeral)** | **In-memory / `/tmp`** | Stores the cloned repository during the container's lifetime. Note that this is cleared when the instance shuts down. |

## Deployment Commands

### Build Image
```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/eikasia-ops/central-planner-repo/central-planner:latest .
```

### Deploy to Cloud Run
```bash
gcloud run deploy central-planner \
    --image us-central1-docker.pkg.dev/eikasia-ops/central-planner-repo/central-planner:latest \
    --region us-central1 \
    --platform managed \
    --set-env-vars="REPO_MOUNT_POINT=/tmp/central_planner_repo,GITHUB_REPO_URL=https://github.com/eikasia-llc/central_planner.git" \
    --set-secrets="GITHUB_TOKEN=GITHUB_TOKEN:latest"
```

## Security Layers

1. **IAM Controls**: The Cloud Run service account is restricted to minimal permissions (`Secret Manager Secret Accessor` only for specific secrets).
2. **Secret Masking**: The GitHub PAT is injected as a secret reference, never exposed in environment variables or logs in plain text.
3. **Private Access**: Service is restricted by Org Policy, accessible via `gcloud run services proxy`.
