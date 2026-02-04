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
| **Registry** | **Artifact Registry** | Stores the Docker container images for the application. Repo: `central-planner-app` |
| **Compute** | **Google Cloud Run** | Hosts the Streamlit application as a serverless container. Scalable and only runs when requests are active. |
| **Authentication** | **Identity-Aware Proxy (IAP)** | Secures the `run.app` URL. Intercepts incoming requests and requires a Google login before granting access to authorized users. |
| **Secret Management** | **Secret Manager** | Securely stores the GitHub Personal Access Token (`GITHUB_TOKEN`) used for repository synchronization. |
| **Persistence** | **Git / GitHub** | Acts as the source of truth for planning files. The app pulls content from GitHub to ephemeral storage on startup. |
| **Storage (Ephemeral)** | **In-memory / `/tmp`** | Stores the cloned repository during the container's lifetime. Note that this is cleared when the instance shuts down. |

## Deployment Commands

### Local Development
To run the Streamlit dashboard locally:
```bash
pip install -r requirements.txt
streamlit run src/app.py
```

### Build Image
```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/eikasia-ops/central-planner-repo/central-planner-app:latest .
```

### Deploy to Cloud Run
```bash
gcloud run deploy central-planner-app \
    --image us-central1-docker.pkg.dev/eikasia-ops/central-planner-repo/central-planner-app:latest \
    --region us-central1 \
    --platform managed \
    --set-env-vars="REPO_MOUNT_POINT=/tmp/central_planner_repo,GITHUB_REPO_URL=https://github.com/eikasia-llc/central_planner.git" \
    --set-secrets="GITHUB_TOKEN=GITHUB_TOKEN:latest"
```

## Key Files
- status: active
<!-- content -->
- **`MD_CONVENTIONS.md`**: The definitive guide on how to write files in this repository.
- **`AGENTS.md`**: The entry point for any AI agent joining the project.


### Initiating IAP Configuration

Setting up Identity-Aware Proxy (IAP): The first step involves enabling IAP on the Cloud Run service. After that, the IAM permissions are next

Internet Access: to expose the service securely to the internet without the cost of a Load Balancer, I enabled Identity-Aware Proxy (IAP) directly on the Cloud Run service.

Managed Authentication: Users are now required to sign in with their Google accounts before reaching the application.
Verification: I verified that the service URL correctly intercepts requests and identifies the user session.

Use the gcloud beta run services update --iap command to enable Direct IAP for the Cloud Run service.

```
gcloud run services enable-iap central-planner-app --region us-central1 --project eikasia-ops 2>&1

gcloud beta run deploy central-planner-app \
       --region us-central1 \
       --project eikasia-ops \
       --iap \
       --no-allow-unauthenticated 2>&1
```

### On Ephemeral Storage

In Google Cloud Run, a container's life doesn't end the moment it finishes sending an HTTP response. Instead, it enters a state of "idle" where Google keeps it alive to avoid the performance penalty of a "cold start" for the next request.

#### The "Idle" Grace Period
Once your container sends the final byte of a response, it is marked as idle.
Default Duration: Cloud Run typically keeps idle instances alive for up to 15 minutes.
Purpose: This "warm" state allows the container to handle subsequent requests instantly. If a new request arrives during this window, the container is "reused," and the idle timer resets.
Persistent storage is github. Manually synced via UI buttons.

## Security Layers

1. **IAM Controls**: The Cloud Run service account is restricted to minimal permissions (`Secret Manager Secret Accessor` only for specific secrets).
2. **Secret Masking**: The GitHub PAT is injected as a secret reference, never exposed in environment variables or logs in plain text.
3. **Private Access**: Service is restricted by Org Policy, accessible via `gcloud run services proxy`.

### Permissions

To access the app: Grant access to your specific account (Recommended)
Instead of making it public, we grant ourseles permission to view it. 
This is the command:

```
gcloud run services add-iam-policy-binding knowledge-base-app \
    --region=us-central1 \
    --member="user:eikasia@eikasia.com" \
    --role="roles/run.invoker" \
    --project=eikasia-ops

```
That grants IAM run.invoker role to eikasia user
