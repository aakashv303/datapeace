from .models import User
from .serializers import UserSerializer
import pandas as pd
import sqlite3
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re

# importing data into database
# connex = sqlite3.connect("db.sqlite3")  
# cur = connex.cursor()
# for chunk in pd.read_csv(r'C:\Users\Aakash Vaghela\Downloads\sqlify-result.csv', chunksize=4):
#     chunk.to_sql(name="crud_user", con=connex, if_exists="append", index=False)

class UserList(APIView):
    def get(self, request, format=None):
        path = (str(request.get_full_path))
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        sort = request.GET.get('sort')
        name = request.GET.get('name')
        final = []
        if (path.find('page') == -1) and (path.find('limit') == -1) and (path.find('sort') == -1) and (path.find('name') == -1):
            user_list = User.objects.all()
            serializer = UserSerializer(user_list, many=True)
            return Response(serializer.data, status=200)
        elif len(sort) != 0:
            user_list = User.objects.all().order_by(sort)
            for i in user_list:
                if re.search(name,i.first_name) or re.search(name,i.last_name):
                    final.append(i)
            if len(limit) == 0:
                paginator = Paginator(final, 5)
            else:
                paginator = Paginator(final, limit)
            users = paginator.get_page(page)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=200)
        elif len(sort) == 0 and len(name) != 0:
            user_list = User.objects.all()
            for i in user_list:
                if re.search(name,i.first_name) or re.search(name,i.last_name):
                    final.append(i)
            if len(limit) == 0:
                paginator = Paginator(final, 5)
            else:
                paginator = Paginator(final, limit)
            users = paginator.get_page(page)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=200)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_object(self, id):
        try:
            user = User.objects.get(id=id)
            return(user)
        except user.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

    def put(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = self.get_object(id)
        user.delete()
        return Response(status=200)
