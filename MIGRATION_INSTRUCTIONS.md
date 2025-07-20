# Οδηγίες Μεταφοράς MySQL στο PythonAnywhere

## Βήματα που έχουν ολοκληρωθεί:
✅ Εξαγωγή βάσης δεδομένων στο αρχείο `synetairismos_export.sql`
✅ Ενημέρωση settings.py για PythonAnywhere

## Επόμενα βήματα στο PythonAnywhere:

### 1. Clone του Git repository
Άνοιξε ένα **Bash console** στο PythonAnywhere και εκτέλεσε:

```bash
cd /home/gverv
git clone https://github.com/gverv/synetairismos.git
cd synetairismos
```

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
Άνοιξε ένα **Bash console** στο PythonAnywhere και εκτέλεσε:

```bash
mysql -u gverv -p'pefkos@@1932' -h gverv.mysql.pythonanywhere-services.com 'gverv$synet'
```

### 4. Σύνδεση με τη βάση δεδομένων
Στο **Bash console**:

```bash
mysql -u gverv -p'pefkos@@1932' -h gverv.mysql.pythonanywhere-services.com 'gverv$synet'
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

### 7. Εναλλακτικά μέσω bash
```bash
mysql -u gverv -p'pefkos@@1932' -h gverv.mysql.pythonanywhere-services.com 'gverv$synet' < /home/gverv/synetairismos_export.sql
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
