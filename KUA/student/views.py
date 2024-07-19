from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import render
from . import models
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from . import serializers
import string
import random
from django.core.mail import EmailMessage
from django.utils import timezone
        
class SubmitTimeTableView(generics.CreateAPIView): #id, 학수번호, 개설년도와 학기 정보를 통해 시간표를 등록하는 view
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(user.username)
        course_id = request.data['course_id']
        year = request.data['year']
        semester = request.data['semester']
        timetable = {
            'username': user.username,
            'course_id': course_id,
            'year': year,
            'semester': semester
        }
        serializer = serializers.TimeTableSerializer(data = timetable)
        if serializer.is_valid():
            serializer.save()
            return Response({'response': 'Time Table Saved'})
        return Response({'response': 'Time Table Rejected'})
    
class EmailCodeSendView(generics.CreateAPIView):
    def post(self, request):
        letters_set = string.ascii_letters
        random_code_list = random.sample(letters_set,8)
        random_code = ''.join(random_code_list)

        email = request.data['email']

        if not email:
            return Response({'error': 'Not Valid Email'})
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'This email is already used.'})
        
        email_message = EmailMessage(
            subject='KU&A Permission Code',
            body= f'KU&A 인증 번호는 {random_code}입니다.',
            to=[email],
        )
        email_message.send()
        
        email_object, created = models.CertificationCode.objects.get_or_create(email=email)

        email_object.certification_code = random_code

        email_object.save()

        return Response({'Permission Code Update' : True})

class EmailCodeCheckView(generics.RetrieveAPIView):
    def get(self, request):
        email = request.data['email']
        code = request.data['code']
        
        if not email:
            return Response({'error': 'Invalid Email Address'})
        
        if models.CertificationCode.objects.filter(email=email).exists():
            email_object = models.CertificationCode.objects.get(email=email)
            if code == email_object.certification_code:
                email_object.certification_check = True
                return Response({'Permission': True})
            else:
                return Response({'Permission': False})
        
        else:
            return Response({'error': 'Invalid Email Address'})

class CreateGroupView(generics.CreateAPIView):
    def post(self, request):
        group = Group.objects.get_or_create(name=request.data['group_name'])
        return Response('Success to create group')
    
class SignupView(generics.CreateAPIView):
    def post(self, request):
        user_data = {
            'username' : request.data['username'],
            'first_name' : request.data['first_name'],
            'last_name' : request.data['last_name'],
            'email' : request.data['email'],
            'password' : request.data['password'],
            'group': request.data['group'],
            'is_staff' : False,
            'is_active' : True,
            'is_superuser' : False,
            'date_joined' : timezone.now(),
        }
        
        user_serializer = serializers.UserSerializer(data = user_data)
        if not user_serializer.is_valid():
            return Response({'Invalid User Information'})
        
        user = user_serializer.save()
        
        student_number = models.Student.objects.count()
        
        nickname_animal = ['사자', '고양이', '강아지', '호랑이', '매', '양', '토끼', '용', '용', '다람쥐', '돼지', '소', '쥐', '파리', '모기',
                   '까마귀', '벌', '개미', '염소', '하마', '코뿔소', '곰', '뱀', '원숭이', '고릴라', '말']

        random_animal = random.choices(nickname_animal, k=1)

        nickname = random_animal[0] + str(student_number)
        
        student = {
            'user': user.id,
            'nickname': nickname,
            'points': 0,
            'permission_type':  '7',
            'permission_date': timezone.now(),
        }

        student_serializer = serializers.StudentSerializer(data = student)

        if not student_serializer.is_valid():   
            return Response(student_serializer.errors)
            
        student_serializer.save()
        token = Token.objects.create(user = user)
        return Response({"Token": token.key})
        
        
class LoginView(generics.RetrieveAPIView):
    def get(self, request):
        user = authenticate(username = request.data['username'], password = request.data['password'])
        if user is not None:
            token = Token.objects.get(user=user)
            return Response({"Token": token.key})
        else:
            return Response(status = 401)
        

