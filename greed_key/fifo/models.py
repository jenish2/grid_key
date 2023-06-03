from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Transaction(BaseModel):
    date = models.DateField()
    transaction_type = models.CharField(max_length=5)
    quantity = models.IntegerField(default=None)
    price = models.FloatField(default=None)
    ratio = models.IntegerField(default=None)

    class Meta:
        abstract = False
        app_label = 'fifo'
