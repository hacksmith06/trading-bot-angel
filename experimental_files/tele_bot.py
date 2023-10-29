from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import logging
import json

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration from config.json
with open('config-arpit.json', 'r') as file:
    config = json.load(file)

TOKEN = config["TELEGRAM_BOT_TOKEN"]

user_data = {}


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("START", callback_data='start_bot'),
         InlineKeyboardButton("STOP", callback_data='stop_bot')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == "start_bot":
        query.edit_message_text(text=f"Bot Started... ✅")
        logger.info("Bot started by user %s", update.effective_user.first_name)
        choose_instrument(update, context)

    elif query.data == "stop_bot":
        query.edit_message_text(text=f"Bot Stopped... ❌")
        logger.info("Bot stopped by user %s", update.effective_user.first_name)

    elif query.data in ["NIFTY", "BANKNIFTY"]:
        user_data['instrument'] = query.data
        logger.info("User %s selected instrument: %s", update.effective_user.first_name, user_data['instrument'])
        query.message.reply_text(f"Selected: {user_data['instrument']}. Now, send the strike price and option type (e.g. 20000PE):")

    elif query.data == "confirm_order":
        summary = f"Order Details:\nInstrument: {user_data['instrument']}\nStrike & Option: {user_data['strike_and_option']}\nBuy Price: {user_data['buy_price']}"
        logger.info("User %s confirmed order:\n%s", update.effective_user.first_name, summary)
        query.edit_message_text(text=summary + "\nOrder Confirmed ✅")

    elif query.data == "edit_order":
        del user_data['strike_and_option']
        del user_data['buy_price']
        choose_instrument(update, context)


def choose_instrument(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("NIFTY", callback_data='NIFTY'),
         InlineKeyboardButton("BANKNIFTY", callback_data='BANKNIFTY')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Please select either "NIFTY" or "BANKNIFTY":', reply_markup=reply_markup)


def handle_message(update: Update, context: CallbackContext) -> None:
    if 'instrument' in user_data and 'strike_and_option' not in user_data:
        user_data['strike_and_option'] = update.message.text
        logger.info("User %s selected strike and option: %s", update.effective_user.first_name, user_data['strike_and_option'])
        update.message.reply_text(f"Selected: {user_data['strike_and_option']}. Now, send the buy price:")
    elif 'buy_price' not in user_data:
        user_data['buy_price'] = update.message.text
        logger.info("User %s selected buy price: %s", update.effective_user.first_name, user_data['buy_price'])
        confirm_or_edit(update, context)


def confirm_or_edit(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Confirm", callback_data='confirm_order'),
         InlineKeyboardButton("Edit", callback_data='edit_order')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please confirm or edit your order:', reply_markup=reply_markup)


def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
