from django.contrib.auth.models import AbstractUser  # new 
from django.db import models

# new
class User(AbstractUser):
    pass
