# Οδηγίες Μεταφοράς MySQL στο PythonAnywhere 

## Βήματα που έχουν ολοκληρωθεί:
✅ Εξαγωγή βάσης δεδομένων στο αρχείο `synetairismos_export.sql`
✅ Ενημέρωση settings.py για PythonAnywhere

## Επόμενα βήματα στο PythonAnywhere:

### 1. Clone του Git repository
Άνοιξε ένα **Bash console** στο PythonAnywhere και εκτέλεσε:

**Επιλογή 1 - Public clone (Προτεινόμενο):**
```bash
cd /home/gverv
git clone https://github.com/gverv/synetairismos.git
cd synetairismos
```

**Αν παίρνεις authentication error, δοκίμασε:**

**Επιλογή 2 - Με Personal Access Token (για private repo):**
```bash
cd /home/gverv
# Αντικατάστησε το YOUR_TOKEN με το δικό σου token από GitHub
git clone https://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@github.com/gverv/synetairismos.git
cd synetairismos
```

**Πώς να δημιουργήσεις Personal Access Token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Επίλεξε scope: `repo` (Full control of private repositories)
4. Copy το token και χρησιμοποίησέ το στη παραπάνω εντολή

**Επιλογή 3 - SSH (αν έχεις SSH key):**
```bash
cd /home/gverv
git clone git@github.com:gverv/synetairismos.git
cd synetairismos
```

**Επιλογή 4 - Download ZIP:**
Αν το Git clone δεν δουλεύει:
- Πήγαινε στο https://github.com/gverv/synetairismos
- Κάνε κλικ στο **Code** → **Download ZIP**
- Ανέβασε το ZIP στο PythonAnywhere
- Εκτέλεσε: `unzip synetairismos-main.zip && mv synetairismos-main synetairismos`

### 2. Ανέβασμα του SQL αρχείου
- Μπες στο PythonAnywhere dashboard
- Πήγαινε στο **Files** tab
- Κάνε κλικ στο **Upload a file**
- Ανέβασε το αρχείο `synetairismos_export.sql` στο `/home/gverv/`

### 2. Ανέβασμα του SQL αρχείου
- Μπες στο PythonAnywhere dashboard
- Πήγαινε στο **Files** tab
- Κάνε κλικ στο **Upload a file**
- Ανέβασε το αρχείο `synetairismos_export.sql` στο `/home/gverv/`

### 3. Εγκατάσταση Python dependencies
```bash
cd /home/gverv/synetairismos
pip3.10 install --user -r requirements.txt
# Ή αν δεν υπάρχει requirements.txt:
pip3.10 install --user django mysqlclient django-crispy-forms crispy-bootstrap4
```

### 4. Σύνδεση με τη βάση δεδομένων
Άνοιξε ένα **Bash console** στο PythonAnywhere και δοκίμασε μία από τις παρακάτω εντολές:

**Επιλογή 1 (με password στην εντολή):**
```bash
mysql -u gverv -p'pefkos@@1932' -h gverv.mysql.pythonanywhere-services.com 'gverv$synet'
```

**Επιλογή 2 (χωρίς κενά μετά το -p):**
```bash
mysql -ugverv -p'pefkos@@1932' -hgverv.mysql.pythonanywhere-services.com 'gverv$synet'
```

**Επιλογή 3 (interactive password prompt):**
```bash
mysql -u gverv -p -h gverv.mysql.pythonanywhere-services.com 'gverv$synet'
# Θα σε ρωτήσει για password - γράψε: pefkos@@1932
```

**Επιλογή 4 (με escape characters):**
```bash
mysql -u gverv -p"pefkos@@1932" -h gverv.mysql.pythonanywhere-services.com "gverv\$synet"
```

### 5. Εισαγωγή δεδομένων
Μέσα στο MySQL console:

```sql
SOURCE /home/gverv/synetairismos_export.sql;
```

### 6. Έλεγχος εισαγωγής
```sql
SHOW TABLES;
SELECT COUNT(*) FROM synet_persons;
SELECT COUNT(*) FROM synet_counters;
```

