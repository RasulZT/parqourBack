from django.db import models

# Create your models here.
class Chat(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[("group", "Group"), ("private", "Private")])
    object_name = models.CharField(max_length=255, null=True, blank=True)  # Название объекта (ЖК, офис и т.п.)

    def __str__(self):
        return self.title
