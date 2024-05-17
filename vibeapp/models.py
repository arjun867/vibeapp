from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    class_10_school = models.CharField(max_length=255, null=True, blank=True)
    class_10_passing_year = models.IntegerField(null=True, blank=True)
    class_12_school = models.CharField(max_length=255, null=True, blank=True)
    class_12_passing_year = models.IntegerField(null=True, blank=True)
    college_name = models.CharField(max_length=255, null=True, blank=True)
    expected_graduation_year = models.IntegerField(null=True, blank=True)

    # Specify related_name to avoid clash with auth.User
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        related_name="custom_user_set",
        related_query_name="user",
    )

class BlockedUser(models.Model):
    blocker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocker')
    blocked = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocked')
    blocked_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}: {self.content[:20]}'
    
class VibeMatch(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vibe_match_user1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vibe_match_user2')
    user1_vibe = models.BooleanField(default=False)
    user2_vibe = models.BooleanField(default=False)
    matched = models.BooleanField(default=False)
    
    def check_match(self):
        if self.user1_vibe and self.user2_vibe:
            self.matched = True
        else:
            self.matched = False
        self.save()