#!/bin/bash

# sudo apt update
# sudo apt install dos2unix -y
# dos2unix setup.sh


# Exit immediately if a command exits with a non-zero status
set -e

# Update package list
echo "Updating packages..."
sudo apt-get update -y

# Install AWS CLI
echo "Installing AWS CLI..."
sudo apt-get install -y unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version

# Install Docker
echo "Installing Docker..."
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# Add Docker repository
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update -y
sudo apt-get install -y docker-ce

# Start and enable Docker
echo "Starting Docker..."
sudo systemctl start docker
sudo systemctl enable docker

# Add current user to Docker group (optional: avoid sudo)
sudo usermod -aG docker $USER

# Cleanup
rm -rf awscliv2.zip aws

echo "Installation complete! You may need to log out and log back in to use Docker without sudo."
