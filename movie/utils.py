import random
import string
from django.utils.text import slugify
from functools import wraps
from django.http import HttpResponseRedirect
import os

def random_string_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def code_generator(instance, new_code=None):
    if new_code is not None:
        code = new_code
    else:
        code = random_string_generator()
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(code=code).exists()
    if qs_exists:
        new_code = random_string_generator()
        return random_string_generator(instance, new_code=new_code)
    return code


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None: 
        slug = new_slug
    else:
        slug = slugify(instance.title)
    if slug in DONT_USE:
        slug=slug
        randstr=random_string_generator(size=4)
        new_slug = f"{slug}-{randstr}"
        
        return unique_slug_generator(instance, new_slug=new_slug)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

from accounts.models import Profile

def payment_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        current_user = request.user
        if Profile.user == current_user:
            if Profile.acc_amount > 200:
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/accounts/makepayments")
    return wrap

def get_filename(path):
    return os.path.basename(path)

def sliced_name(name):
    lower = name.lower()
    sliced = slice(lower(0,3))
    return sliced

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