# Oracle Cloud Always Free - Django Deployment Guide

## Γιατί Oracle Cloud Always Free;
- ✅ **Πραγματικά ALWAYS FREE** (όχι trial)
- ✅ 2 AMD VMs (1/8 OCPU, 1 GB RAM each)
- ✅ 1 ARM VM (4 OCPUs, 24 GB RAM) - Αρκετό για πολλές εφαρμογές!
- ✅ 200 GB Block Storage
- ✅ MySQL Database (20 GB)
- ✅ Load Balancer
- ✅ Unlimited bandwidth (10 TB outbound/month)
- ✅ **Πλήρης έλεγχος** του server
- ✅ **Χωρίς περιορισμούς** χρηστών/sessions

## Προαπαιτούμενα:
- Credit/Debit card (για verification - ΔΕΝ χρεώνεται)
- Υπομονή για setup (πιο περίπλοκο από Railway)

## Βήμα προς βήμα setup:

### 1. Δημιουργία Oracle Cloud Account

1. **Πήγαινε στο:** https://www.oracle.com/cloud/free/
2. **Sign Up** → "Start for free"
3. **Country/Territory:** Greece
4. **Προσωπικά στοιχεία:** Συμπλήρωσε με πραγματικά στοιχεία
5. **Verification:** 
   - Phone verification
   - Credit card verification (ΔΕΝ χρεώνεται)
6. **Wait for approval** (μπορεί να πάρει 24-48 ώρες)

### 2. Δημιουργία Virtual Machine

**Μόλις ενεργοποιηθεί ο λογαριασμός:**

1. **Login** στο Oracle Cloud Console
2. **Hamburger Menu** → **Compute** → **Instances**
3. **Create Instance**

**Instance Configuration:**
```
Name: django-synetairismos
Placement: 
  - Availability Domain: AD-1 (ή όποιο διαθέσιμο)
  - Fault Domain: Leave default

Image: 
  - Ubuntu 22.04 LTS (Canonical)
  
Shape:
  - VM.Standard.A1.Flex (ARM - ΠΡΟΤΕΙΝΟΜΕΝΟ)
  - OCPUs: 2 (από τα 4 διαθέσιμα)
  - Memory: 12 GB (από τα 24 διαθέσιμα)
  
  ΣΤ: Αν δεν είναι διαθέσιμο ARM, επίλεξε:
  - VM.Standard.E2.1.Micro (AMD - Always Free)

Boot Volume: 50 GB (από τα 200 διαθέσιμα)

Networking:
  - Create new VCN: synet-vcn
  - Create new subnet: public subnet
  - Assign public IP: Yes
```

4. **SSH Keys:**
   ```bash
   # Στο Windows (PowerShell)
   ssh-keygen -t rsa -b 4096 -f oracle_key
   # Upload το oracle_key.pub
   ```

5. **Create Instance**

### 3. Ρύθμιση Security Rules

**Allow HTTP/HTTPS traffic:**

1. **VCN Details** → **Security Lists** → **Default Security List**
2. **Add Ingress Rules:**

```
Rule 1 - HTTP:
Source: 0.0.0.0/0
Protocol: TCP
Destination Port: 80

Rule 2 - HTTPS:
Source: 0.0.0.0/0
Protocol: TCP
Destination Port: 443

Rule 3 - Django Dev:
Source: 0.0.0.0/0
Protocol: TCP
Destination Port: 8000
```

### 4. Σύνδεση και βασική ρύθμιση του VM

**SSH Connection:**
```bash
ssh -i oracle_key ubuntu@<PUBLIC_IP>
```

**Initial Setup:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y python3 python3-pip python3-venv git nginx mysql-server

# Install Python packages
sudo apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

# Create user for the app
sudo adduser synet
sudo usermod -aG sudo synet

# Switch to app user
sudo su - synet
```

### 5. Ρύθμιση MySQL Database

```bash
# Start MySQL and secure it
sudo systemctl start mysql
sudo systemctl enable mysql
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p
```

**MySQL Commands:**
```sql
CREATE DATABASE synet_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'synet_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON synet_db.* TO 'synet_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 6. Deploy Django Application

**Clone and setup:**
```bash
# As synet user
cd /home/synet
git clone https://github.com/gverv/synetairismos.git
cd synetairismos

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
pip install gunicorn mysqlclient
```

