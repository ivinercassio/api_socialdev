from django.db import models
from django.conf import settings

class Friend(models.Model):
    friend_one = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friends_initiated'
    )
    friend_two = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friends_received'
    )
    date_start = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('friend_one', 'friend_two')

    def __str__(self):
        return f"Friendship: {self.friend_one.username} & {self.friend_two.username}"

class FriendRequest(models.Model):
    user_one = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_friend_requests'
    )
    user_two = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_friend_requests'
    )
    date_request = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_one', 'user_two')

    def __str__(self):
        return f"Request: {self.user_one.username} -> {self.user_two.username}"