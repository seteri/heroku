import random

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.conf import settings

from users.models import MyUser


def send_confirmation_email(email):
    otp = random.randint(1000, 9999)
    subject = f'ვერიფიკაციის იმეილი'
    message = f'თქვენი კოდი {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    user_obj = MyUser.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()




def send_password_reset_instruction(email, token_id):
    print(token_id)

    subject = f'პაროლის შეცვლის ინსტრუქცია'
    message = f'დააკლიკეთ ღილაკს რომ შეცვალოთ პაროლი : http://localhost:5173/auth/recover2/{token_id}/'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])






