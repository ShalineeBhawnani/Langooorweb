import datetime
import json
import django
import jwt
from django.template.loader import render_to_string
from pyee import BaseEventEmitter 
from pymitter import EventEmitter
from lib.emitter import ee
from validate_email import validate_email
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from rest_framework.views import APIView
from project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from snippets.token import token_activation,token_validation,account_activation_token
from rest_framework.response import Response
from .serializers import EmailSerializer,LoginSerializer, RegistrationSerializer, UserSerializer,ResetPasswordSerializers
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from django.http import HttpResponse, HttpResponseRedirect , response
from jwt import ExpiredSignatureError
from project.settings import SECRET_KEY
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User, auth
User = get_user_model
from django.db.models import Q
from project import redis_class
rdb = redis_class.Redis()


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

User = get_user_model()

class Login(GenericAPIView):

    serializer_class = LoginSerializer

    # def get(self, request):
    #     return render(request, 'login.html')

    
    def post(self, request):
        print("hello")
        # permission_classes = [permissions.AllowAny]
        if request.user.is_authenticated:
            pass
            #return Response({'details': 'user is already authenticated'})
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        user = authenticate(username=username, password=password)
        print(user)
        qs = User.objects.filter(
            Q(username__exact=username) or
            Q(email__iexact=email)
        ).distinct()
        print(qs)
        if qs.count() == 1:
            user_obj = qs.first()
            print(user_obj)
            if user_obj.check_password(password):
                user = user_obj
                print(user)
                login(request, user)
                print(user)
                token = token_activation(username, password)
                print("token", token)
                #cache.set(user.username, token)
                #print(cache.get(user.username))
                rdb.set(user.username, token)
                rdb.get(token)
                return Response({'details': 'user succesfully loggedin,thakyou'})
            return Response("incorrect password")
        return Response("user name alredy used")

class Registrations(GenericAPIView):

    serializer_class = RegistrationSerializer

    # def get(self, request):
    #     return render(request, 'registration.html')
        
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
            #return Response("your are already registred")
        data = request.data     
        name = data.get('name')
        username = data.get('username') 
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            return Response("passwords are not matching")
        qs_name = User.objects.filter(
            Q(username__iexact=username)
        )
        qs_email = User.objects.filter(
            Q(email__iexact=email)
        )
        if qs_name.exists():
            return Response("already user id present with this username ")
        elif qs_email.exists():
            return Response("already user id present with this  email")
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            domain = current_site.domain 
            print(current_site)
            print('domain:', domain)                
            token = token_activation(username, password)
            print('return from tokens.py:', token)
            cache.set(username, token)
            print("stroged token in cache:  ",cache.get(username))
            url = str(token)
            print('url is ',  url)
            surl = get_surl(url)
            print(surl)
            z = surl.split("/")
            print("the z value is", z)
            print("z[2] line printed :", z[2])
            mail_subject = "Activate your account clicking on the link below"
            message = render_to_string('email_validation.html', {
                    'user': user.username,
                    'domain': domain,
                    'surl': z[2]
                })
            print(message)
            
            email = EmailMessage(mail_subject, message, to=[email])
            email.send()
            print('confirmation mail sent')
            return Response({"details": "please verify through your email"})

class ForgotPassword(GenericAPIView):
 
    serializer_class = EmailSerializer

    # def get(self, request):
    #     return render(request,'forgot_password.html')

    def post(self, request):

        global response
        email = request.data["email"]
        smd = {
            'success': False,
            'message': "not a vaild email ",
            'data': []
        }
        try:
            if email == "":
                response = 'email field is empty please provide vaild input'
            else:

                try:
                    validate_email(email)
                except Exception:
                    return HttpResponse(json.dumps(smd))
                try:
                    print(email)
                    user = User.objects.filter(email=email)
                    useremail = user.values()[0]["email"]
                    username = user.values()[0]["username"]
                    user_id = user.values()[0]["id"]

                    if useremail is not None:
                        token = token_activation(username, user_id)
                        url = str(token)
                        surl = get_surl(url)
                        z = surl.split("/")

                        mail_subject = "Activate your account by clicking below link"
                        mail_message = render_to_string('reset_password_token.html', {
                            'user': username,
                            'domain': get_current_site(request).domain,
                            'surl': z[2]
                        })
                        recipientemail = email
                        
                        email = EmailMessage(mail_subject, mail_message, to=[recipientemail])
                        email.send()
                        response = {
                            'success': True,
                            'message': "check email for vaildation ",
                            'data': []
                        }

                except Exception as e:
                    response = smd['message'] = "not a registered user",
        except Exception:
            smd['message'] = "not a registered user",

        return HttpResponse(json.dumps(response))


def activate(request, surl):
    print("Activate url is ", surl)   
    try:
        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        if user is not None:
            user.is_active = True
            user.save()
            messages.info(request, "your account is active now")
            return redirect('login')        
        else:           
            messages.info(request, 'was not able to sent the email')          
            return redirect('registration')
    

    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('registration')
     
def reset_password(request, surl):
    try:
        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        print("user",user)

        if user is not None:
            context = {'userReset': user.username}
            print(context)
            return redirect('/resetpassword/' + str(user)+'/')
        else:
            messages.info(request, 'was not able to sent the email')
            return redirect('/api/forgotpassword')
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('/api/forgotpassword')
    except Exception as e:
        print(e)
        messages.info(request, 'activation link expired')
        return redirect('/api/forgotpassword')


class ResetPassword(GenericAPIView):
    serializer_class = ResetPasswordSerializers

    def post(self, request, user_reset):
        password1 = request.data['password']

        if user_reset is None:
            return Response({'details': 'not a valid user'})
        elif (password1 or password2) == "":
            return Response({'details': 'password should not be empty'})
            # elif (password1 != password2):
            #     return Response({'details': 'password are should match'})
        else:
            try:
                user = User.objects.get(username=user_reset)
                user.set_password(password1)
                user.save()
                return Response({'details': 'your password has been Reset'})
                #messages.info(request, "your password has been reset")
                #return redirect('/login')
            except Exception:
                return Response({'details': 'not a valid user'})


def session(request):
    """
    if user seeion is closed
    redirect user to session page
    """
    return render(request, 'session.html')


class Logout(GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request):
        try:
            user = request.user
            logout(request)
            #cache.delete(user.username)
            rdb.delete(user.username)
            return Response({'details': 'your succefully loggeg out,thankyou'})
        except Exception:
            return Response({'details': 'something went wrong while logout'})

