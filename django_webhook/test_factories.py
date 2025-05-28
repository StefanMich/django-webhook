import factory

from django_webhook.models import (
    Webhook,
    WebhookEvent,
    WebhookSecret,
    WebhookTopic,
    states,
)
from tests.models import (
    MultiTenantWebhook,
    Tenant,
)


class WebhookSecretFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WebhookSecret

    token = factory.Faker("isbn13")


class WebhookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Webhook

    url = factory.Faker("url", schemes=["https"])
    active = True
    secrets = factory.RelatedFactory(
        WebhookSecretFactory, factory_related_name="webhook"
    )

    @factory.post_generation
    def topics(self, create, extracted, **kwargs):
        self.refresh_from_db()
        if not create:
            return

        if extracted:
            for topic in extracted:
                self.topics.add(topic)  # pylint: disable=no-member


class WebhookTopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WebhookTopic


class WebhookEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WebhookEvent

    webhook = factory.SubFactory(WebhookFactory)
    object = factory.Faker("pydict")
    object_type = factory.Faker("pystr")
    status = factory.Faker("random_element", elements=states.ALL_STATES)
    url = factory.Faker("url")
    topic = factory.Faker("pystr")


class TenantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tenant

    name = factory.Faker("name")


class MultiTenantWebhookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MultiTenantWebhook

    tenant = factory.SubFactory(TenantFactory)
    webhook = factory.SubFactory(WebhookFactory)
