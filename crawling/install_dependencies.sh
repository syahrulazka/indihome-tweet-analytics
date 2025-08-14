#!/bin/bash

# Konfigurasi versi Node.js
NODE_MAJOR=20

echo "🚀 Mulai instalasi Python package dan Node.js..."

# Install pip package
pip install pandas

# Update dan install tools dasar
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# Setup repository Node.js 20
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | \
    sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | \
    sudo tee /etc/apt/sources.list.d/nodesource.list

# Install Node.js
sudo apt-get update
sudo apt-get install -y nodejs
echo "🟢 Node.js terpasang versi: $(node -v)"

# Install dependency Playwright
echo "🔧 Menginstal dependency Playwright..."
sudo npx playwright install-deps

echo "✅ Instalasi selesai. Siap digunakan."
