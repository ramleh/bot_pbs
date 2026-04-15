from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime

# =========================
# DATA
# =========================
data_user = {}
user_daily = {}
user_monthly = {}
user_step = {}
user_temp = {}
user_page = {}

# =========================
# DATA BOBOT
# =========================
bobot_data = {
    "HSI Indihome Reseller": 2,
    "Tangible": 1,
    "Tiket Datin Kategori 1": 2.67,
    "Tiket Datin Kategori 2": 2.67,
    "Tiket Datin Kategori 3": 2.67,
    "Tiket HSI Indibiz": 2,
    "Tiket NodeB CNQ (Preventive/Quality)": 4,
    "Tiket NodeB Critical": 6,
    "Tiket NodeB Low": 4,
    "Tiket NodeB Major": 4,
    "Tiket NodeB Minor": 4,
    "Tiket NodeB Premium": 6,
    "Tiket NodeB Premium Preventive": 4,
    "Tiket OLO Datin Gamas": 4,
    "Tiket OLO Datin Non Gamas": 4,
    "Tiket OLO Datin Quality": 4,
    "Tiket OLO SL WDM": 4,
    "Tiket OLO SL WDM Quality": 4,
    "Tiket Pra SQM Gaul HSI": 2,
    "Tiket SIP Trunk": 2.67,
    "Tiket SQM Datin": 2.67,
    "Tiket SQM HSI": 2,
    "Tiket WIFI ID": 2.67,
    "Tiket Wifi Logic": 2.67,
    "Preventive SPBU": 8,
    "Inventory SPBU": 4,
    "Unspec DATIN": 2.67,
    "Unspec HSI": 2,
    "Unspec SITE": 0,
    "Unspec WIFI": 0,
    "PSB OLO": 0,
    "PSB WIFI": 0,
    "PSB DATIN": 0,
    "Aktivasi/Migrasi/Dismantel Digiserve": 4,
    "Corrective Akses Tower Lintasarta": 4,
    "Corrective Digiserve": 4,
    "Corrective MMP": 4,
    "Corrective SPBU": 4,
    "Corrective Tower TIS": 4,
    "Preventif MMP": 2,
    "Preventive Akses Tower Lintasarta": 2,
    "Preventive Tower TIS": 4,
    "Relokasi Digiserve": 1,
    "SPPG": 8,
    "Corrective IBU - FTTR": 5,
    "Corrective Mitratel": 4,
    "Lapsung (Laporan Langsung)": 4,
    "Patroli Akses": 4,
    "SQM Reguler": 4,
    "Tangible ODP": 0,
    "Tiket GAMAS": 0,
    "Tiket Reguler": 0,
    "Unspec Reguler": 0,
    "Validasi Tiang": 0,
    "Valins FTM": 0,
    "Valins ODC": 0,
    "Valins Reguler": 0,
    "Instalasi IP Camera": 0,
    "Instalasi SD-WAN": 0,
    "Instalasi Router": 0,
    "Install AP WIFI (1 AP)": 0,
    "Install AP WIFI (2 AP)": 0,
    "Install AP WIFI(3 AP)": 0,
    "Install AP WIFI (4 AP)": 0,
    "Pembuatan BAI (Satkomindo,BRI MPLS)": 0,
    "Pasang Baru Indihome": 0
}

# =========================
# MAPPING KATEGORI → ORDER
# =========================
kategori_order = {
    "Assurance B2B Internal": [
        "HSI Indihome Reseller", "Tangible", "Tiket Datin Kategori 1", "Tiket Datin Kategori 2",
        "Tiket Datin Kategori 3", "Tiket HSI Indibiz", "Tiket NodeB CNQ (Preventive/Quality)",
        "Tiket NodeB Critical", "Tiket NodeB Low", "Tiket NodeB Major", "Tiket NodeB Minor",
        "Tiket NodeB Premium", "Tiket NodeB Premium Preventive", "Tiket OLO Datin Gamas",
        "Tiket OLO Datin Non Gamas", "Tiket OLO Datin Quality", "Tiket OLO SL WDM",
        "Tiket OLO SL WDM Quality", "Tiket Pra SQM Gaul HSI", "Tiket SIP Trunk",
        "Tiket SQM Datin", "Tiket SQM HSI", "Tiket WIFI ID", "Tiket Wifi Logic",
        "Preventive SPBU", "Inventory SPBU", "Unspec DATIN", "Unspec HSI",
        "Unspec SITE", "Unspec WIFI", "PSB OLO", "PSB WIFI", "PSB DATIN"
    ],
    "Assurance B2B External": [
        "Aktivasi/Migrasi/Dismantel Digiserve", "Corrective Akses Tower Lintasarta",
        "Corrective Digiserve", "Corrective MMP", "Corrective SPBU", "Corrective Tower TIS",
        "Preventif MMP", "Preventive Akses Tower Lintasarta", "Preventive Tower TIS",
        "Relokasi Digiserve", "SPPG", "Corrective IBU - FTTR", "Corrective Mitratel"
    ],
    "Assurance B2C": [
        "Lapsung (Laporan Langsung)", "Patroli Akses", "SQM Reguler", "Tangible ODP",
        "Tiket GAMAS", "Tiket Reguler", "Unspec Reguler", "Validasi Tiang",
        "Valins FTM", "Valins ODC", "Valins Reguler"
    ],
    "Provisioning B2B Internal": ["PSB DATIN", "PSB OLO", "PSB WIFI"],
    "Provisioning B2B External": [
        "Instalasi IP Camera", "Instalasi SD-WAN", "Instalasi Router",
        "Install AP WIFI (1 AP)", "Install AP WIFI (2 AP)", "Install AP WIFI(3 AP)",
        "Install AP WIFI (4 AP)", "Pembuatan BAI (Satkomindo,BRI MPLS)"
    ],
    "Provisioning B2C": ["Pasang Baru Indihome"]
}

