from.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login 

# Create your views here.

def iniciarSesion(request):
    return render(request,"login/login.html")

def adoptions(request):
    return render(request,"adoptions/index.html")

def registerUser(request):
    return render(request,"login/register_user.html")

def administrador(request):
    return render(request,"administrator/index.html")

   
    



def startSesion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Buscar el usuario por email
            usuario = User.objects.get(email=email)

            # Verificar contraseña
            if usuario.check_password(password):
                
                # Iniciar sesión usando Django
                login(request, usuario)

                # Redirigir según rol
                if usuario.role == 'administrator':
                    return redirect('/administrador')
                elif usuario.role == 'adopter':
                    return redirect('/')
                elif usuario.role == 'owner':
                    return redirect('/')
                else:
                    messages.error(request, "Rol desconocido.")
                    return render(request, 'login/login.html')

            else:
                messages.error(request, "Contraseña incorrecta.")
                return render(request, 'login/login.html')

        except User.DoesNotExist:
            messages.error(request, "Correo no registrado.")
            return render(request, 'login/login.html')

    return render(request, 'login/login.html')



def registerNewUser(request):
    if request.method == 'POST': 
        first_name = request.POST.get('first_name')  
        last_name = request.POST.get('last_name')    
        phone = request.POST.get('telefono')
        address = request.POST.get('direccion')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(email=email).exists():
                messages.error(request, "El correo ya está registrado.")
                return render(request, 'login/register_user.html')

        if User.objects.filter(username=username).exists():
                messages.error(request, "El nombre de usuario ya existe.")
                return render(request, 'login/registrarUsuario.html')

        if User.objects.filter(phone=phone).exists():
                messages.error(request, "El número de teléfono ya está registrado.")
                return render(request, 'login/registrarUsuario.html')

        usuario = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            password=make_password(password),  
        )
        usuario.save()
        messages.success(request, "Usuario registrado correctamente.")
        return redirect('/')

    return render(request, 'login/registrarUsuario.html')


def nuevaAdopcion(request):
    return render(request,'adoptions/newAdoptions')

def nuevaPublicacion(request):
    return render(request,'adoptions/newPublication')