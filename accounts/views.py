from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from .models import Profile, Code_payment
from .forms import PaymentForm, GenCodeForm, CodePaymentForm
import requests
from .forms import SignUpForm, UserInformationUpdateForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import JsonResponse

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with username already exists.'
    return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    form_class = UserInformationUpdateForm
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user


@login_required(login_url='/accounts/login/')
def makepayment(request):
    form = CodePaymentForm(request.POST)
    if request.method == 'POST':
        form = CodePaymentForm(request.POST)
        if form.is_valid():
            code = form.save(commit=False)
            submitted_code = request.POST.get("code")

            current_user = request.user
            current_amount = current_user.profile.acc_amount
            amount_entered = list(Code_payment.objects.filter(code=submitted_code).values_list('amount', flat=True))
            for i in amount_entered:
                int_amount = i
                updated_amount = int_amount + int(current_amount)
                Profile.objects.filter(user=current_user).update(acc_amount=updated_amount)
            Code_payment.objects.filter(code=submitted_code).update(used=True)
            messages.success(request, int_amount)
            return redirect('home')
    return render(request, 'make_payment.html',{'form':form})

def gen_code(request):
    code_form = GenCodeForm()
    if request.method == 'POST':
        code_form = GenCodeForm(request.POST)
        if code_form.is_valid():
            code = code_form.save()
            print(code.code)
            pk = code.id
            return redirect(f'/accounts/code/{pk}/')
    return render(request, 'gen_code.html',{'form':code_form})

def code_view(request, pk):
    code = Code_payment.objects.get(id=pk)
    template_name = 'code_view.html'
    return render(request, template_name, {'code':code})