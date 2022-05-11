from django.db import models

# Create your models here.
class Feed(models.Model):
    content = models.TextField()    # 글내용
    image = models.TextField()  # 피드 이미지
    email = models.EmailField(default='')
    
class Like(models.Model):
    feed_id = models.IntegerField(default=0) # 내가 어떤 글에 좋아요를 눌렀는지    
    email = models.EmailField(default='') # 좋아요를 누른 사람
    is_like = models.BooleanField(default = True) # 좋아요를 눌렀는지의 여부, 좋아요 취소 시 굳이 삭제하지 않고 업데이트 하려고.
    
class Reply(models.Model):
    feed_id = models.IntegerField(default=0) # 내가 어떤 글에 댓글을 달았는지    
    email = models.EmailField(default='') # 댓글을 단 사람
    reply_content = models.TextField()  # 댓글 내용
    
class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0) # 내가 어떤 글에 북마크를 눌렀는지    
    email = models.EmailField(default='') # 북마크를 누른 사람
    is_marked = models.BooleanField(default = True) # 북마크를 눌렀는지의 여부, 북마크 취소 시 굳이 삭제하지 않고 업데이트 하려고.
    