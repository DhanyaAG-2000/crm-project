from django.db import models

from students.models import BaseClass

class PaymentStatusChoices(models.TextChoices):

    PENDING="PENDING","PENDING"

    SUCCESS="SUCCESS","SUCCESS"

    FAILED="FAILED","FAILED"



class Payment(BaseClass):

    student=models.OneToOneField('students.Students',on_delete=models.CASCADE)

    amount=models.FloatField()

    status=models.CharField(max_length=20,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    paid_at=models.DateTimeField(null=True,blank=True)


    def __str__(self):

       return f'{self.student.first_name} {self.student.batch.name}'
    
    class Meta :
       
        verbose_name = 'Payments'

        verbose_name_plural = 'Payments'


    


class Transations(BaseClass):

    payment=models.ForeignKey('Payment',on_delete=models.CASCADE)

    rzp_order_id=models.SlugField()

    amount=models.FloatField()

    status=models.CharField(max_length=20,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    transations_at=models.DateTimeField(null=True,blank=True)

    rzp_payment_id=models.SlugField(null=True,blank=True)

    rzp_signature_id=models.TextField(null=True,blank=True)

    def __str__(self):

       return f'{self.payment.student.first_name} {self.payment.student.batch.name} {self.status}'
    
    class Meta :
       
        verbose_name = 'Transactions'

        verbose_name_plural = 'Transactions'

    




    


# Create your models here.

# from students.models import BaseClass

# class PaymentSettleChoices(models.TextChoices):

#     ONE_TIME='ONE TIME','ONE TIME'

#     INSTALLMENTS='INSTALLMENT','INSTALLMENT'

# class InstallmentChoices(models.IntegerChoices):

#     TWO=2,'2'

#     THREE=3,'3'

#     FOUR=4,'4'

#     FIVE=5,'5'
    
#     SIX=6,'6'


# class PaymentStructure(BaseClass):

#     student=models.OneToOneField('students.Students',on_delete=models.CASCADE)

#     one_time_or_installment=models.CharField(max_length=20,choices=PaymentSettleChoices)

#     no_of_installment=models.IntegerField(choices=InstallmentChoices.choices,null=True,blank=True)

#     fee_to_be_paid=models.FloatField()

#     def __str__(self):

#      return f'{self.student.first_name} {self.student.batch.name} '
    
#     class Meta :
       
#        verbose_name = 'Payment structure'
#        verbose_name_plural = 'Payment structure'

#        ordering = ['-id']


