import decimal
import json

import requests as requests
from django.http import JsonResponse
from users.models import User_new
from fe_bot.settings import TOKEN

from bot.models import BotTexts, TelegramPaymentLog


def view_message_from_free_kassa(request):
    """ Принимает уведомление от фрикассы об успешной оплате """
    if request.method == "GET":
        payload = request.GET.dict()

        if payload.get("MERCHANT_ORDER_ID"):
            telegram_id = int(payload.get("MERCHANT_ORDER_ID"))
            user = User_new.objects.filter(chat_id=telegram_id).first()

            if user:
                amount = float(payload.get("AMOUNT", 0))
                log = TelegramPaymentLog.objects.filter(telegram_id=str(telegram_id), status="waiting", amount=amount).last()
                if log:
                    log.status = "payed"
                    log.save()

                currency = payload.get("us_CURRENCY")
                amount_in_rub = amount * 1.97 if currency == "UAH" else (amount * 72 if currency == "USD" else amount)

                user.balance += decimal.Decimal(amount_in_rub)
                user.save()

                language_code = user.language_code if user.language_code in ["ua", "ru", "en"] else "ru"
                message_text = getattr(BotTexts.objects.get(message_code='TEXT_SUCCESS_PAYMENT'), language_code)
                message_text = message_text.format(amount=amount_in_rub)
                post_data = {"chat_id": user.chat_id, "text": message_text}
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=post_data)

    return JsonResponse({"status": "ok"})
