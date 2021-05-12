import logging
from uuid import uuid4

from telegram import (LabeledPrice, ShippingOption, Update, 
                        InlineQueryResultArticle, 
                        InlineKeyboardButton,
                        InlineKeyboardMarkup,
                        InputTextMessageContent, 
                        ParseMode,
                        
                        InlineQuery)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    InlineQueryHandler,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    CallbackContext,
    CallbackQueryHandler
)
from telegram.inline.inputinvoicemessagecontent import InputInvoiceMessageContent
from telegram.utils.helpers import escape_markdown
TOKEN = "350862534:LIVE:MTAwMmZkMDA2MmVj"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Use /start to launch this bot.")


def start_callback(update: Update, _: CallbackContext) -> None:
    msg = (
        "Use /shipping to get an invoice for shipping-payment, or /noshipping for an "
        "invoice without shipping."
        "Or use @botname to view all avaiable product and select one to pay. in any chat"
    )

    update.message.reply_text(msg)


def start_with_shipping_callback(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Demo Payment"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    provider_token = TOKEN

    currency = "USD"
    # price in dollars
    price = 1
    # price * 100 so as to include 2 decimal points
    # check https://core.telegram.org/bots/payments#supported-currencies for more details
    prices = [LabeledPrice("Price", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    context.bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        provider_token,
        currency,
        prices,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
    )


def start_without_shipping_callback(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    title = "Make Payment"
    description = "Payment Without Shipping"
    payload = "Custom-Payload"
    provider_token = TOKEN
    currency = "USD"
    price = 1
    prices = [LabeledPrice("Price", price * 100)]
    context.bot.send_invoice(
        chat_id, title, description, payload, provider_token, currency, prices
    )


def shipping_callback(update: Update, _: CallbackContext) -> None:
    query = update.shipping_query
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message="Something went wrong...")
        return

    options = list()
    options.append(ShippingOption('1', 'Shipping Option A', [LabeledPrice('A', 100)]))
    price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
    options.append(ShippingOption('2', 'Shipping Option B', price_list))
    query.answer(ok=True, shipping_options=options)


def precheckout_callback(update: Update, _: CallbackContext) -> None:
    query = update.pre_checkout_query
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)


def successful_payment_callback(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Thank you for your payment!")


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    if query == "":
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Pay",
            thub_url = 'https://i.pinimg.com/originals/a0/99/01/a09901c7cbacf0f13fad6568817f18dc.jpg',
            description="Buy this item, send me your money.",
            input_message_content=InputInvoiceMessageContent(
                title="Laptop baggy",
                payload="my-payment-bot",
                description="Buy this Bag 100USD",
                provider_token=TOKEN,
                currency = 'USD',
                photo_url = 'https://i.pinimg.com/originals/a0/99/01/a09901c7cbacf0f13fad6568817f18dc.jpg',
                prices = [LabeledPrice("Price", 100 * 100)],
                need_name= True,
                need_phone_number= True,
                need_email=True,
                is_flexible= True
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Pay",
            thumb_url = 'https://i.pinimg.com/originals/a0/99/01/a09901c7cbacf0f13fad6568817f18dc.jpg',
            description="Buy this item, send me your money.",
            input_message_content=InputInvoiceMessageContent(
                title="Laptop baggy",
                payload="my-payment-bot",
                description="Buy this Bag 50USD",
                provider_token=TOKEN,
                currency = 'USD',
                photo_url = 'https://i.pinimg.com/originals/a0/99/01/a09901c7cbacf0f13fad6568817f18dc.jpg',
                prices = [LabeledPrice("Price", 50 * 100)],
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Pay",
            thumb_url = 'https://i.pinimg.com/originals/a0/99/01/a09901c7cbacf0f13fad6568817f18dc.jpg',
            description="Buy this item, send me your money.",
            input_message_content=InputInvoiceMessageContent(
                title="Laptop baggy",
                payload="my-payment-bot",
                description="Buy this Bag 25USD",
                provider_token=TOKEN,
                currency = 'USD',
                photo_url = 'https://i.pinimg.com/originals/a0/99/01/a09901c7cbacf0f13fad6568817f18dc.jpg',
                prices = [LabeledPrice("Price", 25 * 100)],
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Pay",
            thumb_url = 'https://i.pinimg.com/originals/a0/99/01/a09901c7cbacf0f13fad6568817f18dc.jpg',
            description="Buy this item, send me your money.",
            input_message_content=InputInvoiceMessageContent(
                title="Laptop baggy",
                payload="my-payment-bot",
                description="Buy this Bag 75USD",
                provider_token=TOKEN,
                currency = 'USD',
                photo_url = 'https://i.pinimg.com/originals/a0/99/01/a09901c7cbacf0f13fad6568817f18dc.jpg',
                prices = [LabeledPrice("Price", 75 * 100)],
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Pay",
            thumb_url = 'https://i.pinimg.com/originals/a0/99/01/a09901c7cbacf0f13fad6568817f18dc.jpg',
            description="Buy this item, send me your money.",
            input_message_content=InputInvoiceMessageContent(
                title="Laptop baggy",
                payload="my-payment-bot",
                description="Buy this Bag 75USD",
                provider_token=TOKEN,
                currency = 'USD',
                photo_url = 'https://i.pinimg.com/originals/a0/99/01/a09901c7cbacf0f13fad6568817f18dc.jpg',
                prices = [LabeledPrice("Price", 75 * 100)],
            ),
        ),
        
    ]

    update.inline_query.answer(results)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")






def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("1853391556:AAH3EiJsBnFz_VBkCmpn5nkGwpJUgNVF0eU")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # simple start function
    dispatcher.add_handler(CommandHandler("start", start_callback))
    dispatcher.add_handler(CommandHandler('help', help_command))

    # Add command handler to start the payment invoice
    dispatcher.add_handler(CommandHandler("shipping", start_with_shipping_callback))
    dispatcher.add_handler(CommandHandler("noshipping", start_without_shipping_callback))

    # Optional handler if your product requires shipping
    dispatcher.add_handler(ShippingQueryHandler(shipping_callback))

    # Pre-checkout handler to final check
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))

    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    # UNKOWN COMMANDS   
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()