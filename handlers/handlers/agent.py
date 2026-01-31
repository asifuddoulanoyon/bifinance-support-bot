from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from database import assign_agent, get_case, add_message, get_user_open_case, close_case
from config import AGENTS, BOT_OWNER_ID
from database import cursor, conn

async def agent_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👨‍💼 Agent Commands:\n"
        "/mycases - View your open cases\n"
        "/takecase <CASE_ID> - Take ownership\n"
        "/closecase <CASE_ID> - Close case\n"
        "/transfer <CASE_ID> - Transfer to another agent\n"
        "/search <CASE_ID> - Search case\n"
    )
    await update.message.reply_text(msg)

async def my_cases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    agent_id = update.effective_user.id
    cursor.execute("SELECT * FROM cases WHERE assigned_agent=? AND status IN ('OPEN','IN_PROGRESS')", (agent_id,))
    cases = cursor.fetchall()
    if not cases:
        await update.message.reply_text("You have no open cases.")
        return
    buttons = [[InlineKeyboardButton(f"{c[0]}", callback_data=f"view_{c[0]}")] for c in cases]
    await update.message.reply_text("Your open cases:", reply_markup=InlineKeyboardMarkup(buttons))

async def view_case_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    case_id = query.data.split("_")[1]
    case = get_case(case_id)
    text = f"📂 Case {case_id}\nUser: {case[2]}\nEmail: {case[4]}\nProblem: {case[5]}\nStatus: {case[6]}"
    await query.message.reply_text(text)

# Add more handlers for takecase, transfer, close, reply, dashboard
# Same style as user.py for media support
