from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.form_login, name='form_login'),
    path('signup/', views.signup, name='signup'),
    path('add-curso/', views.curso, name="curso"),
    path('cursos/', views.exibir_cursos, name="get-cursos"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user/edit/<int:id_usuario>', views.edit_user, name="edit-user"),
    path('user/delete/<int:id_usuario>', views.delete_user, name="delete-user"),
    path('user/password/<int:id_usuario>', views.change_password, name="change-password"),
    path('upload_foto', views.upload_foto, name="upload-foto"),
    path('galeria', views.galeria, name="galeria"),
    path('contato', views.contato, name='contato'),
    path('comprar-curso/<int:id_curso>', views.comprar_curso, name="comprar-curso"),
    path('graficos', views.grafico_vendas, name="grafico-vendas")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
