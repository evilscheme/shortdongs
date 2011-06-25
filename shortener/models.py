from django.db import models

from dongbits import dong_to_int, int_to_dong

# Create your models here.

class URL(models.Model):
    url = models.CharField(max_length=4096, unique=True)

    def as_dong(self):
        return int_to_dong(self.id)
