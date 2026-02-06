#!/bin/bash
# Deployment script for Central Planner

set -e

echo "🚀 Starting Cloud Build deployment..."
echo "Project: $(gcloud config get-value project)"
echo "Region: us-central1"
echo ""

# Submit to Cloud Build
gcloud builds submit --config cloudbuild.yaml .

echo ""
echo "✅ Deployment complete!"
echo "🌐 App URL: https://central-planner-app-216559257034.us-central1.run.app"
