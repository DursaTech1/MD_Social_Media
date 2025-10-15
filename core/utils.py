# core/utils.py
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_welcome_email(user_email, username):
    """
    Send a welcome email to new users
    """
    subject = 'Welcome to Our Social Media Platform!'
    
    # HTML message
    html_message = render_to_string('emails/welcome.html', {
        'username': username,
    })
    
    # Plain text version
    plain_message = f"""
    Hi {username},
    
    Welcome to our social media platform! We're excited to have you as part of our community.
    
    Start connecting with friends and sharing your moments!
    
    Best regards,
    The Social Media Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False