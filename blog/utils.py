import re
from .tokens import email_verification_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
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

def abuse_detector(title,content,chat_session):
    question_to_ask = "Detect the abusive or vulgur words in above text ignoring lighter words like stupid,idiot,rude and filter other on your own. Give message containing only abusive or vulgur words with all letters in lower case no other things and if no abusive text then just send an empty line"
    message = title + " " + content + "\n" + question_to_ask

    response = chat_session.send_message(message)

    abusive_words = response.text.split()

    return abusive_words

def highlight_abusive_words(text,abusive_words):
    if not abusive_words:
        return text
    
    abusive_words = sorted(set(abusive_words),key=len,reverse=True)

    pattern = r'\b(' + '|'.join(map(re.escape,abusive_words)) + r')\b'

    def replacer(match):
        word = match.group()
        return f'<span style="background-color: yellow; color: red; font-wright: bold;">{word}</span>'
    
    
    highlighted_text = re.sub(pattern,replacer,text,flags=re.IGNORECASE)
    return mark_safe(highlighted_text)



    