from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def main(request):

    return render_to_response('base.html',
                              {'request': request,
                               'user': request.user},
                              context_instance=RequestContext(request))

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            response = redirect('/')
        else:
            # Return a 'disabled account' error message
            response = HttpResponse('user is not active')
    else:
        # Return an 'invalid login' error message.
        response = HttpResponse('user doesnt exist')

    return response

def logout_user(request):
    logout(request)
    return redirect('/')
