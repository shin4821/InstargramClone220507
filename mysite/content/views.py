from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Feed, Reply, Like, Bookmark
import os
from uuid import uuid4
from mysite.settings import MEDIA_ROOT
from user.models import User



class Main(APIView):
    def get(self, request):
        
        ########세션정보 만들기##############
        email = request.session.get('email', None)
    
        #이메일이 없으면 로그인 창으로 이동
        if email is None:
            return render(request, "user/login.html")
        
        user = User.objects.filter(email=email).first()
        
        #세션에 이메일은 있는데 인스타의 이메일이 아닌 경우, 로그인 창으로 이동.
        if user is None:
            return render(request, "user/login.html")
        ###################################
                
        # feed_list = Feed.objects.all().order_by('-id') # Select * from content_feed; 이게 바로 쿼리셋을 하는거임
        
        feed_object_list = Feed.objects.all().order_by('-id') # Select * from content_feed; 이게 바로 쿼리셋을 하는거임
        feed_list = []
        
        for feed in feed_object_list:
            # 해당 email에 맞는 유저를 찾는다.
            user = User.objects.filter(email=feed.email).first()
            
            # 댓글 리스트를 찾는다.
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                # 댓글 리스트에는 email만 있고, nickName는 없으므로 따로 해당 유저 찾아서 nickName을 넣어주어야 한다.
                user = User.objects.filter(email = reply.email).first()
                reply_list.append(dict(reply_content = reply.reply_content,
                                       nickName = user.nickName))
            
            
            
            like_count = Like.objects.filter(feed_id=feed.id, is_like = True).count() # 현재 피드 번호의, 좋아요가 True인 개수.
            
            is_liked=Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists() # 내가 이 피드에 좋아요를 눌렀는지의 여부.
            is_marked=Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists() # 내가 이 피드에 북마크를 눌렀는지의 여부.
                        
            
            # 프로필 사진을 바꾸거나 닉네임을 바꿀때 실시간으로 feed에 반영되도록 따로 처리하는 것.
            feed_list.append(dict(image=feed.image,
                                  id = feed.id,
                                  content = feed.content,
                                  like_count=like_count,
                                  profile_image = user.profile_image,
                                  nickName = user.nickName,
                                  reply_list = reply_list,
                                  is_liked = is_liked,
                                  is_marked = is_marked
                                  ))
        


        return render(request,'shaystargram/main.html', context = dict(feed_list = feed_list, user=user))
    

class UploadFeed(APIView):
    def post(self, request):
        
        # 일단 파일 불러와--------------------------------------------
        file = request.FILES['file'] #파일 통째로 갖고오기.

        uuid_name = uuid4().hex # 랜덤하게 글자를 만들어준다.
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        #-----------------------------------------------------------
        
        file =request.data.get('file')      
        image = uuid_name
        content = request.data.get('content')
        email = request.session.get('email', None)

        Feed.objects.create(content=content, image=image, email=email)
        
        return Response(statue=200)
        
        
        
class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)
    
        #이메일이 없으면 로그인 창으로 이동
        if email is None:
            return render(request, "user/login.html")
        
        user = User.objects.filter(email=email).first()
        
        #세션에 이메일은 있는데 인스타의 이메일이 아닌 경우, 로그인 창으로 이동.
        if user is None:
            return render(request, "user/login.html")
        
        # 내가 올린 피드만 보여주기.
        feed_list = Feed.objects.filter(email=email)
        # 내가 좋아요 한 피드만 보여주기
        like_list = list(Like.objects.filter(email=email, is_like = True).values_list('feed_id', flat=True)) #[1,2] 이런식으로 출력됨.
        like_feed_list = Feed.objects.filter(id__in = like_list)
        
        # 내가 북마크 한 피드만 보여주기
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked = True).values_list('feed_id', flat=True)) #[1,2] 이런식으로 출력됨.
        bookmark_feed_list = Feed.objects.filter(id__in = bookmark_list)
        
        
        return render(request,'content/profile.html', context=dict(feed_list = feed_list, like_feed_list = like_feed_list, user=user, bookmark_feed_list = bookmark_feed_list))
    
    
class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)
        
        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)
        
        return Response(status=200)
    
    
class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True) # 따로 안올라오면 True가 Default.
        email = request.session.get('email', None)
        
        if favorite_text == 'favorite_border': 
            is_like = True
        else:
            is_like = False
        
        # 무조건 db create하지말고 기존에 아이디가 이미 등록되어 있으면 업데이트만 하는 식으로 진행.
        like = Like.objects.filter(feed_id = feed_id, email = email).first()
        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)
        
        return Response(status=200)    
    
    
class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True) # 따로 안올라오면 True가 Default.
        email = request.session.get('email', None)
        
        if bookmark_text == 'bookmark_border': 
            is_marked = True
        else:
            is_marked = False
        
        # 무조건 db create하지말고 기존에 아이디가 이미 등록되어 있으면 업데이트만 하는 식으로 진행.
        bookmark = Bookmark.objects.filter(feed_id = feed_id, email = email).first()
        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)
        
        return Response(status=200)    