from datetime import datetime
import json
from rest_framework.response import Response
import random
from rest_framework import status
from rest_framework.decorators import api_view
from .models import user_collection
import random
from django.conf import settings
from twilio.rest import Client
from bson.json_util import dumps

# Create your views here.
@api_view(['get'])
def home(request):
    return Response("Women are safe")

@api_view(['post'])
def send_otp(request):
    data = request.data
    phnm = data.get('phone_number')

    otp = random.randint(1000,9999)
    global otpshare
    def otpshare():
       return otp


    if data.get('phone_number') is None:
        return Response({'msg':'required number'})

    else:
      try:
        account_sid = settings.ACCOUNT_SID
        auth_token = settings.AUTH_TOKEN

        print(account_sid)

        client = Client(account_sid , auth_token)

        message = client.messages.create(
           from_ ='+12565489967',
           body = f'your otp is {otp} please do not share this otp to anyone',
           to = data.get('phone_number')
      )
      except Exception as e:
       print(e)


    return Response({
           'msg':"otp sent",
       })

@api_view(['post'])
def register_user(request):
    data = request.data

    records = {
       "phone_number":data.get['phone_number'],
       "password":data.get['passsword']
    }
    find_user =user_collection.find({"phone_number":data.get["phone_number"]})
    if find_user is None:
       user_collection.insert_one(records)
       return Response(status=status.HTTP_201_CREATED)
    else:
       return Response(status=status.HTTP_208_ALREADY_REPORTED)



@api_view(['POST'])
def loginuser(request):
    data = request.data
    phone = data.get("phone_number")
    password = data.get("password")
    
    print(phone,password)

    if not phone or not password:
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

    # Correct usage
    user = user_collection.find_one({"phone_number": phone})

    if not user:
        return Response({"error": "User not found{phone}"}, status=status.HTTP_404_NOT_FOUND)

    if user.get("password") != password:
        return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({"message": "Login successful"}, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_all_users(request):
    try:
        users_cursor = user_collection.find()  # fetch all users
        users_list = list(users_cursor)  # convert cursor to list
        users_json = json.loads(dumps(users_list))  # convert BSON to JSON-serializable

        return Response({"users": users_json}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
     

@api_view(['POST'])
def add_user(request):
    data = request.data

    phone_number = data.get("phone_number")
   
    password = data.get("password")  

    if not phone_number or not password:
        return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

    existing_user = user_collection.find_one({"phone_number": phone_number})
    if existing_user:
        return Response({"error": "User already exists."}, status=status.HTTP_409_CONFLICT)

    new_user = {
        "phone_number": phone_number,
        "password": password,
        
    }

    result = user_collection.insert_one(new_user)

    return Response({
        "message": "User added successfully.",
        "user_id": str(result.inserted_id)
    }, status=status.HTTP_201_CREATED)