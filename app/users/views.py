from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.users.models import User
from app.users.serializers import UserSerializer, RegisterSerializer, MyTokenObtainPairSerializer,\
SendEmailSerilaizer
from app.tasks import send_email_task

from celery.result import AsyncResult

class UserAPIList(GenericViewSet, 
                mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegisterAPI(GenericViewSet, 
                        mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class SendEmailAPIView(APIView):
    def post(self, request):
        serializer = SendEmailSerilaizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        subject = serializer.validated_data["subject"]
        body = serializer.validated_data['body']
        delay = serializer.validated_data.get("delay", 0)

        if delay and delay > 0:
            async_result = send_email_task.apple_async(args=[email, subject, body], countdown=delay)
        else:
            async_result = send_email_task.delay(email, subject, body)

        return Response(
            {"task_id" : async_result.id, "status" : async_result.status},
            status=status.HTTP_202_ACCEPTED,
        )

class TaskStatusAPIView(APIView):
    def get(self, request, task_id: str):
        async_result = AsyncResult(task_id)
        data = {
            "task_id" : task_id,
            "status" : async_result.status,
            "ready" : async_result.ready(),
            "result" : None,
        }
        if async_result.ready():
            data["result"] = async_result.result
        return Response(data)