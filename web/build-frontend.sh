#!/bin/bash
# Build frontend for deployment

echo "🔨 Building Vue.js frontend..."

cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm ci --only=production

# Build for production
echo "🏗️ Building for production..."
npm run build

# Copy to static directory
echo "📁 Copying to static directory..."
mkdir -p ../static
cp -r dist/* ../static/

echo "✅ Frontend build complete!"
echo "📂 Files copied to web/static/"