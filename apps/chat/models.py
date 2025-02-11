from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    host = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='rooms')
    current_users = models.ManyToManyField(
        User,
        related_name='current_users',
        blank=True
    )

    def __str__(self):
        return f'{self.name} -> {self.host}'


class Message(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='message'
    )
    text = models.TextField()
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)