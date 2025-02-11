import factory

from django.contrib.auth import get_user_model

from faker import Faker


User = get_user_model()
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: fake.email())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    is_active = True

    @factory.post_generation
    def activation_code(self, create, extracted, **kwargs):
        self.create_activation_code()

    @staticmethod
    def generate_user_with_missing_fields(missing_fields={'email',}):
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': 'password123',
            'password_confirm': 'password123'
        }

        for missing_field in missing_fields:
            if missing_field in data:
                data.pop(missing_field)
        return data