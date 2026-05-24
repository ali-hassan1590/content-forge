from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    niche = models.CharField(max_length=100, blank=True)
    credits = models.IntegerField(default=100)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"

    def __str__(self):
        return f"{self.user.username}'s profile"

    def has_credits(self, amount: int) -> bool:
        return self.credits >= amount

    def deduct_credits(self, amount: int) -> bool:
        if not self.has_credits(amount):
            return False
        self.credits -= amount
        self.save(update_fields=["credits"])
        return True
