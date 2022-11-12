from random import shuffle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from .models import Task
from django.shortcuts import get_object_or_404
import datetime


class TaskWiew(APIView):
    def get(self, request):
        q = Task.objects.all().filter(status="NEW")
        query_serializer = TaskSerializer(q, many=True)
        shuffle(query_serializer.data)
        if len(query_serializer.data) > 0:
            return Response(data=query_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=False, status=status.HTTP_201_CREATED)

    def post(self, request):
        data = request.data.get('data')
        naive_datetime = datetime.datetime.now()
        try:
            t = get_object_or_404(Task, UUID=data['UUID'])
            t.logs += f"{naive_datetime} Status changed {t.status} -> {data['status']}\n"
            t.last_update = naive_datetime
            TaskSerializer = TaskPrototypeSerializer(instance=t, data=data, partial=True) #КОСТЫЛЬ удаление TaskStatusSerializer
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
        serializer = TaskSerializer(instance=t, data=data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"status": f"Status changed {t.status} -> {t.status}",
                                 "data": t.status}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"status": e.args, "data": data}, status=status.HTTP_400_BAD_REQUEST)