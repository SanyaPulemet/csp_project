from django.db import models
from user_app import models as user_app_models
import uuid

# Models

# Файл
class File(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    path        = models.FileField(default="file.*", upload_to="files")
    public_on   = models.BooleanField(default=False)
    link_on     = models.BooleanField(default=False)
    comment_on  = models.BooleanField(default=False)

class Link(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file        = models.ForeignKey(to=File, on_delete=models.CASCADE)

# Страница
class Page(models.Model):
    user        = models.ForeignKey(user_app_models.User, null=False, on_delete=models.CASCADE)
    title       = models.CharField(max_length=50, default="Untitled")
    image       = models.ImageField(default="page/default.jpg", upload_to="page")
    category    = models.CharField(default="other")
    public_on   = models.BooleanField(default=False)
    comment_on  = models.BooleanField(default=False)

# Файл-страница OneToMany (для нескольких фалов на одной странице)
class FilePage(models.Model):
    file        = models.ForeignKey(to=File, null=False, on_delete=models.CASCADE)
    page        = models.ForeignKey(to=Page, null=False, on_delete=models.CASCADE)

# Комментарии
class Comment(models.Model):
    id          = models.UUIDField(primary_key=True, auto_created=True)
    text        = models.CharField(max_length=200)
    datetime    = models.DateTimeField(null=False)
    user        = models.ForeignKey(user_app_models.User, null=False, on_delete=models.CASCADE)
    page        = models.ForeignKey(Page, null=False, on_delete=models.CASCADE)