import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# define the api key
load_dotenv()
TOKEN = os.getenv('Telebot_API_KEY')
BOT_USERNAME = "@DistrictGovernor_bot"

## COMMANDS

# start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello. I am District Governor \nI control the whether.")

# greet
async def greet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi, how are you?")

# joke
async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here's a joke: I respect you.")


## RESPONSES
def handle_response(text: str) -> str:

    processed_text: str = text.lower()

    if "you are useless" in processed_text:
        return "F you!"
    
    if "bye" in processed_text:
        return "see you"
    
    return None
    

## MESSAGES

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f"User {update.message.chat.id} in {message_type}: '{text}'")  # debug

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return  # do nothing if bot wasn't mentioned
    else:
        response: str = handle_response(text)

    if response:
        print(f"Bot: {response}")
        await update.message.reply_text(response)

## LOGGING ERRORS

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused the following error: {context.error}")


if __name__ == "__main__":
    print(f"{BOT_USERNAME}...")
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('greet', greet_command))
    app.add_handler(CommandHandler('joke', joke_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    # check for updates every 1 second
    print(f"{BOT_USERNAME} is polling.")
    app.run_polling(poll_interval=1)

print(f"{BOT_USERNAME} has been stopped.")