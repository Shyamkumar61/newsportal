from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME, login, logout, authenticate
from django.views.generic import View, TemplateView, RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import SingUpForm, EditProfile
from django.views import generic
# Create your views here.


class LoginView(View):

    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = get_user_model()
            user = user.objects.get(email=email)
        except:
            messages.success(request, 'User Not Found')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('/')
        else:
            messages.error(request, 'Password Incorrect')
        return render(request, 'account/login.html')


class LogOutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)


class SingupView(generic.CreateView):

    form_class = SingUpForm
    success_url = '/'
    template_name = 'account/singup.html'


# class SingupView(SuccessMessageMixin, generic.CreateView):
#
#     form_class = SingUpForm
#     success_url = '/'
#     template_name = 'account/singup.html'
#     success_message = "Thank you for Registering !!"
#
#     def form_valid(self, form):
#         self.object = form.save()
#         username = self.request.POST['email']
#         password = self.request.POST['password1']
#         print(self.request.POST)
#         redirect_url = self.get_success_url()
#         user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
#         login(self.request, user)
#         messages.success(self.request, 'Thank you for Registering !!')
#         return HttpResponseRedirect(redirect_url)


class ProfileHomeView(TemplateView):

    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileHomeView, self).get_context_data(**kwargs)
        context['user_details'] = self.request.user
        print(context['user_details'])
        return context


class EditProfileView(TemplateView):

    template_name = 'account/edit_profile.html'
    register_form_class = EditProfile

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = self.register_form_class(request.POST, request.FILES, instance=self.request.user)
        if form.is_valid():
            usr = form.save()
            return HttpResponseRedirect('/account/profile')
        context['form'] = form
        return self.register_form_class(context)

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        form = self.register_form_class(instance=self.request.user)
        context['user_details'] = self.request.user
        context['form'] = form
        return context





