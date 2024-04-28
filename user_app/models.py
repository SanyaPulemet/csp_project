from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Пользователь
class User(AbstractUser):
    #   ПОЛЯ АБСТРАКТНОГО ПОЛЬЗОВАТЕЛЯ
    #   см. документацию Django
    #
    description = models.CharField(max_length=512)
    image       = models.ImageField(default="profile/default.jpg", upload_to="profile")

    # отображает, удалён ли пользователь
    removed     = models.BooleanField(default=False)

    # уникальное поле, по стандарту login
    def __str__(self):
        return self.email

# таблица тэгов пользователя
class UserTag(models.Model):
    text        = models.CharField(max_length=63)

# таблица для сопоставления тэга пользователя с самим пользователем
class UserTagConnectionTable(models.Model):
    user_id     = models.ForeignKey(User, on_delete=models.CASCADE)
    userTag_id  = models.ForeignKey(UserTag, on_delete=models.CASCADE)

# хранит дату удаления пользователя
# по истечении 3-ёх дней пользователь удаляется
class UserRemoveDate(models.Model):
    user_id     = models.ForeignKey(User, on_delete=models.CASCADE)
    remove_date = models.DateTimeField()
    