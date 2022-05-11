from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from django.contrib.auth.hashers import make_password
from uuid import uuid4
import os
from mysite.settings import MEDIA_ROOT

# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")
    
    def post(self, request):
        #TODO 회원가입
        email = request.data.get('email', None)
        userName = request.data.get('userName', None)
        nickName = request.data.get('nickName', None)
        password = request.data.get('password', None)
 
        User.objects.create(email=email, userName=userName, nickName=nickName, password=make_password(password), profile_image = "default_profile.jpg")
        
        return Response(status=200)
        
    
class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")
    
    def post(self, request):
        #TODO 회원가입
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        #해당 유저 찾기
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))
        
        if user.check_password(password):
            #로그인 성공. 세션 or 쿠키       
            request.session['email'] = email 
            return Response(status=200)
        
        else:
            #비밀번호가 잘못된 경우.
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))
        


class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")
    
    
    
class UploadProfile(APIView):
    def post(self, request):
        
        # 일단 파일 불러와--------------------------------------------
        file = request.FILES['file'] #파일 통째로 갖고오기.

        uuid_name = uuid4().hex # 랜덤하게 글자를 만들어준다.
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        #-----------------------------------------------------------
             
        profile_image = uuid_name
        email = request.data.get('email')
        
        user = User.objects.filter(email=email).first()
        user.profile_image = profile_image
        user.save()
        
        return Response(statue=200)