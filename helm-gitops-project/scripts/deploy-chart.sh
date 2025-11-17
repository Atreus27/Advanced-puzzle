#!/bin/bash

CHART_NAME="application"
NAMESPACE="default"
VALUES_FILE="values.yaml"
RELEASE_NAME="application-release"

# Decide environment
if [ "$1" == "dev" ]; then
    VALUES_FILE="values/dev.yaml"
    RELEASE_NAME="${RELEASE_NAME}-dev"
elif [ "$1" == "prod" ]; then
    VALUES_FILE="values/prod.yaml"
    RELEASE_NAME="${RELEASE_NAME}-prod"
fi

echo "🔄 Deploying HELM release: $RELEASE_NAME"
echo "📁 Using values file: ./charts/$CHART_NAME/$VALUES_FILE"
echo "📌 Namespace: $NAMESPACE"

# Run deployment
helm upgrade --install "$RELEASE_NAME" "./charts/$CHART_NAME" \
    -n "$NAMESPACE" \
    -f "./charts/$CHART_NAME/$VALUES_FILE" \
    --wait --timeout 300s

# Check status
if [ $? -eq 0 ]; then
    echo "✅ Deployment of $RELEASE_NAME to namespace $NAMESPACE succeeded."
else
    echo "❌ Deployment of $RELEASE_NAME FAILED."
    exit 1
fi
