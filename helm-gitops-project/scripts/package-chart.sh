#!/bin/bash

set -e

CHART_DIR="charts/application"
OUTPUT_DIR="charts"

echo "📦 Packaging Helm chart from: $CHART_DIR"

# Move into chart directory
cd "$CHART_DIR"

# Package chart
helm package .

echo "📦 Chart packaged successfully."

# Move generated .tgz file back to parent charts folder
mv ./*.tgz "../"

echo "📁 Packaged chart moved to: $OUTPUT_DIR"
echo "✅ Done."
