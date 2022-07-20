from django.http import JsonResponse
from django.shortcuts import render
from .models import Book
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

# Authentication Start
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Authentication End

# register
@api_view(['POST'])
def addUser(request):
    User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password'],
        is_staff=1,
        is_superuser=True)
    return JsonResponse({"done": "test"})


# name ,author,createdTime, _id
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def books(request, id=-1):
    print(request.user)
    if request.method == 'GET':  # method get all
        if int(id) > -1:  # get single product
            if int(id) > Book.objects.count():
                return JsonResponse({"out of bounds array": "1111"})
            book = Book.objects.get(_id=id)

            return JsonResponse({
                "name": book.name,
                "author": book.author
            }, safe=False)
        else:  # return all
            res = []  # create an empty list
            for bookObj in Book.objects.all():  # run on every row in the table...
                res.append({"name": bookObj.name,
                            "author": bookObj.author,
                            "id": bookObj._id
                            })  # append row by to row to res list
            # return array as json response
            return JsonResponse(res, safe=False)
    if request.method == 'POST':  # method post add new row
        # print(request.data['name'])
        # name =request.data['name']
        Book.objects.create(
            name=request.data['name'], author=request.data['author'])
        return JsonResponse({'POST': "test"})
    if request.method == 'DELETE':  # method delete a row
        temp = Book.objects.get(_id=id)
        temp.delete()
        return JsonResponse({'DELETE': id})
    if request.method == 'PUT':  # method delete a row
        temp = Book.objects.get(_id=id)

        temp.name = request.data['name']
        temp.author = request.data['author']
        temp.save()

        return JsonResponse({'PUT': id})
