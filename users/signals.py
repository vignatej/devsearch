from .models import Profile
from django.contrib.auth.models import User


from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
#@receiver(post_save,sender=Profile)
def createProfile(sender, instance : User, created :bool, **kwargs):
    if created:
        user=instance
        profile=Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject='welcome to dev search'
        message='we are glad you are here'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )




def updateuser(sender,instance:Profile,created,**kwargs):
    profile=instance
    user=profile.user
    if created==False:
        user.first_name=profile.name
        user.username=profile.username
        user.email=profile.email
        user.save() 


def deleteuser(sender,instance : Profile, **kwargs):
    try:
        user=instance.user
        user.delete()
    except:
        pass

post_save.connect(createProfile, sender = User)
post_save.connect(updateuser,sender=Profile)
post_delete.connect(deleteuser,sender=Profile)

