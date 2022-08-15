import json, requests, os
from telegram import Update
from telegram.ext import CallbackContext
from bot.handlers.base import Message
from tasks.models import Task
from users.models import User_new
from bot.models import BotTexts, BotSettings, userlevels

FIRST, SECONT, THIRD, FOURTH, PROPOSAL1, PROPOSAL2, PLATEGKA1, PLATEGKA2, LIQPAY = range(9)

BACKEND_URL = os.getenv("BACKEND_URL", "http://146.190.236.156/api/query/prototype/")
PARSE_MODE = os.getenv("PARSE_MODE", "MarkdownV2")
LOCALE = os.getenv("LOCALE", "ru")
BOT_NAME = os.getenv("BOT_NAME", "fandydev2341bot")

headers = {
            'Content-Type': "application/json; charset=utf8",
            'Accept': 'text/html,application/json;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': "ru,uk-UA;q=0.9,uk;q=0.8,en-US;q=0.7,en;q=0.6"}


def upload(update: Update, context: CallbackContext) -> None:
    bot_settings = BotSettings.objects.get(pk=1)
    fname = update.message.photo[len(update.message.photo) - 1].file_id
    user_object = User_new.objects.get(chat_id=update.message.chat.id)
    data = {"type": "add", "data": {"file_id": fname,
                                    "backend_key": BOT_NAME,
                                    "status": "NEW",
                                    "language": "RU",
                                    "telegram_message_id": "666",
                                    "foto_source": "file",
                                    "send_full_results": user_object.level.send_full_results,
                                    "FC_account": bot_settings.findclone_login,
                                    "FC_password": bot_settings.findclone_password,
                                    "FC_max_results": user_object.level.findclone_results_count,
                                    "FC_tolerance": "99.999",
                                    "PY_account": bot_settings.pimeyes_login,
                                    "PY_password": bot_settings.pimeyes_password,
                                    "PY_max_results": user_object.level.pimeyes_results_count,
                                    "PY_tolerance": 99,
                                    'chat_id': update.message.chat.id}}

    response = requests.post(BACKEND_URL, data=json.dumps(data), headers=headers)
    if response.status_code == 201:
        UUID = response.text[1:-1]
        task = Task.create(user_object, UUID, fname, 'Free')
        task.save()
    else:
        Message("SEARCH_STATUS_pim_0", update,).message_by_status()
