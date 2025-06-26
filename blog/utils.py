from .tokens import email_verification_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from BlogProject.settings import EMAIL_HOST_USER

def send_verification_email(user,request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)

    verification_link = request.build_absolute_uri(
        reverse('verify_email_confirm',kwargs={'uidb64':uid,'token':token})
    )

    subject = "Verification Email"
    message = f"Hii {user.username},\nPlease Verify your email by clicking below link:\n{verification_link}"

    send_mail(
        subject,
        message,
        from_email= EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )

    