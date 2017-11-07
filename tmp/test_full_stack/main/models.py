from django.db import models


class Plan(models.Model):
    number_of_products = models.IntegerField()
    crawls_per_month = models.IntegerField()
    final_price = models.FloatField()

    def __str__(self):
        return str(self.id)


class AccountConnector(models.Model):
    connected_accounts = models.IntegerField()
    final_price = models.FloatField()

    def __str__(self):
        return str(self.id)