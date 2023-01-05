from bot.handlers import upload
from bot.handlers.base import Message
from bot.handlers.usercheck import UserValidator
from bot.models import BotTexts
from django.db.models import Q
from django_telegrambot.apps import DjangoTelegramBot
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, \
    CallbackQueryHandler
from users.models import User_new

from .free_kassa_api import freekassa_client
from .models import TelegramPaymentLog

FIRST = range(1)
GET_AMOUNT_STATE = range(2)


# ГОВНОКОД, НУЖНО ПОДИЧСТИТЬ. ЗАТО РАБОТАЕТ

def check_ban_and_maitenence(user: User_new):
    if user.is_user_baned():
        return "BAN"
    elif user.is_maitenence():
        return "STATUS_MAITENANCE"
    else:
        return False


def start(update: Update, context: CallbackContext) -> None:
    u = UserValidator(update, context)
    is_allowed = check_ban_and_maitenence(u)
    if is_allowed:
        Message(is_allowed, update=update, context=context).message_by_status()
    else:
        Message("/start", update=update, context=context, log=update.message.text).message_by_status()
    # return FIRST


def anytext(update: Update, context: CallbackContext) -> None:
    u = UserValidator(update, context)
    is_allowed = check_ban_and_maitenence(u)
    if is_allowed:
        Message(is_allowed, update=update, context=context).message_by_status()
    else:
        Message("ANYTEXT", update=update, context=context, log=update.message.text).message_by_status()
    return FIRST


def foto_upload(update: Update, context: CallbackContext) -> None:
    u = UserValidator(update, context)
    is_allowed = check_ban_and_maitenence(u)
    if is_allowed:
        Message(is_allowed, update=update, context=context).message_by_status()
        return FIRST
    elif u.is_day_limit():
        if u.is_user_have_extra_searches():
            Message("SEARCH_DAY_LIMIT", update=update, context=context, log='_').message_by_status()
            return FIRST
        else:
            upload.add_task(update, context)
            try:
                Message("PROMO_LIMIT", update=update, context=context, log='_').send_document_upload()
            except Exception as e:
                print(e)
                Message("PROMO_LIMIT", update=update, context=context, log='_').message_by_status()
            Message("SEARCH_STATUS_pim_1", update=update, context=context, log='_').message_by_status()
            return FIRST
    elif u.is_need_to_join_group():
        Message("MESSAGE_TEXT_PODPISKA", update=update, context=context, log='_').message_by_status()
    else:
        upload.add_task(update, context)
        Message("SEARCH_STATUS_pim_1", update=update, context=context, log='_').message_by_status()
    if u.is_need_to_show_ads():
        Message("SEARCH_REKLAMA", update=update, context=context, log='_').message_by_status()
    return FIRST


def profile(update: Update, context: CallbackContext) -> None:
    u = UserValidator(update, context)
    is_allowed = check_ban_and_maitenence(u)
    if is_allowed:
        Message(is_allowed, update=update, context=context).message_by_status()
    else:
        Message('MENU_TEXT_PROFILE', update, log=update.message.text).profile(update, context)
    return FIRST


""" Пополнить кошелек """


def add_money_balance(update: Update, context: CallbackContext) -> iter:
    u = UserValidator(update, context)
    is_allowed = check_ban_and_maitenence(u)
    if is_allowed:
        Message(is_allowed, update=update, context=context).message_by_status()
    else:
        Message('MENU_TEXT_ADD_MONEY', update, log=update.message.text).add_money_balance(update, context)
    return GET_AMOUNT_STATE


#

def get_amount_to_add_balance(update: Update, context: CallbackContext) -> iter:
    u = UserValidator(update, context)
    is_allowed = check_ban_and_maitenence(u)
    if is_allowed:
        Message(is_allowed, update=update, context=context).message_by_status()
    else:
        try:
            amount = float(update.message.text)
            TelegramPaymentLog.objects.create(telegram_id=update.message.from_user.id, status="waiting", amount=amount)
            payment_link = freekassa_client.create_sci(amount, update.message.from_user.id)
            Message('MENU_TEXT_ASK_TO_PAY', update, log=update.message.text).ask_to_pay(payment_link=payment_link)
            return FIRST

        except ValueError:
            return GET_AMOUNT_STATE


""" End пополнить кошелек """


def inline(update: Update, context: CallbackContext) -> None:
    u = UserValidator(update, context)
    is_allowed = check_ban_and_maitenence(u)
    if is_allowed:
        Message(is_allowed, update=update, context=context).message_by_status()
        return FIRST
    quer = update.callback_query
    if quer.data == "INLINE_TEXT_SUPPORT":
        m = Message('MESSAGE_TEXT_DONATE', chat_id=quer.message.chat.id, log='_')
        m.inline()
    elif quer.data[:9] == "feedback_":
        Message('SEARCH_REKLAMA', chat_id=quer.message.chat.id, log='_').message_by_status()
    else:
        pass
    return FIRST


def main():
    dp = DjangoTelegramBot.dispatcher
    raw_texts = BotTexts.objects.all().filter(Q(message_code="BUTTON_MENU_PROFILE") | Q(message_code="BUTTON_HOME"))
    default_points = [CommandHandler('start', start),
                      CommandHandler('profile', profile),
                      MessageHandler(Filters.photo, foto_upload),
                      MessageHandler(Filters.regex('^.*Профіль$|^.*Профиль$|^.*Profile$'), profile),
                      MessageHandler(Filters.regex('^.*Пополнить баланс$|^.*Пополнить баланс$|^.*Пополнить баланс$'),
                                     add_money_balance),
                      MessageHandler(Filters.regex('^.*Додому$|^.*Домой$|^.*Home$'), start),
                      MessageHandler(Filters.regex('^.*$'), anytext),
                      MessageHandler(Filters.photo, foto_upload),
                      CallbackQueryHandler(inline, pass_update_queue=False, pass_chat_data=True,
                                           pass_job_queue=False, pass_user_data=True, run_async=False
                                           )]
    conv_handler = ConversationHandler(
        per_message=False,
        entry_points=[*default_points],
        states={
            FIRST: [*default_points],
            GET_AMOUNT_STATE: [MessageHandler(Filters.text, get_amount_to_add_balance), *default_points],
        },
        fallbacks=[CommandHandler('cancel', start)],
    )
    dp.add_handler(conv_handler)