### 7. Εναλλακτικά μέσω bash (απευθείας εισαγωγή)
```bash
# Επιλογή 1:
mysql -u gverv -p'pefkos@@1932' -h gverv.mysql.pythonanywhere-services.com 'gverv$synet' < /home/gverv/synetairismos_export.sql

# Επιλογή 2:
mysql -ugverv -p'pefkos@@1932' -hgverv.mysql.pythonanywhere-services.com 'gverv$synet' < /home/gverv/synetairismos_export.sql

# Επιλογή 3 (με escape):
mysql -u gverv -p"pefkos@@1932" -h gverv.mysql.pythonanywhere-services.com "gverv\$synet" < /home/gverv/synetairismos_export.sql
```

### 8. Django migrations και έλεγχος sessions
Μετά την εισαγωγή, εκτέλεσε στο PythonAnywhere:

```bash
cd /home/gverv/synetairismos
python3.10 manage.py makemigrations
python3.10 manage.py migrate
python3.10 manage.py migrate --run-syncdb  # Για να βεβαιωθείς ότι οι πίνακες sessions υπάρχουν
python3.10 manage.py collectstatic --noinput
```

**Έλεγχος της βάσης δεδομένων:**
```bash
python3.10 manage.py shell
# Στο Django shell:
>>> from django.contrib.sessions.models import Session
>>> Session.objects.count()  # Πρέπει να επιστρέψει αριθμό (ακόμα και 0)
>>> exit()
```

### 9. Ρύθμιση Web App στο PythonAnywhere

**Βήμα 1: Δημιουργία Web App**
- Πήγαινε στο **Web** tab στο PythonAnywhere dashboard
- Αν δεν έχεις web app: **Add a new web app** → **Manual configuration** → **Python 3.10**
- Αν έχεις ήδη web app: **Delete** την παλιά και δημιούργησε νέα

**Βήμα 2: Ρύθμιση Code section**
- **Source code:** `/home/gverv/synetairismos`
- **Working directory:** `/home/gverv/synetairismos`

**Βήμα 3: Ρύθμιση WSGI configuration file**
Κάνε κλικ στο **WSGI configuration file** link και αντικατάστησε ΟΛΟ το περιεχόμενο με:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/gverv/synetairismos'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'synetairismos.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Βήμα 4: Ρύθμιση Static files**
Στο **Static files** section:
- URL: `/static/`
- Directory: `/home/gverv/synetairismos/static/`

**Βήμα 5: Ρύθμιση Virtualenv (προαιρετικό)**
Αν χρησιμοποιείς virtualenv:
- **Virtualenv:** `/home/gverv/.local`

### 10. Δοκιμή της εφαρμογής
- Ανανέωσε την web app από το Web tab
- Δοκίμασε την εφαρμογή στο https://gverv.pythonanywhere.com

## Σημείωση:
Το αρχείο settings.py είναι ήδη ρυθμισμένο για PythonAnywhere με:
- Host: gverv.mysql.pythonanywhere-services.com
- User: gverv
- Database: gverv$synet

## ⚠️ Περιορισμοί PythonAnywhere Free Account:

### Γνωστά προβλήματα:
- **Ταυτόχρονες συνδέσεις:** Μόνο 1 ενεργός χρήστης κάθε φορά
- **Session conflicts:** Νέα σύνδεση διακόπτει την προηγούμενη
- **Timeout:** Sessions λήγουν γρήγορα
- **Browser issues:** Πρόβλημα με cached sessions

### Λύσεις για Free Account:
1. **Χρήση ενός browser/device κάθε φορά**
2. **Πάντα logout όταν τελειώνεις**
3. **Clear sessions τακτικά:**
   ```bash
   python3.10 manage.py clearsessions
   ```
4. **Incognito mode για testing**
5. **Αν κολλήσει, περίμενε 5-10 λεπτά**

### Για επαγγελματική χρήση:
Upgrade σε **Paid account** για:
- Unlimited concurrent users
- Better session handling
- Faster performance
- No daily CPU limits

## 🚀 Εναλλακτικές Free Hosting Platforms:

### 1. **Railway.app** (Προτείνεται #1)
**Πλεονεκτήματα:**
- Πολλαπλοί χρήστες χωρίς περιορισμούς
- Automatic deployments από Git
- Built-in PostgreSQL/MySQL
- $5 credit κάθε μήνα (αρκετό για μικρές εφαρμογές)

**Setup:**
```bash
# Install Railway CLI
npm install -g @railway/cli
# Deploy
railway login
railway init
railway up
```

### 2. **Render.com** (Εύκολο setup)
**Πλεονεκτήματα:**
- Free tier χωρίς session περιορισμούς
- Auto-deploy από GitHub
- Free PostgreSQL database
- Custom domains

