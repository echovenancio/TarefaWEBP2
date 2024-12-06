from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    hash_senha = models.CharField(max_length=512)
    foto = models.ImageField(upload_to="images/user/")

    def __str__(self):
        return self.email + "|" + self.hash_senha


class Curso(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    duration = models.BigIntegerField()
    estoque = models.BigIntegerField(default=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to="images/curso/")

class Foto(models.Model):
    nome = models.CharField(max_length=255)
    foto = models.ImageField(upload_to="images/galeria/")

class Venda(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
