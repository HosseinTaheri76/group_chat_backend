from string import ascii_letters, digits
from random import choice
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

def generate_code():
    source = ascii_letters + digits
    return ''.join(choice(source) for _ in range(10))


class ChatGroup(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_chat_groups')
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=10, default=generate_code, db_index=True)

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return self.user.username

    @property
    def group_code(self):
        return self.group.code

    @property
    def group_name(self):
        return self.group.name


class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages')
