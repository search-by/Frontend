from telegram import Update
from telegram.ext import CallbackContext
from tasks.models import Task
from users.models import User_new


def add_task(update: Update, context: CallbackContext) -> None:
    fname = update.message.photo[len(update.message.photo) - 1].file_id
    user_object = User_new.objects.get(chat_id=update.message.chat.id)
    task = Task.create(user_object, fname)
    task.save()
