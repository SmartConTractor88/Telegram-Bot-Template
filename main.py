import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from functions import is_valid_bsc_contract_address, is_token_contract, token_data

# define the api key
load_dotenv()
TOKEN = os.getenv('Telebot_API_KEY')
BOT_USERNAME = "@DistrictGovernor_bot"
api_key = os.getenv('api_key')


## COMMANDS
# start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I am District Governor. \nI can asist you with crypto trading on BSC.")

# greet
async def greet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi, how are you?")


## RESPONSES
def handle_response(text: str) -> str:

    # change text to lowercase for easier processing
    processed_text: str = text

    if is_valid_bsc_contract_address(ca=processed_text): # True/False
        if is_token_contract(ca=processed_text, api_key=api_key):
            analysis = token_data(ca=processed_text)
            return analysis
        else:
            return "This is not a crypto token on BSC"
    else: 
        return "Invalid contract address."

## MESSAGES

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f"User {update.message.chat.id} in {message_type}: '{text}'")  # debug

  
    if message_type == "private":
        response: str = handle_response(text)
    # private messages
    else:
        response: str = handle_response(text)

    if response:
        print(f"Bot: {response}")
        await update.message.reply_text(response)

## LOGGING ERRORS

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused the following error: {context.error}")


if __name__ == "__main__":
    print(f"Starting {BOT_USERNAME}")
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('greet', greet_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    # check for updates every 1 second
    print(f"{BOT_USERNAME} is polling...")
    app.run_polling(poll_interval=1)

print(f"{BOT_USERNAME} has been stopped.")