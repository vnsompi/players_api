from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.forms import ValidationError

class CustomUserManager(BaseUserManager):

    def get_object_by_public_id(self, public_id):

        try:
            instance = self.get(public_id=public_id)

            return instance

        except ObjectDoesNotExist:
            raise Http404("Public ID does not exist")

        except (ValueError, TypeError):
            raise Http404("Invalid public ID")


    def create_user(self, email, first_name, last_name,password=None , **fields):

        if email is None:
            raise ValueError('The email must be set')
        if first_name is None:
            raise ValueError('The first name must be set')
        if last_name is None:
            raise ValueError('The last name must be set')

        email = self.normalize_email(email)

        user = self.model(email=email, first_name=first_name,last_name=last_name,**fields)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)


        self.create_user(email=email, first_name=first_name, last_name=last_name, password=password, **extra_fields)