**Περιορισμοί:**
- Sleep μετά από 15 λεπτά αδράνειας
- 750 ώρες/μήνα

### 3. **Fly.io** (Σύγχρονο)
**Πλεονεκτήματα:**
- Καλή free tier
- Global deployment
- Postgres included
- Docker-based

**Setup:**
```bash
# Install flyctl
flyctl deploy
```

### 4. **Vercel** (Για Serverless)
**Πλεονεκτήματα:**
- Unlimited users
- Fast CDN
- Easy GitHub integration

**Μειονεκτήματα:**
- Χρειάζεται αλλαγές για serverless
- Καλύτερο για Next.js

### 5. **Heroku** (Κλασικό - Πληρωμένο πλέον)
**Σημείωση:** Το Heroku κατάργησε το free tier το 2022

### 6. **DigitalOcean App Platform**
**Πλεονεκτήματα:**
- $200 credit για νέους λογαριασμούς
- Professional grade
- Easy scaling

### 7. **Google Cloud Run** 
**Πλεονεκτήματα:**
- Generous free tier
- Pay per use
- Auto-scaling
- $300 credit για νέους λογαριασμούς

### 8. **Oracle Cloud Always Free**
**Πλεονεκτήματα:**
- Πραγματικά always free
- 2 VMs + databases
- Πλήρης έλεγχος

**Μειονεκτήματα:**
- Πιο περίπλοκο setup
- Manual configuration

## 📋 Σύγκριση για τη δική σου εφαρμογή:

| Platform | Free Tier | Multiple Users | Database | Auto Deploy | Difficulty |
|----------|-----------|----------------|----------|-------------|------------|
| Railway | $5/month credit | ✅ | ✅ MySQL/Postgres | ✅ | 🟢 Easy |
| Render | 750h/month | ✅ | ✅ Postgres | ✅ | 🟢 Easy |
| Fly.io | Good limits | ✅ | ✅ Postgres | ✅ | 🟡 Medium |
| PythonAnywhere | Basic | ❌ (1 user) | ✅ MySQL | ❌ | 🟢 Easy |
| Google Cloud | $300 credit | ✅ | ✅ Cloud SQL | 🟡 | 🔴 Hard |
| Oracle Cloud | Always Free | ✅ | ✅ | ❌ | 🔴 Hard |

## 🎯 Προτεινόμενη λύση: **Railway.app**

**Γιατί Railway:**
- Πολύ εύκολο deployment
- Support για MySQL (σαν PythonAnywhere)
- Git integration
- Καλό free tier
- Χωρίς session περιορισμούς

**Quick start για Railway:**
1. Push το project στο GitHub
2. Πήγαινε στο railway.app
3. "Deploy from GitHub repo"
4. Επίλεξε το synetairismos repo
5. Προσθήκη MySQL service
6. Set environment variables
7. Deploy!

## Troubleshooting Authentication Issues:

### Αν βλέπεις την αρχική σελίδα Django αντί για την εφαρμογή σου:

**Πρόβλημα:** Το PythonAnywhere δείχνει "The install worked successfully! Congratulations!" αντί για την εφαρμογή σου.

**Λύση:**

1. **Έλεγξε το WSGI configuration file:**
   - Web tab → WSGI configuration file
   - Πρέπει να περιέχει τον σωστό path προς το project σου
   - Αντικατάστησε το περιεχόμενο με τον κώδικα από το Βήμα 3 παραπάνω

2. **Έλεγξε τα paths:**
   ```bash
   # Στο Bash console:
   cd /home/gverv/synetairismos
   ls -la  # Πρέπει να βλέπεις το manage.py
   python3.10 manage.py check  # Έλεγχος για errors
   ```

3. **Έλεγξε το settings.py:**
   ```bash
   cd /home/gverv/synetairismos
   python3.10 -c "import synetairismos.settings; print('Settings OK')"
   ```

4. **Ρύθμισε το ALLOWED_HOSTS στο settings.py:**
   Προσθήκη στο settings.py:
   ```python
   ALLOWED_HOSTS = ['gverv.pythonanywhere.com', 'localhost', '127.0.0.1']
   ```

5. **Reload την Web App:**
   - Web tab → **Reload** button
   - Περίμενε να ολοκληρωθεί το reload

