# Cloud Infrastructure: Central Planner

This document details the cloud components and security layers used to deploy and protect the Central Planner application on Google Cloud Platform.

## Architecture Diagram

```mermaid
graph TD
    User([User / Web Browser]) --> Proxy[GCloud Run Proxy / IAP]
    Proxy -- Authentication --> CR[Cloud Run Service]

    subgraph Container[Docker Container Port 8080]
        Nginx[nginx Reverse Proxy :8080]
        Streamlit[Streamlit App :8501]
        Flask[Flask API :8502]

        Nginx -- / --> Streamlit
        Nginx -- /api --> Flask
    end

    CR --> Nginx
    Streamlit -- Git Operations --> GitHub[GitHub Repository]
    Streamlit -- Renders --> Viz[D3 Visualization]
    Viz -- POST /api/save_edits --> Nginx
    Flask -- File Edits --> Temp[/tmp/central_planner_repo]
    Streamlit -- Runtime Files --> Temp

    CR -- Credentials --> SM[Secret Manager]
    SM -- GITHUB_TOKEN --> CR
    AR[Artifact Registry] -- Container Image --> CR
```

## Component Enumeration

### Cloud Infrastructure Components

| Component | Service | Purpose |
| :--- | :--- | :--- |
| **Registry** | **Artifact Registry** | Stores the Docker container images for the application. Repo: `central-planner-app` |
| **Compute** | **Google Cloud Run** | Hosts the multi-service application as a serverless container. Scalable and only runs when requests are active. |
| **Authentication** | **Identity-Aware Proxy (IAP)** | Secures the `run.app` URL. Intercepts incoming requests and requires a Google login before granting access to authorized users. |
| **Secret Management** | **Secret Manager** | Securely stores the GitHub Personal Access Token (`GITHUB_TOKEN`) used for repository synchronization. |
| **Persistence** | **Git / GitHub** | Acts as the source of truth for planning files. The app pulls content from GitHub to ephemeral storage on startup. |
| **Storage (Ephemeral)** | **In-memory / `/tmp`** | Stores the cloned repository during the container's lifetime. Note that this is cleared when the instance shuts down. |

### Application Components (Inside Container)

The application runs three services within a single container, coordinated by nginx:

#### 1. **nginx Reverse Proxy** (Port 8080)

**What:** Lightweight HTTP server and reverse proxy that acts as the single entry point for all external traffic.

**Why Needed:** Cloud Run only exposes one port to the internet. Without nginx, the browser cannot access the Flask API (port 8502) for editing operations. Nginx solves this by routing requests based on URL paths.

**How It Connects:**
- **External:** Receives all incoming traffic from Cloud Run on port 8080
- **Internal Routing:**
  - `/` → forwards to Streamlit (127.0.0.1:8501)
  - `/api/*` → forwards to Flask API (127.0.0.1:8502)
- **WebSocket Support:** Maintains WebSocket connections for Streamlit's real-time updates

**Configuration:** `nginx.conf` defines upstream servers and location-based routing rules.

#### 2. **Streamlit App** (Port 8501)

**What:** Python web framework that provides the interactive dashboard UI. Handles git operations, renders the visualization, and manages user interactions.

**Why Needed:** Provides the user interface for viewing and managing the Master Plan. Integrates git operations (pull/push) and embeds the D3 visualization.

**How It Connects:**
- **To nginx:** Listens on 127.0.0.1:8501 (internal only), receives HTTP/WebSocket traffic from nginx
- **To GitHub:** Uses `GitManager` to clone/pull/push via HTTPS with token authentication
- **To Visualization:** Embeds HTML/JavaScript D3 visualization using `streamlit.components.html()`
- **To Flask:** Indirectly - the embedded visualization's JavaScript sends API requests to `/api/save_edits`

**Main File:** `src/app.py`

#### 3. **Flask API** (Port 8502)

**What:** Lightweight Python web framework providing REST API endpoints for file editing operations.

**Why Needed:** The D3 visualization needs a way to save edits back to markdown files. JavaScript running in the browser cannot directly modify files on the server. Flask provides a secure API endpoint that accepts edit requests and applies them using the `FileEditor` class.

**How It Connects:**
- **To nginx:** Listens on 127.0.0.1:8502 (internal only), receives API requests from nginx
- **To Browser (via nginx):** JavaScript in the D3 visualization sends `POST /api/save_edits` requests
- **To File System:** Uses `FileEditor` to apply line-based edits to markdown files in `/tmp/central_planner_repo`
- **To Streamlit:** Indirectly - after successful edits, the visualization reloads and Streamlit re-parses the updated file

