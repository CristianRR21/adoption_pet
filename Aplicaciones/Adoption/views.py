from.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login 
from .models import Pet,PetPhoto

# Create your views here.

def iniciarSesion(request):
    return render(request,"login/login.html")

def adoptions(request):
    
    pets= Pet.objects.filter(status='available')
    publications=[]
    for pet in pets:
        image_path=PetPhoto.objects.filter(pet=pet).order_by('order').first()
        publications.append({
            'pet':pet,
            'image_path':image_path
        })
            
        
    return render (request,'adoptions/index.html',{'publications':publications})

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
        first_name = request.POST['first_name']  
        last_name = request.POST['last_name']    
        phone = request.POST['telefono']
        address = request.POST['direccion']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

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
    return render(request,'adoptions/newAdoptions.html')

def nuevaPublicacion(request):
    return render(request,'adoptions/newPublication.html')

def savePublication(request):
    
    if request.user.is_authenticated:    
        name=request.POST['name']
        species=request.POST['species']
        breed=request.POST['breed']
        age=request.POST['age']
        gender=request.POST['gender']
        color=request.POST['color']
        description=request.POST['description']
        image_path= request.FILES.getlist('image_path[]')   
        publisher_id= request.user.id
        
        pet = Pet.objects.create(
            name=name,
            species=species,
            breed=breed,
            age=age,
            gender=gender,
            color=color,
            description=description,
            publisher_id=publisher_id
        )
        user= User.objects.get(id=request.user.id)
        user.num_publications +=1
        user.role = 'owner'
        user.save()
    
        for index,photo in enumerate(image_path,start=1):
            PetPhoto.objects.create(
                image_path=photo,
                pet =pet,
                order=index
                     
            )
            
            
            
        messages.success(request,"Mascota registrada correctamente")
        return redirect('/')
        
    else:
        return redirect('/iniciarSesion')

    

    

def misPublicaciones(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        pets= Pet.objects.filter(publisher_id=user_id)
        publications=[]
        for pet in pets:
            image_path=PetPhoto.objects.filter(pet=pet).order_by('order').first()
            publications.append({
                'pet':pet,
                'image_path':image_path
            })
                
            
        return render (request,'adoptions/myPublications.html',{'publications':publications})
    
    else:
        return redirect('/iniciarSesion')
