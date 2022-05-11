from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.

class User(AbstractBaseUser):
    """
    유저 프로필 사진
    유저 닉네임(실제 화면에 표기)
    유저 이름(실제 유저 이름)
    유저 이메일(회원가입 시 아이디)
    유저 비밀번호 => 장고 디폴트 사용. 따로 설정x
    """
    profile_image = models.TextField()
    nickName = models.TextField(max_length=24, unique=True)
    userName = models.TextField(max_length=24, null=True)
    email = models.EmailField(unique=True)
      
    #실제 유저를 선택하면 그 유저의 이름을 어떤 필드를 쓸꺼냐 정하는거임.
    USERNAME_FIELD = 'nickName'
      
    class Meta:
        db_table = "User"
    
    
    
    
    
    