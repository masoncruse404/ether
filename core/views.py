from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .forms import RegistrationForm
from django.shortcuts import render
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .signals import user_logged_in
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .forms import UserLoginForm
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
User = get_user_model()

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'core/createaccount.html'




def indexView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        data = request.POST.copy()
        email = data.get('email')
        print('email', email)
        newu = User.objects.filter(email=email)
        print('newu ',newu)
        if(newu):
          print('exists')
          form = RegistrationForm()
          warningmsg = email + ' is already taken'
          context = {"alert":1,"warningmsg":warningmsg, 'form':form}
          return render(request, 'core/createaccount.html', context)
        if form.is_valid():
              print('does not exist')
              CustomUser = form.save()
            # Do something with the user
              messages.success(request, 'User saved successfully.')
              success_url = reverse_lazy('login')

        else:
            messages.error(request, 'The form is invalid.')

        return render(request, 'core/login.html', {'form': form})

    else:
        form = RegistrationForm()
        return render(request, 'core/createaccount.html', {'form': form})


#adding Q object to allow complex 'OR' lookups

def validate_username(request):
    username = request.GET.get('username', None)

    #result checks if the username has an account
    result = User.objects.filter(email__contains=username).exists() | User.objects.filter(email__exact=username).exists()

    if(result):
            user = User.objects.filter(email__contains=username)[0]
            request.session['userid'] = user.id
    print(username)
    data = {
        'is_taken': result
    }
    return JsonResponse(data)

@csrf_exempt
def user_login(request):
    print('in dis hoe')
    context = RequestContext(request)
    authentication_form = UserLoginForm
    form = UserLoginForm
    try:
      uid = request.session['userid']
    except KeyError:
      return render(None,'core/login.html', {'form':form})
    user = User.objects.get(id=uid)
    print('username',user.firstname)
    username = user.firstname
    initial = user.firstname[0]
    initial = initial.upper()
    print(initial)
    print('again'+str(user))
    if request.method == 'POST':
          username = str(user)
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  user_logged_in.send(user.__class__,instance=user,request=request)
                  # Redirect to index page.
                  return HttpResponseRedirect("/users/")
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("Your account is disabled.")
          else:
              # Return an 'invalid login' error message.
              print  ("invalid login details " + username + " " + password)
              return render(None,'core/login.html', {'form':form})
    else:
        # the login is a  GET request, so just show the user the login form.
        return render(None,'core/loginpw.html', {'form':form, 'user':user, 'initial':initial,'username':username})





def handler404(request, *args, **argv):
    response = render('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, 'core/500.html', {})

    response.status_code = 500
    return response



def changename(request):
    if request.method == 'POST':
        searchq = request.GET.get('qname', None)
        print('searchqqq',searchq)
        request.user.name = searchq
        request.user.save()
       
    else:
        pass
    return render(request, 'core/changename.html')


def accountview(request):
    print('in account view')
   
    return render(request, 'core/account.html')