**Create Oracle-specific settings.py:**
```python
# oracle_settings.py (create new file)
from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['<YOUR_ORACLE_VM_IP>', 'your-domain.com', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'synet_db',
        'USER': 'synet_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

STATIC_ROOT = '/home/synet/synetairismos/staticfiles/'
STATIC_URL = '/static/'

# Security settings
SECURE_SSL_REDIRECT = False  # Set True when you add SSL
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

**Setup Django:**
```bash
# Set settings module
export DJANGO_SETTINGS_MODULE=synetairismos.oracle_settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 7. Import existing data (αν έχεις)

**From PythonAnywhere export:**
```bash
# Copy το synetairismos_export.sql στον Oracle server
scp -i oracle_key synetairismos_export.sql ubuntu@<PUBLIC_IP>:/tmp/

# On Oracle server
mysql -u synet_user -p synet_db < /tmp/synetairismos_export.sql
```

### 8. Configure Gunicorn

**Create gunicorn service:**
```bash
sudo nano /etc/systemd/system/synetairismos.service
```

**Service file content:**
```ini
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
```

**Enable and start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable synetairismos
sudo systemctl start synetairismos
sudo systemctl status synetairismos
```

### 9. Configure Nginx

**Create Nginx config:**
```bash
sudo nano /etc/nginx/sites-available/synetairismos
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name <YOUR_ORACLE_VM_IP> your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/synet/synetairismos;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/synet/synetairismos/synetairismos.sock;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/synetairismos /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. Firewall setup

```bash
# Enable UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw status
```

### 11. SSL Certificate (Optional but recommended)

**Using Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 12. Monitoring and Maintenance

**Useful commands:**
```bash
# Check Django service
sudo systemctl status synetairismos

# Check Nginx
sudo systemctl status nginx

# Check logs
sudo journalctl -u synetairismos -f

# Django logs
tail -f /home/synet/synetairismos/debug.log

# Update application
cd /home/synet/synetairismos
git pull origin main
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart synetairismos
```

## Πλεονεκτήματα Oracle Cloud:

### Τεχνικά:
- ✅ **Full root access**
- ✅ **Unlimited users/sessions**
- ✅ **Custom domains**
- ✅ **SSL certificates**
- ✅ **Backup solutions**
- ✅ **Monitoring tools**

### Οικονομικά:
- ✅ **Always Free** (όχι trial)
- ✅ **Χωρίς χρεώσεις** ποτέ
- ✅ **Professional grade** hosting

### Scalability:
- ✅ **Load balancers**
- ✅ **Multiple VMs**
- ✅ **Database scaling**
- ✅ **CDN integration**

## Μειονεκτήματα:

- ❌ **Περίπλοκο setup** (1-2 ημέρες)
- ❌ **Χρειάζεται Linux γνώσεις**
- ❌ **Manual maintenance**
- ❌ **Approval process** (24-48 ώρες)

## Κόστος:
- **Always Free:** $0/μήνα για πάντα
- **Upgrade options:** Διαθέσιμες αν χρειαστείς περισσότερους πόρους

## Σύγκριση με άλλες λύσεις:

| Χαρακτηριστικό | Oracle Free | Railway | PythonAnywhere Free |
|---------------|-------------|---------|-------------------|
| Κόστος | $0 forever | $3/μήνα | $0 (περιορισμένο) |
| Users | Unlimited | Unlimited | 1 concurrent |
| Database | MySQL 20GB | MySQL included | MySQL 512MB |
| RAM | 12-24GB | ~500MB | Limited |
| Storage | 200GB | Limited | 512MB |
| Bandwidth | 10TB/month | Limited | 100MB/day |
| Setup Difficulty | Hard | Easy | Easy |
| Control | Full | Limited | Limited |

## Troubleshooting:

### "Always Free" resources not available:
- Δοκίμασε διαφορετική περιοχή (region)
- Περίμενε λίγες ώρες και ξαναδοκίμασε
- Contact Oracle support

### VM creation fails:
- Επιβεβαίωσε ότι ο λογαριασμός είναι verified
- Δοκίμασε AMD instance αντί ARM
- Check service limits

### Application errors:
```bash
# Check Django
sudo systemctl status synetairismos
sudo journalctl -u synetairismos

# Check Nginx
sudo nginx -t
sudo systemctl status nginx

# Check database
mysql -u synet_user -p synet_db
```

## Support:
- Oracle Cloud Documentation: https://docs.oracle.com/en-us/iaas/
- Oracle Cloud Forums: https://community.oracle.com/
- YouTube: "Oracle Cloud Always Free tutorial"

## Βήμα-βήμα video tutorials:
1. "Oracle Cloud Always Free Account Setup"
2. "Deploy Django on Oracle Cloud"
3. "Oracle Cloud VM Ubuntu setup"

**Αυτή είναι η καλύτερα μακροπρόθεσμη λύση για δωρεάν hosting!** 🚀
