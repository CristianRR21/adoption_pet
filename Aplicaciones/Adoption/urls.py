from django.urls import path
from.import views
urlpatterns = [
    path('iniciarSesion',views.iniciarSesion),
    path('',views.adoptions),
    path('registrarUsuario',views.registerUser),
    path('administrador',views.administrador),
    path('registerNewUser',views.registerNewUser),
    path('startSesion',views.startSesion),
    path('nuevaAdopcion',views.nuevaAdopcion),
    path('nuevaPublicacion',views.nuevaPublicacion),
    path('savePublication',views.savePublication),
    path('misPublicaciones',views.misPublicaciones),
    path('editarPublicacion/<id>/',views.editarPublicacion),
    path('processEditPublication/',views.processEditPublication),
    path('eliminarPublicacion/<id>', views.eliminarPublicacion),
    path('cerrarSesion',views.cerrarSesion),
    path('adoptar/<id>/',views.adoptar),
    path('saveAdoption',views.saveAdoption),
    path('listadoMascotas',views.listadoMascotas),
    path('listadoUsuarios',views.listadoUsuarios),
    path('adopcionesPendientes',views.adopcionesPendientes),
    path('approvedAdoption/<id>/',views.approvedAdoption),
    path('rejectAdoption/<id>/',views.rejectAdoption),
    path('adopcionesFinalizadas',views.adopcionesFinalizadas),
    
    
    
    
        

]

    