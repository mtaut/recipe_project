# creating the view for user login and authentication
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout # django authentication libraries
from django.contrib.auth.forms import AuthenticationForm #django form for authentication

# THIS IS THE LOGIN/LOGOUT VIEW LOGIC

def login_view(request):
    error_message = None
    form = AuthenticationForm()

    # POST request generated when user selects login button
    if request.method == 'POST':
        # read the data sent by the form via POST request
        form = AuthenticationForm(data=request.POST)

        # check if form is valid
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            #  use Django authenticate to validate user
            user = authenticate(username=username, password=password)
            if user is not None:
                # if user us authenticated then use pre-defined Djanjo function to login
                login(request, user)
                # send user to desired page
                return redirect('recipes:recipes_list')
            
        else:
            error_message = 'Oops, something went wrong'

    # prepare data to send from view to template
    context = {
        'form': form,
        'error_message': error_message
    }
    # load login page using "context" information
    return render(request, 'auth/login.html', context)

def logout_view(request):
    # use predefined Django logout function
    logout(request)
    # navigate user to login form after logging out
    return render(request, 'auth/success.html')