**Main File:** `src/api_server.py`

**Key Endpoints:**
- `POST /api/save_edits` - Apply metadata and content edits to markdown files
- `GET /api/health` - Health check endpoint

### Request Flow Examples

**Viewing the Dashboard:**
```
User Browser → Cloud Run (IAP) → nginx:8080 → Streamlit:8501 → HTML Response
```

**Saving Edits:**
```
1. User clicks Save in D3 visualization
2. JavaScript: POST /api/save_edits → nginx:8080
3. nginx routes /api/* → Flask:8502
4. Flask applies edits using FileEditor
5. Flask returns JSON success/error
6. JavaScript reloads page → triggers step 1 (Viewing)
```

**Git Push:**
```
User clicks Push → Streamlit executes GitManager.push() → GitHub API
```

## Build

### Create repository in Google Artifact for image push

```
gcloud artifacts repositories create central-planner-app \
    --repository-format=docker \
    --location=us-central1 \
    --project=eikasia-ops \
    --description="Docker images for knowledge_base app" 2>&1
```

### Cloud Build vs Docker Build

Cloud Build runs on Google's shared infrastructure. When you run gcloud builds submit:

1. Your local source is tarball'd and uploaded to a GCS bucket (gs://<project>_cloudbuild/source/). That's the only upload from your machine.                                         
2. A ephemeral VM spins up on Google's side. It pulls that tarball, runs each step sequentially — each step is its own container (gcr.io/cloud-builders/docker, etc.).
3. Each step's container does its work (build, push, deploy) inside GCP. The final image push goes from that VM to Artifact Registry — same network, no public internet.              

Bandwidth comparison:

```
  ┌────────────────────────────────────┬────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────┐
  │             What moves             │                 deploy.sh (local)                  │               cloudbuild.yaml (Cloud Build)                │
  ├────────────────────────────────────┼────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────┤
  │ Source upload                      │ nothing (already local)                            │ tarball → GCS (small, ~3.5 MiB here)                       │
  ├────────────────────────────────────┼────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────┤
  │ Base image pull (python:3.11-slim) │ your machine ← Docker Hub                          │ Cloud Build VM ← Docker Hub                                │
  ├────────────────────────────────────┼────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────┤
  │ Cache image pull (--cache-from)    │ N/A                                                │ Cloud Build VM ← Artifact Registry (same region, internal) │
  ├────────────────────────────────────┼────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────┤
  │ Final image push                   │ your machine → Artifact Registry (public internet) │ Cloud Build VM → Artifact Registry (internal)              │
  └────────────────────────────────────┴────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────┘
```

The big difference is the final image push. That's the heaviest artifact (the full runtime image). With deploy.sh that crosses your public internet connection. With Cloud Build it
stays inside GCP.

The base image pull from Docker Hub hits public internet in both cases. That's why --cache-from on the builder stage matters — if requirements.txt hasn't changed, the builder step
skips rebuilding entirely and the final image pull from Artifact Registry is internal and fast.

TL;DR: Cloud Build trades a small source upload for keeping the heavy image push internal to GCP. deploy.sh pushes that heavy image over your own connection.

## Deployment Commands

### Local Development

To run the full application stack locally (all three services):
```bash
pip install -r requirements.txt
./start.sh
```

This starts:
1. Flask API on port 8502 (background)
2. Streamlit on port 8501 (background)
3. nginx reverse proxy on port 8080 (foreground)

Access the app at: **http://localhost:8080**

**Development Mode (Streamlit only):**
For quick iteration without nginx:
```bash
streamlit run src/app.py
```
Note: Editing features won't work without Flask API running.

### Build Image

without a cloudbuild.yaml (recommended):

```bash
gcloud builds submit --config cloudbuild.yaml .
```

without a cloudbuild.yaml (not recommended):

```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/eikasia-ops/central-planner-repo/central-planner-app:latest .
```

### Deploy to Cloud Run
```bash
gcloud run deploy central-planner-app \
    --image us-central1-docker.pkg.dev/eikasia-ops/central-planner-repo/central-planner-app:latest \
    --region us-central1 \
    --platform managed \
    --port 8080 \
    --set-env-vars="REPO_MOUNT_POINT=/tmp/central_planner_repo,GITHUB_REPO_URL=https://github.com/eikasia-llc/central_planner.git" \
    --set-secrets="GITHUB_TOKEN=GITHUB_TOKEN:latest"
```

