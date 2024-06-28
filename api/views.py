from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
from main.models import User, Group
from .get_avg import get_avg_results
from .mypermission import IsStaffStatus, IsSuperUserStatus


class UserApiView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserStatus)
    def get(self, request, *args, **kwargs):
        
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentAvgApiView(APIView):
    permission_classes = (IsAuthenticated, IsStaffStatus)

    def get(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(User, id=student_id)         
        data = get_avg_results(student)
        return Response(data, status=status.HTTP_200_OK)


class GroupAvgApiView(APIView):
    permission_classes = (IsAuthenticated, IsStaffStatus)

    def get (self, request, group_id, *args, **kwargs):
        group = get_object_or_404(Group, id=group_id)      
        data = get_avg_results(group)
        return Response(data, status=status.HTTP_200_OK)


def myhandler404(request, exception):
    return Response(status=status.HTTP_404_NOT_FOUND)