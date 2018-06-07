from django.utils.http import is_safe_url
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import SamlUser
from .forms import SamlRequestForm

import json

from onelogin.saml2.auth import OneLogin_Saml2_Auth

def _clean_next_url(next_url):
    if is_safe_url(next_url):
        return next_url.strip()
    else:
        return settings.LOGIN_URL

def auth(request):
    if 'next' in request.GET:
        next_url = _clean_next_url(request.GET['next'])
    else:
        next_url = settings.LOGIN_URL
    saml_request_form = SamlRequestForm()
    saml_request_form.fields['next'].initial = next_url
    context = {
        'next_url': next_url,
        'auth_url': settings.LOGIN_URL,
        'saml_request_form': saml_request_form,
    }
    return render(request, 'ecsswebauth/auth.html', context)

def _get_request_for_saml(request):
    result = {
        'https': 'on' if request.is_secure() else 'off',
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        'server_port': request.META['SERVER_PORT'],
        'get_data': request.GET.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'post_data': request.POST.copy()
    }
    return result

def _init_saml(request):
    auth = OneLogin_Saml2_Auth(_get_request_for_saml(request), custom_base_path=settings.SAML_FOLDER)
    return auth

def _get_user_info_from_attributes(attributes):
    userinfo = {
        'username': attributes['http://schemas.microsoft.com/ws/2008/06/identity/claims/windowsaccountname'][0],
        #'groups': attributes['http://schemas.xmlsoap.org/claims/Group'],
        'email': attributes['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress'][0],
        'givenname': attributes['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname'][0],
        'surname': attributes['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname'][0],
    }
    return userinfo

# initiate saml login
@csrf_exempt
def saml_login(request):
    auth = _init_saml(request)
    if 'next' in request.POST:
        next_url = _clean_next_url(request.POST['next'])
    else:
        next_url = settings.LOGIN_URL
    return HttpResponseRedirect(auth.login(next_url))

# sp metadata
def saml_metadata(request):
    auth = _init_saml(request)
    saml_settings = auth.get_settings()
    metadata = saml_settings.get_sp_metadata()
    return HttpResponse(metadata, content_type='application/samlmetadata+xml')

# handle saml login response
@csrf_exempt
def saml_acs(request):
    auth = _init_saml(request)
    auth.process_response()
    errors = auth.get_errors()
    if not errors:
        if auth.is_authenticated():
            userinfo = _get_user_info_from_attributes(auth.get_attributes())
            user = authenticate(username=userinfo['username'], email=userinfo['email'], givenname=userinfo['givenname'], surname=userinfo['surname'])
            login(request, user)
            if 'RelayState' in request.POST:
                return HttpResponseRedirect(request.POST['RelayState'])
            else:
                return HttpResponse('Logged in')
        else:
            return HttpResponse('Not authenticated')
    else:
        return HttpResponse('Error: {}'.format(join(', ', errors)))

# initiate logout
@csrf_exempt
def saml_logout(request):
    auth = _init_saml(request)
    logout(request)
    return HttpResponseRedirect(auth.logout())

@login_required
def saml_test(request):
    return HttpResponse((request.user.samluser.is_persistent))
