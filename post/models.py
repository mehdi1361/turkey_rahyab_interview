from django.db import models
from base.models import Base
from user.models import UserAccount
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Announcement(Base):
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(UserAccount, null=True, on_delete=models.SET_NULL, related_name="announcements")
    picture = models.ImageField(null=True, upload_to="images/", blank=True, verbose_name="Category picture")
    medium_picture = ImageSpecField(source='picture', processors=[ResizeToFill(150, 150)], format="PNG",
                                      options={'quality': 80})

    small_picture = ImageSpecField(source='picture', processors=[ResizeToFill(80, 80)], format="PNG",
                                      options={'quality': 80})
    class Meta:
        db_table = "announcement"
