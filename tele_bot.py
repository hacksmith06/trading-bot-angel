import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load configuration from config.json
with open('config-arpit.json', 'r') as file:
    config = json.load(file)

TOKEN = config["TELEGRAM_BOT_TOKEN"]


# Command to start the bot and provide instructions
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Please enter the name, expiry, strike price, and option type separated by spaces.')


# Handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
    # Split the message into components
    components = update.message.text.split()

    # Check if the message has all required components
    if len(components) == 4:
        name, expiry, strike_price, option_type = components

        # Fetch the token or perform any other operations here
        # For demonstration purposes, we'll just echo the inputs
        update.message.reply_text(f"Name: {name}\nExpiry: {expiry}\nStrike Price: {strike_price}\nOption Type: {option_type}")
    else:
        update.message.reply_text('Invalid input. Please enter the name, expiry, strike price, and option type separated by spaces.')


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
