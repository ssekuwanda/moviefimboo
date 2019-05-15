from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from movie.utils import random_string_generator, code_generator
from django.urls import reverse
from django.dispatch import receiver

Gender = (
        ('Female','female'),
        ('Male','male'),
)

import random
def sliced_name(name):
    lower = name.lower()
    return lower[0:4]
def referal_code_generator(instance, new_referal_code=None):
    if new_referal_code is not None: 
        referal_code = new_referal_code
    else:
        referal_code = sliced_name(instance.user.username)+str(random.randint(10,100))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(referal_code=referal_code).exists()
    if qs_exists:
        new_referal_code = sliced_name(instance.user.username)+str(random.randint(10,100))
        return referal_code_generator(instance, new_referal_code=new_referal_code)
    return referal_code

class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        phone_number = models.IntegerField(blank=True, null=True)
        acc_amount = models.IntegerField(default=1000)
        gender = models.CharField(max_length=12, choices=Gender, null=True, blank=True)
        activated = models.BooleanField(default=False)
        referal_code = models.CharField(max_length=6, null=True, blank=True, unique=True)
        refered_code = models.CharField(max_length=6, null=True, blank=True)

        def __str__(self):
                return str(self.user )+ '-' + '0'+str(self.phone_number) + '-' + str(self.acc_amount)+'/='

@receiver(post_save, sender=User)
def user_profile(sender, instance, created, **kwargs):
        if created:
                Profile.objects.create(user=instance)
        instance.profile.save()

def code_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.referal_code:
        instance.referal_code = referal_code_generator(instance)

pre_save.connect(code_pre_save_receiver, sender=Profile)

class Payments(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        phone_number = models.IntegerField(blank=True, null=True)
        amount = models.IntegerField(default=1000)
        verified_payment = models.BooleanField()
        timestamp = models.DateTimeField(auto_now_add=True, null=True)

        def __str__(self):
                return self.user - str(self.amount)


def user_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_post_save_receiver, sender=User)


class Code_payment(models.Model): #Each code costs 1k
        code = models.CharField(max_length=6, null=True, blank=True)
        amount = models.PositiveIntegerField()
        used = models.BooleanField(default=False)
        timestamp = models.DateTimeField(auto_now_add=True, null=True)        

        def __str__(self):
                if self.used == False:
                        return str(self.code)+ '-' + 'Not used'
                else:
                        return str(self.code)+ '-' + 'Used'

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.code:
        instance.code = code_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=Code_payment)

class Amount(models.Model):
        movie_amount = models.PositiveIntegerField()
        serie_amount = models.PositiveIntegerField()

        def __str__(self):
                return 'Movie'+'-'+str(self.movie_amount)+' & Serie'+'-'+str(self.serie_amount)