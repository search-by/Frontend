from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, \
    CallbackQueryHandler
from django_telegrambot.apps import DjangoTelegramBot
from bot.handlers import upload
from bot.handlers.base import Message
from bot.models import BotTexts, BotSettings
from users.models import User_new
from django.db.models import Q
from bot.handlers.usercheck import UserValidator

FIRST, SECOND = range(2)


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
    return FIRST


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
    elif u.is_promo_limit():
        Message("PROMO_LIMIT", update=update, context=context, log='_').message_by_status()
        return FIRST
    elif u.is_day_limit():
        Message("SEARCH_DAY_LIMIT", update=update, context=context, log='_').message_by_status()
    elif u.is_need_to_join_group():
        Message("MESSAGE_TEXT_PODPISKA", update=update, context=context, log='_').message_by_status()
    else:
        upload.upload(update, context)
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
    return FIRST


def info(update: Update, context: CallbackContext) -> None:
    u = UserValidator(update, context)
    is_allowed = check_ban_and_maitenence(u)
    if is_allowed:
        Message(is_allowed, update=update, context=context).message_by_status()
    else:
        Message('TEXTS_BOTINFO', update, log='_').profile(update, context)
    return FIRST


def main():
    dp = DjangoTelegramBot.dispatcher
    raw_texts = BotTexts.objects.all().filter(Q(message_code="BUTTON_MENU_PROFILE") | Q(message_code="BUTTON_HOME"))

    conv_handler = ConversationHandler(
        per_message=False,
        entry_points=[CommandHandler('start', start),
                      CommandHandler('info', info),
                      CommandHandler('profile', profile),
                      MessageHandler(Filters.photo, foto_upload),
                      MessageHandler(Filters.regex('^.*Профіль$|^.*Профиль$|^.*Profile$'), profile),
                      MessageHandler(Filters.regex('^.*Додому$|^.*Домой$|^.*Home$'), start),
                      MessageHandler(Filters.regex('^.*$'), anytext),
                      MessageHandler(Filters.photo, foto_upload),
                      CallbackQueryHandler(inline, pass_update_queue=False, pass_chat_data=True,
                                           pass_job_queue=False, pass_user_data=True, run_async=False
                                           ),
                      ],
        states={
            FIRST: [CommandHandler('start', start),
                    CommandHandler('profile', profile),
                    CommandHandler('info', info),
                    MessageHandler(Filters.regex('^.*Профіль$|^.*Профиль$|^.*Profile$'), profile),
                    MessageHandler(Filters.regex('^.*Додому$|^.*Домой$|^.*Home$'), start),
                    MessageHandler(Filters.regex('^.*$'), anytext),
                    MessageHandler(Filters.photo, foto_upload),
                    CallbackQueryHandler(inline, pass_update_queue=True, pass_chat_data=True,
                                         pass_job_queue=False, pass_user_data=True, run_async=False
                                        ),
                    ],
        },
        fallbacks=[CommandHandler('cancel', start)],
    )
    dp.add_handler(conv_handler)
