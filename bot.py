from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from cryptography.fernet import Fernet
import json
import os

TOKEN = "ISI_TOKEN_KAMU"
OWNER_ID = 123456789  # GANTI DENGAN ID TELEGRAM KAMU

# ===== ENCRYPTION =====
KEY_FILE = "key.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

cipher = Fernet(load_key())

# ===== DATABASE =====
DB_FILE = "data.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# ===== SECURITY CHECK =====
def is_owner(update: Update):
    return update.effective_user.id == OWNER_ID

# ===== COMMAND =====
async def set_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    try:
        service = context.args[0]
        username = context.args[1]
        password = context.args[2]

        encrypted = cipher.encrypt(password.encode()).decode()

        db = load_db()
        db[service] = {"username": username, "password": encrypted}
        save_db(db)

        await update.message.reply_text(f"✅ {service} disimpan!")

    except:
        await update.message.reply_text("Format:\n/set shopee user pass")

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    try:
        service = context.args[0]
        db = load_db()

        if service not in db:
            await update.message.reply_text("❌ Tidak ditemukan")
            return

        username = db[service]["username"]
        password = cipher.decrypt(db[service]["password"].encode()).decode()

        await update.message.reply_text(
            f"🔐 {service}\n👤 {username}\n🔑 {password}"
        )

    except:
        await update.message.reply_text("Format:\n/password shopee")

# ===== RUN =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("set", set_password))
app.add_handler(CommandHandler("password", get_password))

app.run_polling()
