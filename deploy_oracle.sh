#!/bin/bash

# Oracle Cloud Django Deployment Script 
# Run this on your Oracle Cloud VM after basic setup

set -e  # Exit on any error

echo "🚀 Starting Django deployment on Oracle Cloud..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}
# 
print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as synet user
if [ "$USER" != "synet" ]; then
    print_error "This script should be run as the 'synet' user"
    print_status "Switch to synet user: sudo su - synet"
    exit 1
fi

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv git nginx mysql-server ufw
sudo apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

# Configure MySQL if not already done
print_status "Checking MySQL configuration..."
if ! sudo mysql -u root -e "SELECT 1;" 2>/dev/null; then
    print_warning "MySQL needs to be configured. Please run:"
    echo "sudo mysql_secure_installation"
    echo "Then create database and user as shown in the documentation."
    read -p "Have you configured MySQL? (y/n): " mysql_configured
    if [ "$mysql_configured" != "y" ]; then
        print_error "Please configure MySQL first"
        exit 1
    fi
fi

# Clone or update repository
if [ -d "/home/synet/synetairismos" ]; then
    print_status "Updating existing repository..."
    cd /home/synet/synetairismos
    git pull origin main
else
    print_status "Cloning repository..."
    cd /home/synet
    git clone https://github.com/gverv/synetairismos.git
    cd synetairismos
fi

# Create virtual environment
print_status "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install Python packages
print_status "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn mysqlclient

# Get Oracle Cloud VM public IP
ORACLE_IP=$(curl -s ifconfig.me)
print_status "Detected Oracle Cloud VM IP: $ORACLE_IP"

# Update Oracle settings with the IP
print_status "Updating Oracle settings..."
sed -i "s/# 'YOUR_ORACLE_VM_IP',/'$ORACLE_IP',/" synetairismos/oracle_settings.py

# Set Django settings
export DJANGO_SETTINGS_MODULE=synetairismos.oracle_settings

# Run Django setup
print_status "Running Django migrations..."
python manage.py migrate

print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser
print_warning "You need to create a Django superuser"
read -p "Create superuser now? (y/n): " create_user
if [ "$create_user" = "y" ]; then
    python manage.py createsuperuser
fi

# Create Gunicorn service
print_status "Creating Gunicorn service..."
sudo tee /etc/systemd/system/synetairismos.service > /dev/null <<EOF
[Unit]
Description=Synetairismos Django app
After=network.target

[Service]
User=synet
Group=synet
WorkingDirectory=/home/synet/synetairismos
Environment="PATH=/home/synet/synetairismos/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=synetairismos.oracle_settings"
ExecStart=/home/synet/synetairismos/venv/bin/gunicorn --workers 3 --bind unix:/home/synet/synetairismos/synetairismos.sock synetairismos.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start Gunicorn service
sudo systemctl daemon-reload
sudo systemctl enable synetairismos
sudo systemctl start synetairismos

# Check service status
if sudo systemctl is-active --quiet synetairismos; then
    print_status "Gunicorn service started successfully"
else
    print_error "Gunicorn service failed to start"
    sudo systemctl status synetairismos
    exit 1
fi

# Configure Nginx
print_status "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/synetairismos > /dev/null <<EOF
server {
    listen 80;
    server_name $ORACLE_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/synet/synetairismos;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/synet/synetairismos/synetairismos.sock;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/synetairismos /etc/nginx/sites-enabled/
sudo nginx -t

if [ $? -eq 0 ]; then
    sudo systemctl restart nginx
    print_status "Nginx configured successfully"
else
    print_error "Nginx configuration failed"
    exit 1
fi

# Configure firewall
print_status "Configuring firewall..."
if command -v ufw >/dev/null 2>&1; then
    print_status "Using UFW firewall..."
    sudo ufw --force enable
    sudo ufw allow ssh
    sudo ufw allow 'Nginx Full'
    sudo ufw status
elif command -v firewall-cmd >/dev/null 2>&1; then
    print_status "Using firewalld..."
    sudo firewall-cmd --permanent --add-service=ssh
    sudo firewall-cmd --permanent --add-service=http
    sudo firewall-cmd --permanent --add-service=https
    sudo firewall-cmd --reload
    sudo firewall-cmd --list-all
else
    print_warning "No firewall manager found (ufw/firewalld)"
    print_status "Using iptables directly..."
    
    # Allow SSH (port 22)
    sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
    
    # Allow HTTP (port 80)
    sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
    
    # Allow HTTPS (port 443)
    sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
    
    # Allow established connections
    sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    
    # Allow loopback
    sudo iptables -A INPUT -i lo -j ACCEPT
    
    # Save iptables rules (Oracle Linux/RHEL style)
    if [ -f /etc/redhat-release ]; then
        sudo service iptables save 2>/dev/null || true
    else
        # Ubuntu/Debian style
        sudo iptables-save > /etc/iptables/rules.v4 2>/dev/null || sudo mkdir -p /etc/iptables && sudo iptables-save | sudo tee /etc/iptables/rules.v4 >/dev/null
    fi
    
    print_status "iptables rules configured"
    sudo iptables -L
fi

print_status "Firewall configuration completed"

print_status "🎉 Deployment completed successfully!"
echo ""
print_status "Your Django application is now running at: http://$ORACLE_IP"
echo ""
print_status "Next steps:"
echo "1. Test your application: http://$ORACLE_IP"
echo "2. Set up a domain name (optional)"
echo "3. Configure SSL certificate: sudo certbot --nginx"
echo "4. Import your data if needed"
echo ""
print_status "Useful commands:"
echo "- Check Django service: sudo systemctl status synetairismos"
echo "- Check Nginx: sudo systemctl status nginx"
echo "- View Django logs: sudo journalctl -u synetairismos -f"
echo "- Restart services: sudo systemctl restart synetairismos nginx"
