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
    
    
    
    

]

    