# =========================
# KEYBOARD INLINE
# =========================
def get_order_keyboard(page=0, per_page=10, kat=None):
    orders = kategori_order.get(kat, [])
    start = page * per_page
    end = start + per_page
    keyboard = []
    for o in orders[start:end]:
        keyboard.append([InlineKeyboardButton(o, callback_data=f"order|{o}")])
    nav = []
    if start > 0:
        nav.append(InlineKeyboardButton("⬅️ Back", callback_data="back"))
    if end < len(orders):
        nav.append(InlineKeyboardButton("➡️ Next", callback_data="next"))
    if nav:
        keyboard.append(nav)
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nama = update.effective_user.first_name
    data_user[user_id] = nama
    user_page[user_id] = 0

    keyboard = [
        [InlineKeyboardButton("Assurance B2B External", callback_data="kategori|Assurance B2B External")],
        [InlineKeyboardButton("Assurance B2B Internal", callback_data="kategori|Assurance B2B Internal")],
        [InlineKeyboardButton("Assurance B2C", callback_data="kategori|Assurance B2C")],
        [InlineKeyboardButton("Provisioning B2B External", callback_data="kategori|Provisioning B2B External")],
        [InlineKeyboardButton("Provisioning B2B Internal", callback_data="kategori|Provisioning B2B Internal")],
        [InlineKeyboardButton("Provisioning B2C", callback_data="kategori|Provisioning B2C")]
    ]
    await update.message.reply_text(f"Hallo {nama} 👋\nSilahkan pilih Kategori:", reply_markup=InlineKeyboardMarkup(keyboard))

# =========================
# BUTTON HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data.startswith("kategori|"):
        kat = data.split("|")[1]
        user_temp[user_id] = {"kategori": kat}  # simpan kategori
        user_page[user_id] = 0
        await query.message.reply_text("Pilih order:", reply_markup=get_order_keyboard(page=0, kat=kat))
        return

    if data == "next":
        user_page[user_id] += 1
        kat = user_temp[user_id]["kategori"]
        await query.edit_message_reply_markup(reply_markup=get_order_keyboard(page=user_page[user_id], kat=kat))
        return

    if data == "back":
        user_page[user_id] -= 1
        kat = user_temp[user_id]["kategori"]
        await query.edit_message_reply_markup(reply_markup=get_order_keyboard(page=user_page[user_id], kat=kat))
        return

    if data.startswith("order|"):
        order = data.split("|")[1]
        user_temp[user_id]["order"] = order
        user_step[user_id] = "input_tiket"
        await query.message.reply_text("🎫 Input nomor tiket:")
        return

# =========================
# HANDLE TEXT
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    step = user_step.get(user_id)

    if step == "input_tiket":
        order = user_temp[user_id]["order"]
        user_temp[user_id]["nomor_tiket"] = text
        user_step[user_id] = "input_teknisi"
        await update.message.reply_text("👷 Input jumlah teknisi:")
        return

    if step == "input_teknisi":
        try:
            jumlah = int(text)
        except:
            await update.message.reply_text("⚠️ Harap input angka jumlah teknisi.")
            return
        order = user_temp[user_id]["order"]
        bobot = bobot_data.get(order, 0)
        user_temp[user_id]["jumlah_teknisi"] = jumlah

        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")
        user_daily.setdefault(user_id, {}).setdefault(today, 0)
        user_monthly.setdefault(user_id, {}).setdefault(month, 0)

        user_daily[user_id][today] += bobot
        user_monthly[user_id][month] += bobot

        user_step[user_id] = None

        per_teknisi = bobot / jumlah if jumlah > 0 else bobot

        await update.message.reply_text(
            f"✅ {order}\n🎫 Tiket: {user_temp[user_id]['nomor_tiket']}\n"
            f"👷 Jumlah teknisi: {jumlah}\n"
            f"📊 Bobot total: {bobot} → per teknisi: {per_teknisi:.2f}"
        )
        return

# =========================
# INFO
# =========================
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%Y-%m")

    text = "No | Nama | Hari ini | Bulan ini\n"
    for i, (uid, nama) in enumerate(data_user.items(), 1):
        total_hari = user_daily.get(uid, {}).get(today, 0)
        total_bulan = user_monthly.get(uid, {}).get(month, 0)
        jumlah_teknisi = user_temp.get(uid, {}).get("jumlah_teknisi", 1)
        per_teknisi_hari = total_hari / jumlah_teknisi
        per_teknisi_bulan = total_bulan / jumlah_teknisi
        text += f"{i} | {nama} | {per_teknisi_hari:.2f} | {per_teknisi_bulan:.2f}\n"

    await update.message.reply_text(text)

# =========================
# MAIN
# =========================
import os

def main():
    TOKEN = os.getenv("TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot jalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
