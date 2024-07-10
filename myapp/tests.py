from django.test import TestCase
from .models import stationen_ISK_2022

stationen = stationen_ISK_2022.objects.all()

print(stationen)
# Create your tests here.
