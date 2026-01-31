from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters
from handlers import user, agent
import os

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

# User conversation
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', user.start)],
    states={
        user.ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, user.ask_name)],
        user.ASK_UID: [MessageHandler(filters.TEXT & ~filters.COMMAND, user.ask_uid)],
        user.ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, user.ask_email)],
        user.ASK_PROBLEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, user.ask_problem)],
    },
    fallbacks=[]
)

app.add_handler(conv_handler)

# User message handler (reply in existing case)
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, user.handle_message))

# Agent commands
app.add_handler(CommandHandler("mycases", agent.my_cases))
app.add_handler(CommandHandler("help", agent.agent_help))
# Add other agent handlers like takecase, closecase, transfer

app.run_polling()
