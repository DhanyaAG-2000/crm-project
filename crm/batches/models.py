from django.db import models

from students.models import BaseClass

# Create your models here.

class Batches(BaseClass):



    name = models.CharField(max_length=15)

    start_date = models.DateField()

    expecting_end_date = models.DateField()

    offline_capacity = models.IntegerField()

    online_capacity = models.IntegerField()

    batch_ended = models.BooleanField(default=False)

    ended_on = models.DateField(null=True,blank=True)

    academic_counsellor = models.ForeignKey('academic_councellors.AcademicCounsellors',on_delete=models.SET_NULL,null=True)


    def __str__(self):

        return f'{self.name}'
    
    class Meta:

        verbose_name = 'Batches'

        verbose_name_plural ='Batches'

