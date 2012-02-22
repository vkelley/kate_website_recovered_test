from django.db import models
from django.contrib.auth.models import User

from userena.models import UserenaBaseProfile

from core.models import ContentArea, Level

class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User)
    levels = models.ManyToManyField(Level, blank=True)
    content_areas = models.ManyToManyField(ContentArea, blank=True)