from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskStatusSerializer
from .models import Task
from django.shortcuts import get_object_or_404
import datetime
from bot.handlers.base import Message


class TaskWiew(APIView):
    def post(self, request):
        data = request.data.get('data')
        naive_datetime = datetime.datetime.now()
        try:
            t = get_object_or_404(Task, UUID=data['UUID'])
            t.logs += f"{naive_datetime} Status changed {t.status} -> {data['status']}\n"
            t.last_update = naive_datetime
            TaskSerializer = TaskStatusSerializer(instance=t, data=data, partial=True)
            if TaskSerializer.change_status(instance=t, validated_data=data):
                if TaskSerializer.is_valid(raise_exception=True):
                    t_new = TaskSerializer.save()
                    return Response({"status": f"Status changed {t.status} -> {t_new.status}",
                                     "data": t_new.status}, status=status.HTTP_200_OK)
                else:
                    print(f'Invalid: {TaskSerializer}')
            else:
                return Response({"status": f"Status NOT changed {t.status} -> {data['status']}",
                                 "data": t.status}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            return Response({"status": e.args, "data": data}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data.get('data')

        t = Task.objects.get(UUID=data['UUID'])
        serializer = TaskStatusSerializer(instance=t, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):

            if int(data['pimeyes_status']) == 9:
                if data['status'] == '999999199999':
                    Message(chat_id=t.user.chat_id, status=f"SEARCH_STATUS_pim_{data['pimeyes_status']}").send_pdf_file(search_id=data['UUID'])
                else:
                    Message(chat_id=t.user.chat_id, status=f"SEARCH_STATUS_pim_0").message_by_status()

            else:
                Message(chat_id=t.user.chat_id, status=f"SEARCH_STATUS_pim_{data['pimeyes_status']}").message_by_status()

            serializer.save()

            return Response({"status": True}, status=status.HTTP_200_OK)
        else:
            Message(chat_id=t.user.chat_id, status=f"SEARCH_STATUS_pim_{data['pimeyes_status']}", log='x').message_by_status()
            serializer.save()
            return Response({"status": True}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
