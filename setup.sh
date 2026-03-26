#!/bin/bash
# Ensure local Python bin is on PATH
export PATH="$PATH:/home/codespace/.local/bin"
echo "🔧 Setting up Marine Troubleshooter environment..."

sudo apt update -y
sudo apt install -y python3 python3-pip

python3 -m pip install --upgrade pip
python3 -m pip install "fastapi[standard]" uvicorn openai python-multipart

echo "✅ Installation complete."