Note: `--port 8080` tells Cloud Run to route traffic to nginx, which then routes to Streamlit and Flask internally.

## Multi-Service Startup

The container startup is orchestrated by `start.sh`:

```bash
#!/bin/bash
# 1. Start Flask API in background on port 8502
python ./src/api_server.py &

# 2. Start Streamlit in background on port 8501 (bind to 127.0.0.1)
streamlit run ./src/app.py --server.port 8501 --server.address 127.0.0.1 &

# 3. Start nginx in foreground on port 8080
nginx -g 'daemon off;'
```

**Why this order:**
1. Flask starts first (fastest to start)
2. Streamlit starts second (needs time to initialize)
3. nginx starts last in foreground (keeps container alive)

**Startup sequence details:**
- Flask and Streamlit bind to `127.0.0.1` (localhost only, not exposed externally)
- nginx binds to `0.0.0.0:8080` (accepts external traffic)
- Cloud Run health checks hit `http://container:8080/` → nginx → Streamlit
- If nginx exits, the container stops (terminates Flask and Streamlit)

**Git identity configuration:**
During Streamlit's startup, `GitManager.startup_sync()` automatically configures:
```bash
git config user.name "Central Planner App"
git config user.email "central-planner-app@eikasia.com"
```
This allows the Push button to create commits without "Author identity unknown" errors.

## Troubleshooting

### "Network Error: Failed to fetch" when saving edits

**Cause:** The Flask API is not reachable from the browser, or nginx is not routing `/api/*` correctly.

**Solution:**
1. Check that all three services are running: `ps aux | grep -E 'nginx|streamlit|flask'`
2. Verify nginx config: `nginx -t`
3. Check Flask is listening: `curl http://127.0.0.1:8502/api/health`
4. Check nginx routing: `curl http://127.0.0.1:8080/api/health`

### "Author identity unknown" when using Git Push

**Cause:** Git user configuration is missing.

**Solution:** This should be automatic via `GitManager.startup_sync()`. If it fails:
```bash
git config user.name "Central Planner App"
git config user.email "central-planner-app@eikasia.com"
```

### Container fails to start in Cloud Run

**Cause:** One of the three services (Flask, Streamlit, nginx) is failing to start.

**Solution:** Check Cloud Run logs:
```bash
gcloud run services logs read central-planner-app --region us-central1 --limit 50
```

Look for startup errors from Flask, Streamlit, or nginx.

### Edit button visible but non-functional

**Cause:** JavaScript cannot reach the Flask API endpoint.

**Solution:**
1. Check browser console for errors (F12)
2. Verify the fetch URL is relative: `/api/save_edits` (not `http://localhost:8502`)
3. Ensure nginx is routing `/api/*` to Flask

## Key Files
- status: active
<!-- content -->
- **`MD_CONVENTIONS.md`**: The definitive guide on how to write files in this repository.
- **`AGENTS.md`**: The entry point for any AI agent joining the project.
- **`nginx.conf`**: Reverse proxy configuration for routing traffic
- **`start.sh`**: Multi-service startup orchestration script
- **`src/api_server.py`**: Flask API for file editing operations
- **`src/app.py`**: Streamlit dashboard application
- **`src/git_manager.py`**: Git operations wrapper with identity configuration


### Initiating IAP Configuration

Setting up Identity-Aware Proxy (IAP): The first step involves enabling IAP on the Cloud Run service. After that, the IAM permissions are next

Internet Access: to expose the service securely to the internet without the cost of a Load Balancer, I enabled Identity-Aware Proxy (IAP) directly on the Cloud Run service.

Managed Authentication: Users are now required to sign in with their Google accounts before reaching the application.
Verification: I verified that the service URL correctly intercepts requests and identifies the user session.

Use the gcloud beta run services update --iap command to enable Direct IAP for the Cloud Run service.

```
gcloud run services enable-iap central-planner-app --region us-central1 --project eikasia-ops 2>&1

gcloud beta run deploy central-planner-app \
       --image us-central1-docker.pkg.dev/eikasia-ops/central-planner-repo/central-planner-app:latest \
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
gcloud run services add-iam-policy-binding central-planner-app \
    --region=us-central1 \
    --member="user:eikasia@eikasia.com" \
    --role="roles/run.invoker" \
    --project=eikasia-ops

```
That grants IAM run.invoker role to eikasia user
