from .models import Logs
from rest_framework.response import Response
from rest_framework.views import APIView

#ОСТАЛОСЬ ОТ ПРОШЛОЙ РЕАЛИЗАЦИИ КОГДА ЛОГИ ЧЕРЕЗ АПИ ПЕРЕДАВАЛИСЬ. СЕЙЧАС НЕ ИСПОЛЬЗУЕТСЯ


class LogWiew(APIView):
    def get(self, request, chat_id, user_name, text, add1='', add2='', add3=''):
        l = Logs(chat_id=chat_id, user_name=user_name, text=text, additional1=add1, additional2=add2, additional3=add3)
        l.save()
        return Response({"query": True})

    def post(self, request, chat_id, user_name, text, search_id='',  add1='', add2='', add3=''):
        l = Logs(chat_id=request.POST['chat_id'], user_name=request.POST['user_name'], text=request.POST['text'],
                 additional1=add1, additional2=add2, additional3=add3)
        l.save()
        return Response({"query": True})
