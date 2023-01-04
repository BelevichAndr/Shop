from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images/%Y/%m/%d")
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"EmailVerification object for {self.user}"

    def send_verification_email(self):
        link = settings.DOMAIN_NAME + reverse("users:email_verification", kwargs={"email": self.user.email,
                                                                                  "code": self.code})

        subject = f"Подтверждение учетной записи для {self.user.username}"
        message = f"Для потверджения учетной записи {self.user.username} перейдите по ссылке {link}"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False
        )

    def is_expired(self):
        return True if self.expiration <= now() else False
