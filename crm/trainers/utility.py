import uuid
from .models import Trainers

import string

import random

def get_employee_number():

    while True:
         
         pattern = str(uuid.uuid4().int)[:7]

         emplo_number = f'LM-E{pattern}'

         if not Trainers.objects.filter(employee_id = emplo_number).exists():
              
              return emplo_number



#     print(admission_number)

# get_admission_number()

def get_password():
     
    password=''.join(random.choices(string.ascii_letters+string.digits,k=8))

    print(password)

    return password

# get_password()
