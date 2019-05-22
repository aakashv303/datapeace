from .models import User
from .serializers import UserSerializer
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.paginator import Paginator

# importing data into database
# connex = sqlite3.connect("db.sqlite3")
# cur = connex.cursor()
# for chunk in pd.read_csv(r'C:\Users\Aakash Vaghela\Downloads\sqlify-result.csv', chunksize=4):
#     chunk.to_sql(name="crud_user", con=connex, if_exists="append", index=False)

@api_view(['GET', 'POST'])
def UserList(request):
    if request.method == 'GET':
        # get request with parameter
        if request.GET.get('page') or request.GET.get('limit') or request.GET.get('name') or request.GET.get('sort'):
            page = request.GET.get('page') # getting page num from url
            limit = request.GET.get('limit') # getting limit from url
            name = request.GET.get('name') # getting name from url
            sort = request.GET.get('sort') # getting sort from url
            user_list = User.objects.filter(first_name__icontains=name) | User.objects.filter(last_name__icontains=name) #search with name
            if len(sort) != 0:
                users = user_list.order_by(sort) # sorting by sort parameter
            else:
                users = user_list
            if len(limit) != 0:
                paginator = Paginator(users, limit) # using limit provided by url
            else:
                paginator = Paginator(users, 5) # using default limit
            userlist = paginator.get_page(page)
            serializer = UserSerializer(userlist, many=True)
            return Response(serializer.data, status=200)
        else:
            # get request without parameter
            user_list = User.objects.all()
            serializer = UserSerializer(user_list, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        # create user
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def UserDetail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # get user with id
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # update user with id
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # delete user with id
        user.delete()
        return Response(status=status.HTTP_200_OK)