6. **Έλεγξε τα error logs:**
   - Web tab → **Error log**
   - Αν υπάρχουν errors, διόρθωσέ τα και κάνε reload

### Αν παίρνεις "SessionInterrupted" error:

**Αιτία:** Περιορισμοί του PythonAnywhere FREE account στις ταυτόχρονες συνδέσεις.

**Άμεσες λύσεις:**

1. **Καθαρισμός όλων των sessions:**
   ```bash
   cd /home/gverv/synetairismos
   python3.10 manage.py shell
   # Στο Django shell:
   >>> from django.contrib.sessions.models import Session
   >>> Session.objects.all().delete()
   >>> exit()
   ```

2. **Καθαρισμός sessions με command:**
   ```bash
   python3.10 manage.py clearsessions
   ```

3. **Δημιουργία superuser για τεστ:**
   ```bash
   python3.10 manage.py createsuperuser
   # Δώσε: username, email, password
   ```

4. **Restart της web app:**
   - Web tab → **Reload** button
   - Περίμενε 30 δευτερόλεπτα

5. **Χρήση incognito/private browser:**
   - Άνοιξε την εφαρμογή σε incognito mode
   - Καθάρισε cookies αν χρειάζεται

**Για Free Account - Καλές πρακτικές:**

- Χρησιμοποίησε μόνο έναν browser/tab κάθε φορά
- Κάνε logout όταν τελειώνεις
- Αν κολλήσει, περίμενε 5-10 λεπτά πριν ξαναδοκιμάσεις
- Κάνε clear sessions τακτικά

**Έλεγχος sessions:**
```bash
python3.10 manage.py shell
>>> from django.contrib.sessions.models import Session
>>> print(f"Active sessions: {Session.objects.count()}")
>>> exit()
```

### Αν παίρνεις "Access denied" error:

1. **Έλεγξε τα στοιχεία σύνδεσης:**
   - Username: `gverv` (όχι `gverv$synet`)
   - Password: `pefkos@@1932`
   - Host: `gverv.mysql.pythonanywhere-services.com`
   - Database: `gverv$synet`

2. **Δοκίμασε στο PythonAnywhere MySQL console:**
   - Πήγαινε στο **Databases** tab στο dashboard
   - Κάνε κλικ στο **Open MySQL console**
   - Αυτό θα σε συνδέσει αυτόματα χωρίς authentication

3. **Χρησιμοποίησε το database name με escape:**
   ```bash
   mysql -u gverv -p -h gverv.mysql.pythonanywhere-services.com
   # Μετά τη σύνδεση:
   USE `gverv$synet`;
   ```

4. **Έλεγξε αν η βάση υπάρχει:**
   ```sql
   SHOW DATABASES;
   ```

## Troubleshooting Git Clone Issues:

### Για private repository - Git Authentication στο PythonAnywhere:

**Καλύτερη λύση - Personal Access Token:**

1. **Δημιούργησε Personal Access Token:**
   - GitHub → Settings (profile) → Developer settings
   - Personal access tokens → Tokens (classic)
   - Generate new token (classic)
   - Scope: τσέκαρε `repo` (Full control of private repositories)
   - Copy το token

2. **Clone με το token:**
   ```bash
   cd /home/gverv
   git clone https://YOUR_GITHUB_TOKEN@github.com/gverv/synetairismos.git
   cd synetairismos
   ```

**Εναλλακτικές λύσεις:**

1. **Κάνε το repository public προσωρινά:**
   - GitHub → Repository Settings → Danger Zone
   - Change visibility → Make public
   - Κάνε το clone στο PythonAnywhere
   - Κάνε το ξανά private

2. **SSH Keys (πιο περίπλοκο):**
   ```bash
   # Δημιουργία SSH key στο PythonAnywhere
   ssh-keygen -t ed25519 -C "your-email@example.com"
   cat ~/.ssh/id_ed25519.pub  # Copy αυτό στο GitHub SSH keys
   git clone git@github.com:gverv/synetairismos.git
   ```

3. **Download ZIP method:**
   - GitHub → Code → Download ZIP
   - Upload στο PythonAnywhere Files
   - `unzip synetairismos-main.zip && mv synetairismos-main synetairismos`

4. **Upload μεμονωμένα αρχεία:**
   - Upload όλα τα αρχεία του project μέσω Files tab
   - Δημιούργησε τη δομή φακέλων χειροκίνητα
