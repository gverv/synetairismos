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
git clone https://YOUR_TOKEN@github.com/gverv/synetairismos.git
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

### 8. Django migrations
Μετά την εισαγωγή, εκτέλεσε στο PythonAnywhere:

```bash
cd /home/gverv/synetairismos
python3.10 manage.py makemigrations
python3.10 manage.py migrate
python3.10 manage.py collectstatic
```

### 9. Ρύθμιση Web App στο PythonAnywhere
- Πήγαινε στο **Web** tab
- Δημιούργησε νέα web app (Django)
- Στο **Code** section:
  - Source code: `/home/gverv/synetairismos`
  - Working directory: `/home/gverv/synetairismos`
- Στο **WSGI configuration file** ενημέρωσε το path προς το project

### 10. Δοκιμή της εφαρμογής
- Ανανέωσε την web app από το Web tab
- Δοκίμασε την εφαρμογή στο https://gverv.pythonanywhere.com

## Σημείωση:
Το αρχείο settings.py είναι ήδη ρυθμισμένο για PythonAnywhere με:
- Host: gverv.mysql.pythonanywhere-services.com
- User: gverv
- Database: gverv$synet

## Troubleshooting Authentication Issues:

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
