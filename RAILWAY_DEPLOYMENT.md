# Railway.app Deployment Guide 

## Γιατί Railway;
- ✅ Πολλαπλοί χρήστες χωρίς περιορισμούς
- ✅ MySQL database included
- ✅ Auto-deploy από GitHub
- ✅ $5 credit κάθε μήνα (αρκετό για την εφαρμογή)
- ✅ Custom domains
- ✅ HTTPS by default

## Βήμα προς βήμα deployment:

### 1. Προετοιμασία του project

**Δημιουργία railway.json:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn synetairismos.wsgi:application --bind 0.0.0.0:$PORT",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
```

**Προσθήκη στο requirements.txt:**
```txt
asgiref==3.8.1
crispy-bootstrap4==2024.10
Django==5.2
django-crispy-forms==2.4
mysqlclient==2.2.7
sqlparse==0.5.3
tzdata==2025.2
gunicorn==21.2.0
whitenoise==6.6.0
```

**Ενημέρωση settings.py για Railway:**
```python
import os

# Railway specific settings
DEBUG = os.environ.get('RAILWAY_ENVIRONMENT') != 'production'

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '.railway.app',  # Railway domains
    'gverv.pythonanywhere.com'  # Keep existing
]

# Database configuration for Railway
if 'DATABASE_URL' in os.environ:
    # Railway MySQL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    # Existing PythonAnywhere config
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'gverv$synet',
            'USER': 'gverv',
            'PASSWORD': 'pefkos@@1932',
            'HOST': 'gverv.mysql.pythonanywhere-services.com',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# Static files for Railway
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'synet.middleware.LoginRequiredMiddleware',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 2. Deployment στο Railway

**Βήμα 1: Σύνδεση με Railway**
1. Πήγαινε στο https://railway.app
2. Sign up με GitHub account
3. "New Project" → "Deploy from GitHub repo"
4. Επίλεξε το `synetairismos` repository

**Βήμα 2: Προσθήκη MySQL Service**
1. Στο Railway dashboard → "Add Service"
2. Επίλεξε "MySQL"
3. Deploy το MySQL service

**Βήμα 3: Ρύθμιση Environment Variables**
Στο Django service → Settings → Variables:
```
DJANGO_SETTINGS_MODULE=synetairismos.settings
RAILWAY_ENVIRONMENT=production
```

**Βήμα 4: Connect Database**
1. Railway θα δημιουργήσει αυτόματα το `DATABASE_URL`
2. Verify ότι το Django service βλέπει το MySQL

**Βήμα 5: Deploy**
1. Railway θα κάνει auto-deploy
2. Θα δεις το URL της εφαρμογής

### 3. Μεταφορά δεδομένων

**Εξαγωγή από PythonAnywhere:**
```bash
# Στο PythonAnywhere
mysqldump -u gverv -p'pefkos@@1932' -h gverv.mysql.pythonanywhere-services.com 'gverv$synet' > railway_export.sql
```

**Εισαγωγή στο Railway:**
```bash
# Local με Railway CLI
railway login
railway connect
mysql -u root -p$MYSQLPASSWORD -h $MYSQLHOST -P $MYSQLPORT $MYSQLDATABASE < railway_export.sql
```

**Ή μέσω Railway dashboard:**
1. Railway → MySQL service → Connect
2. Use οποιοδήποτε MySQL client
3. Import το SQL file

### 4. Final steps

**Δημιουργία superuser:**
```bash
railway run python manage.py createsuperuser
```

**Test η εφαρμογή:**
1. Πήγαινε στο Railway URL
2. Test login/logout
3. Test multiple users

## Κόστος:
- **Free:** $5 credit κάθε μήνα
- **Estimated usage:** ~$2-3/μήνα για τη δική σου εφαρμογή
- **Αποτέλεσμα:** 1-2 μήνες δωρεάν, μετά ~$3/μήνα

## Πλεονεκτήματα έναντι PythonAnywhere Free:
- ✅ Unlimited concurrent users
- ✅ No session conflicts
- ✅ Better performance
- ✅ Auto-deploy from Git
- ✅ Professional URLs
- ✅ Better monitoring
- ✅ Scaling options

## Support:
- Railway documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Tutorial videos: YouTube "Railway app deployment"
