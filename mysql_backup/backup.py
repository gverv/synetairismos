



import os
import json
import datetime
import zipfile
import dropbox
import logging

# === Φόρτωση config ===
with open("config.json") as f:
    config = json.load(f)

USERNAME = config["username"]
DBNAME = f"{USERNAME}${config['dbname']}"
HOST = config["host"]
BACKUP_DIR = config["backup_dir"]
LOG_FILE = config["log_file"]
DAYS_TO_KEEP = config["days_to_keep"]
DROPBOX_TOKEN = os.getenv(config["dropbox_token_env"])
PASSWORD = os.getenv(config["mysql_password_env"])
DROPBOX_FOLDER = config["dropbox_folder"]

# === Logging ===
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# === Δημιουργία φακέλου backup ===
os.makedirs(BACKUP_DIR, exist_ok=True)

# === Δημιουργία SQL backup ===
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sql_file = f"{BACKUP_DIR}/backup_{timestamp}.sql"
zip_file = f"{BACKUP_DIR}/backup_{timestamp}.zip"

dump_command = (
    f"mysqldump -u {USERNAME} -p'{PASSWORD}' -h {HOST} "
    f"--set-gtid-purged=OFF --no-tablespaces '{DBNAME}' > {sql_file}"
)
exit_code = os.system(dump_command)

if exit_code != 0:
    logging.error("❌ Αποτυχία δημιουργίας SQL backup.")
    exit(1)
logging.info(f"✅ Δημιουργήθηκε SQL backup: {sql_file}")

# === Συμπίεση σε zip ===
try:
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(sql_file, arcname=os.path.basename(sql_file))
    os.remove(sql_file)
    logging.info(f"✅ Συμπιέστηκε σε zip: {zip_file}")
except Exception as e:
    logging.error(f"❌ Σφάλμα κατά τη συμπίεση: {e}")
    exit(1)

# === Διαγραφή παλιών zip ===
now = datetime.datetime.now()
for filename in os.listdir(BACKUP_DIR):
    filepath = os.path.join(BACKUP_DIR, filename)
    if os.path.isfile(filepath) and filename.endswith(".zip"):
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
        if (now - file_time).days > DAYS_TO_KEEP:
            os.remove(filepath)
            logging.info(f"🗑️ Διαγράφηκε παλιό backup: {filename}")

# === Ανέβασμα στο Dropbox ===
if DROPBOX_TOKEN:
    try:
        dbx = dropbox.Dropbox(DROPBOX_TOKEN)

        # Δημιουργία φακέλου αν δεν υπάρχει
        try:
            dbx.files_get_metadata(DROPBOX_FOLDER)
        except dropbox.exceptions.ApiError:
            dbx.files_create_folder_v2(DROPBOX_FOLDER)
            logging.info(f"📁 Δημιουργήθηκε φάκελος στο Dropbox: {DROPBOX_FOLDER}")

        with open(zip_file, "rb") as f:
            dbx.files_upload(f.read(), f"{DROPBOX_FOLDER}/{os.path.basename(zip_file)}", mode=dropbox.files.WriteMode.overwrite)
        logging.info(f"☁️ Ανεβάστηκε στο Dropbox: {DROPBOX_FOLDER}/{os.path.basename(zip_file)}")
    except Exception as e:
        logging.error(f"❌ Σφάλμα Dropbox: {e}")
else:
    logging.warning("⚠️ DROPBOX_TOKEN δεν έχει οριστεί. Παράλειψη upload.")
