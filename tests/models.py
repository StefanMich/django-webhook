from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    join_date = models.DateField()
    last_active = models.DateTimeField()


class Tenant(models.Model):
    name = models.CharField(max_length=30)


class MultiTenantWebhook(models.Model):
    webhook = models.ForeignKey('Webhook', on_delete=models.CASCADE)
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)


class FilteredUser(User):
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)

    @classmethod
    def webhook_filter(cls, instance):
        return {'tenant': instance.tenant}


class Country(models.Model):
    name = models.CharField(max_length=30)


class ModelWithFileField(models.Model):
    """
        The FileField can't be encoded with JSON.
    https://github.com/danihodovic/django-webhook/issues/35
    """

    file = models.FileField()
