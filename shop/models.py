from django.db import models


from django.utils.timezone import now

# Create your models here.
class Product(models.Model):
    category = models.CharField(max_length=50, default="")
    product_id = models.AutoField
    ad_titel = models.CharField(max_length=50)
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc_product = models.CharField(max_length=300)
    wa_phone = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    pub_date = models.DateTimeField(default=now)
    image = models.URLField()
    popularity = models.IntegerField(default=0)

    def __str__(self):
        return self.ad_titel