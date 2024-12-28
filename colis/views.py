from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import Http404
from django.template import loader
from django.contrib.auth.models import User  
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, CreateColisForm, UpdateColisForm, UpdateProfileForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from .models import Colis
from .models import Profile
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone  

def home(request):
    return render(request, 'colis/index.html')  

def register(request):
  
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm() 
    context = {'form': form}
    return render(request, 'colis/register.html', context)  

#login view
@csrf_protect
def login(request):
  form=LoginForm()
  if request.method=="POST" :
    form=LoginForm(request,data=request.POST)
    if form.is_valid():
      username=request.POST.get('username')
      password=request.POST.get('password')
      
      user= authenticate(request,username=username,password=password)
      
      if user is not None: #user exists 
        if user.is_staff:
          auth.login(request,user)
          
          return redirect('dashboard') 
        else:
          auth.login(request,user) 
          
          return redirect('user_dashboard')
      
        
  context={'form':form}
  return render(request, 'colis/login.html', context)

# Dashboard
@login_required(login_url='login')
def dashboard(request):
 
    if request.user.is_superuser:  # Vérifie si l'utilisateur est un administrateur
        all_colis = Colis.objects.all()  # Récupère tous les colis dans la base de données
        return render(request, 'colis/dashboard.html', {'all_colis': all_colis})
    else:
        # Si l'utilisateur n'est pas un administrateur, redirige-le ailleurs
        return redirect('home')

#voir un colis spécifique(admin)
@login_required(login_url='login')
def view_colis(request,pk):
  coli=Colis.objects.get(code=pk)
  context={'coli':coli}
  return render(request,'colis/view_colis.html' ,context)

#livré un colis (admin)
@login_required(login_url='login')
def accept_colis(request, pk):
    coli = Colis.objects.get(code=pk)
    coli.status = 'livré'  # Utiliser l'instance récupérée
    coli.date_distribution = timezone.now() #zedtha jdida
    coli.save()  
    messages.success(request, "Colis accepté !")
    return redirect("dashboard")

#anuulation d'un colis ( admin)
@login_required(login_url='login')
def refuse_colis(request,pk):
  coli = Colis.objects.get(code=pk)
  coli.status='annulé'
  coli.date_distribution = timezone.now()
  coli.save()
  messages.success(request , "Colis annulé!")
  return redirect("dashboard")  
  

#admin view profile

@login_required(login_url='login')
def admin_view_profiles(request):
    if not request.user.is_superuser:  
        return redirect('home')  

    profiles = Profile.objects.all()  
    return render(request, 'colis/admin_view_profiles.html', {
        'profiles': profiles,
    })


#admin delete profile

@login_required(login_url='login')
def admin_delete_user(request, username):
    # Récupère l'utilisateur avec le username
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
       
        user.delete()  
        messages.success(request, 'Le compte a été supprimé avec succès.')
        return redirect('admin_view_profiles')

    return render(request, 'colis/admin_delete_confirmation.html', {'client_user': user})
   

# User Dashboard

@login_required(login_url='login')
def user_dashboard(request):
    user_colis = Colis.objects.filter(user=request.user) #shows colis of that specific user
    context={'user_colis':user_colis}

    return render(request, 'colis/user_dashboard.html', context)


#view a specific colis(user)
@login_required(login_url='login')
def user_view_colis(request,pk):
  user_coli=Colis.objects.get(code=pk)
  context={'user_coli':user_coli}
  return render(request,'colis/user_view_colis.html' ,context)


# ajouter un  colis (Create)
@csrf_protect
@login_required(login_url='login')
def create_colis(request):
  form=CreateColisForm()
  if request.method == "POST":
    form=CreateColisForm(request.POST)
    
    if form.is_valid():
      new_colis = form.save()
      new_colis.user = request.user  
      new_colis.date_envoi = timezone.now()
      new_colis = form.save()
      messages.success(request, 'Le colis a été créé avec succès.')
      return redirect("user_dashboard")    
      
  context={'form':form}
  
  return render(request,'colis/new_colis.html',context)


#modifier un colis (update) 

@login_required(login_url='login')
def update_colis(request, pk):
    my_colis = Colis.objects.get(pk=pk) 
    

    if my_colis.status == 'livré':
            messages.error(request, "Ce colis a déjà été livré et ne peut pas être modifié.")
            return redirect("user_dashboard")

    if request.method == 'POST':
        form = UpdateColisForm(request.POST, instance=my_colis)
        if form.is_valid():
            update_colis.date_envoi = timezone.now()
            form.save()
            messages.success(request, "Ton colis a été modifié !")
            return redirect("user_dashboard")
    else:
        form = UpdateColisForm(instance=my_colis)
    
    context = {'form': form}
    
   
    return render(request, 'colis/update_colis.html', context)

#supprimer un colis(Delete)
@login_required(login_url='login')
def delete_colis(request, pk):
    try:
        my_colis = Colis.objects.get(pk=pk)  
    except Colis.DoesNotExist:
        raise Http404("Colis non trouvé")  

    if request.method == 'POST':
        my_colis.delete()  
        messages.success(request, "Ton colis a été supprimé !")
        return redirect("user_dashboard")

    context = {'colis': my_colis}  
    return render(request, 'colis/delete_colis.html', context)

#voir un compte (client)
def view_account(request):
    try:
        profile = Profile.objects.get(user=request.user)  
    except Profile.DoesNotExist:
        profile = None  

    return render(request, 'colis/view_account.html', {
        'user': request.user,
        'profile': profile,  
    })


#modifier un  profile
@login_required
def update_profile(request):
    user = request.user
    profile = user.profile  

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view_account')  
    else:
        form = UpdateProfileForm(instance=user)
        form.fields['phone_number'].initial = profile.phone_number  

    return render(request, 'colis/update_profile.html', {'form': form})

#supprimer profile (Delete)
@login_required(login_url='login')
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  
        user.delete()    
        return redirect('home')  

    return render(request, 'colis/delete_confirmation.html')  


# se déconnecter
def logout(request):
    auth_logout(request)  
    return redirect('login')  
