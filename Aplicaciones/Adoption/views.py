from.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login 
from .models import Pet,PetPhoto,Adoption
from django.contrib.auth import logout
import json
from django.db.models import Count, Q


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
    
       
    total_usuarios = User.objects.count()
    total_adoptantes = User.objects.filter(role='adopter').count()
    total_publicadores = User.objects.filter(role='owner').count()
    
    
    
    total_mascotas = Pet.objects.count()
    disponibles = Pet.objects.filter(status='available').count()
    adoptadas = Pet.objects.filter(status='adopted').count()
    
    
    #total_adopciones = Adoption.objects.count()
    pendientes = Adoption.objects.filter(status='pending').count()
    aprobadas = Adoption.objects.filter(status='approved').count()
    rechazadas = Adoption.objects.filter(status='reject').count()
    
    grafico_usuarios = [total_adoptantes, total_publicadores]
    grafico_mascotas = [disponibles, adoptadas]
    grafico_adopciones = [pendientes, aprobadas, rechazadas]
     #usarios 
    usuarios_top = (
    User.objects.annotate(
        total_adopciones=Count(
            'adoption',
            filter=Q(adoption__status='approved')
        )
    )
    .filter(total_adopciones__gt=0)
    .order_by('-total_adopciones')[:5]
    )
    context = {
        'total_usuarios': total_usuarios,
        'total_adoptantes': total_adoptantes,
        'total_publicadores': total_publicadores,
        'total_mascotas': total_mascotas,
        'disponibles': disponibles,
        'adoptadas': adoptadas,
        #'total_adopciones': total_adopciones,
        'pendientes': pendientes,
        'aprobadas': aprobadas,
        'rechazadas': rechazadas,
        'grafico_usuarios_json': json.dumps(grafico_usuarios),
        'grafico_mascotas_json': json.dumps(grafico_mascotas),
        'grafico_adopciones_json': json.dumps(grafico_adopciones),
        'usuarios_top': usuarios_top,
    }
    
   

       
    
    
    return render(request,"administrator/index.html",context)

   
    



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
        pets = Pet.objects.filter(publisher_id=user_id)
        publications = []

        for pet in pets:
            foto = PetPhoto.objects.filter(pet=pet).order_by('order').first()
            publications.append({
                'pet': pet,
                'foto': foto
            })
                
        return render(request, 'adoptions/myPublications.html', {
            'publications': publications
        })
    
    else:
        return redirect('/iniciarSesion')



def editarPublicacion(request, id):
    pet = Pet.objects.get(id=id)
    fotos = PetPhoto.objects.filter(pet=pet)
    return render(request, 'adoptions/editPublication.html', {
        'pet': pet,
        'fotos': fotos  
    })

    

def processEditPublication(request):
    
    if request.user.is_authenticated:    
        pet_id=request.POST['id']
        name=request.POST['name']
        species=request.POST['species']
        breed=request.POST['breed']
        age=request.POST['age']
        gender=request.POST['gender']
        color=request.POST['color']
        description=request.POST['description']
        image_path= request.FILES.getlist('image_path[]')   
        publisher_id= request.user.id
        
        pet=Pet.objects.get(id=pet_id)
        pet.name=name
        pet.species=species
        pet.breed=breed
        pet.age=age
        pet.gender=gender
        pet.color=color
        pet.description=description
        pet.save()
                
        if image_path:
            existing_photos = PetPhoto.objects.filter(pet=pet)
            for photo in existing_photos:
                if photo.image_path:
                    photo.image_path.delete(save=False)  
                photo.delete()  

            for index, image in enumerate(image_path, start=1):
                PetPhoto.objects.create(
                    pet=pet,
                    image_path=image,
                    order=index
                )
            
            
        messages.success(request,"Mascota actualizada correctamente")
        return redirect('/')
        
    else:
        return redirect('/iniciarSesion')

    


def eliminarPublicacion(request, id):
    if request.user.is_authenticated:
        pet = Pet.objects.get(id=id, publisher=request.user)

        fotos = PetPhoto.objects.filter(pet=pet)

        for foto in fotos:
            if foto.image_path:
                foto.image_path.delete(save=False)
            foto.delete()

        usuario = pet.publisher  

        pet.delete()

        if usuario.num_publications > 0:
            usuario.num_publications -= 1
            usuario.save()

        messages.success(request, "Mascota eliminada correctamente.")
        return redirect('/misPublicaciones')
    else:
        return redirect('/iniciarSesion')
    
    
def approvedAdoption(request, id):
    if request.user.is_authenticated:
        adoption = Adoption.objects.get(id=id)     
        adoption.status= 'approved'
        adoption.save()
        
        pet= adoption.pet
        pet.status = 'adopted'
        
        pet.save()
        
        messages.success(request, "Adopcion aprobada correctamente.")
        return redirect('/adopcionesPendientes')
    else:
        return redirect('/iniciarSesion')
    
def rejectAdoption(request, id):
    if request.user.is_authenticated:
        adoption = Adoption.objects.get(id=id)     
        adoption.status= 'reject'
        adoption.save()
        
        pet= adoption.pet
        pet.status = 'available'
        
        pet.save()
        
        messages.success(request, "Adopcion aprobada correctamente.")
        return redirect('/adopcionesPendientes')
    else:
        return redirect('/iniciarSesion')
    
    
def cerrarSesion(request):
    logout(request)
    return redirect('/')
    
def adoptar(request,id):
    user = request.user
    pet = Pet.objects.get(id=id)
    photos = PetPhoto.objects.filter(pet=pet)
    return render(request,'adoptions/newAdoption.html',{'pet':pet,'photos':photos,'user':user})

def saveAdoption(request):
    if request.user.is_authenticated:    
        pet_id= request.POST['pet']
        contract_path = request.FILES.get('contract')  
        status= 'pending'        
        adopter_id= request.user.id
        
        adoption = Adoption.objects.create(
            contract_path=contract_path,
            pet_id=pet_id,
            adopter_id=adopter_id,
            status=status
        ) 
        
        pet=Pet.objects.get(id=pet_id)
        pet.status='pending'
        pet.save()
        messages.success(request, "Su solicitud ha sido enviada correctamente.")    
        return redirect('/')
    else:
        return redirect('/iniciarSesion')





def listadoMascotas(request):
    pets=Pet.objects.all()
    listPets=[]
    
    for pet in pets:
            foto = PetPhoto.objects.filter(pet=pet).order_by('order').first()
            listPets.append({
                'pet': pet,
                'foto': foto
            })
    
    return render(request,'administrator/listPets.html',{'pets':listPets})


def listadoUsuarios(request):
    listUsers=User.objects.all()
    return render(request,'administrator/listUsers.html',{'users':listUsers})

def adopcionesPendientes(request):
    listPendingAdoption=Adoption.objects.filter(status='pending')
    return render(request,'administrator/listPendingAdoptions.html',{'listPending':listPendingAdoption})

def adopcionesFinalizadas(request):
    listFinalAdoption = Adoption.objects.exclude(status='pending')
    return render(request,'administrator/listFinalAdoptions.html',{'listFinal':listFinalAdoption})
