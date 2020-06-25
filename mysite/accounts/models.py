from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="followings",
        blank=True
    )

    # 각종 필드들 추가

    # 슈퍼계정
    # 1. createSuperUser 안통한다? 그래서 User만들기 전에 createSuperUser계정 얼른 만들어놓고 시작하자
    # 2. (shell_plus) create_user is_staff, 최고권한 True 로 강제로 ORM으로 만들어도된다.