from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from database import create_case, add_message, get_user_open_case, close_case
import re

ASK_NAME, ASK_UID, ASK_EMAIL, ASK_PROBLEM = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Bifinance Customer Support!\n"
        "This is the only official support channel.\n"
        "⚠️ Bifinance support will never message you first.\n\n"
        "Please answer the following questions to create a support ticket."
    )
    await update.message.reply_text("What's your Name?")
    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if not name:
        await update.message.reply_text("Name is required. Please type your name.")
        return ASK_NAME
    context.user_data['name'] = name
    await update.message.reply_text("What's your Bifinance UID? (optional, type skip)")
    return ASK_UID

async def ask_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    if uid.lower() == "skip":
        uid = None
    context.user_data['uid'] = uid
    await update.message.reply_text("What's your email?")
    return ASK_EMAIL

async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        await update.message.reply_text("Invalid email format. Please type a valid email.")
        return ASK_EMAIL
    context.user_data['email'] = email
    await update.message.reply_text("Please describe your problem.")
    return ASK_PROBLEM

async def ask_problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    problem = update.message.text
    context.user_data['problem'] = problem
    user_id = update.effective_user.id
    case_id = create_case(user_id, context.user_data['name'], context.user_data['uid'], context.user_data['email'], problem)
    context.user_data['case_id'] = case_id
    add_message(case_id, "user", context.user_data['name'], "text", problem)
    await update.message.reply_text(f"✅ Your support case has been created! Case ID: {case_id}\nAn agent will contact you soon.")
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    case = get_user_open_case(user_id)
    if not case:
        await update.message.reply_text("You have no open case. Use /start to create a new support ticket.")
        return
    case_id = case[0]
    if update.message.text:
        add_message(case_id, "user", update.effective_user.first_name, "text", update.message.text)
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
        add_message(case_id, "user", update.effective_user.first_name, "photo", file_id)
    elif update.message.video:
        file_id = update.message.video.file_id
        add_message(case_id, "user", update.effective_user.first_name, "video", file_id)
    elif update.message.document:
        file_id = update.message.document.file_id
        add_message(case_id, "user", update.effective_user.first_name, "document", file_id)
    # Add other media types as needed
    await update.message.reply_text("✅ Your message has been sent to the assigned agent.")
