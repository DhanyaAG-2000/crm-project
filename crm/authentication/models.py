from django.db import models
from django.contrib.auth.models import  AbstractUser
# Create your models here.
class Rolechoice(models.TextChoices):

    ADMIN='ADMIN','ADMIN'

    STUDENT='STUDENT','STUDENT'

    ACADEMIC_COUNCELLOR='ACADEMIC COUNCELLOR','ACADEMIC COUNCELLOR'

    TRAINER='TRAINER','TRAINER'

    SALES='SALES','SALES'

class Profile(AbstractUser):
    

    role=models.CharField(max_length=30,choices=Rolechoice.choices)

    def __str__(self):

        return f'{self.username} -{self.role}'
    
    class Meta:

        verbose_name='profile'

        verbose_name_plural='profile'