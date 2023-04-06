#!/bin/env bash
# Install Nginx if not already installed
if [ ! -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create fake HTML file
echo "<html><body><h1>Hello World!</h1></body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership of /data folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data

# Configure Nginx to serve web_static content
sudo sed -i "/^\tlocation \/ {$/ i\\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n}" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
