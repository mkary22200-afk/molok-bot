import os, sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
CASH = "01110768571"

conn = sqlite3.connect("data.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, bal REAL DEFAULT 0)")
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    cur.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (uid,))
    conn.commit()
    cur.execute("SELECT bal FROM users WHERE id=?", (uid,))
    bal = cur.fetchone()[0]
    kb = [[InlineKeyboardButton(f"💳 رصيدك: {bal} جنيه", callback_data="x")],
          [InlineKeyboardButton("💳 اضافة رصيد فودافون كاش", callback_data="add")],
          [InlineKeyboardButton("الدعم @Koko00228", url="https://t.me/Koko00228")]]
    await update.message.reply_text(f"👑 ملوك التمويل 👑\n\nرصيدك: {bal} جنيه\nالكاش: {CASH}", reply_markup=InlineKeyboardMarkup(kb))

async def btns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(f"حول على:\n`{CASH}`\n\nوابعت اسكرين لـ @Koko00228", parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btns))
    app.run_polling()
main()
