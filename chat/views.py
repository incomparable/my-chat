from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

from chat.models import Message


class IndexView(View):
    def get(self, request):
        logout(request)
        return render(request,
                      'index.html',
                        )

class Register(View):
    def get(self, request):
        return render(request,
                      'register.html')

    def post(self, request):
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['email'],
                                            password=request.POST['password1'])
                login(request, user)
            except:
                return redirect('exists/')
            users = User.objects.all()
            users_list = []
            for i in users:
                if i.username != request.user.username:
                    users_list.append(i.username)
            return render(request, 'after_log_in.html', {'users_list': users_list})
        else:
            return redirect('/')


class Logout(View):

    def get(self,request):
        logout(request)
        return render(request,
                      'index.html',
                      )


class LoginView(View):
    def get(self, request):
        return render(request,
                      'login.html')

    def post(self,request):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username = username, password=password)
        if user is not None:
            print(user)
            login(request,user)
            users = User.objects.all()
            users_list = []
            for i in users:
                if i.username != request.user.username:
                    users_list.append(i.username)
            return render(request, 'after_log_in.html', {'users_list': users_list})
        else:
            return redirect('not_found/')



class AfterLogin(View):
    def get(self, request):
        if request.user.username:
            print(request.user)
            users = User.objects.all()
            users_list = []
            for i in users:
                if i.username != request.user.username:
                    users_list.append(i.username)

            return render(request, 'after_log_in.html', {'users_list': users_list})
        else:
            return redirect("/log_in/")

    def post(self,request):

        receiver = request.POST['hidden_receiver']
        creator = request.user.username
        message_1 = list(reversed(Message.objects.all().filter(creator=creator, receiver=receiver)))
        message_2 = list(reversed(Message.objects.all().filter(creator=receiver, receiver=creator)))
        message_3 = message_1 + message_2
        message_pk = []
        message_to_show = []
        for i in message_3:
            message_pk.append(i.pk)
            message_pk.sort(reverse=True)

        for i in message_pk:
            for j in message_3:
                if i == j.pk:
                    message_to_show.append(j)
        return render(request, 'chat.html', {'receiver':receiver, 'message': message_to_show})

class NotFoundView(View):
    def get(self, request):
        return render(request, 'not_found.html')

class ExistsView(View):
    def get(self, request):
        return render(request, 'exists.html')



class MessageView(View):
    def post(self, request):
        receiver1 = request.POST.get('receiver_1')
        creator1 = request.POST.get('creator_1')
        message1 = request.POST.get('message1')

        Message.objects.create(creator = creator1, receiver=receiver1, message=message1)
        message_1 = list(reversed(Message.objects.all().filter(creator=creator1, receiver=receiver1)))
        message_2 = list(reversed(Message.objects.all().filter(creator=receiver1, receiver=creator1)))
        message_3 = message_1 + message_2
        message_pk = []
        message_to_show=[]
        for i in message_3:
            message_pk.append(i.pk)
            message_pk.sort(reverse=True)

        for i in message_pk:
            for j in message_3:
                if i == j.pk:
                    message_to_show.append(j)

        return render(request, 'chat.html',{'message':message_to_show,'receiver':receiver1})

