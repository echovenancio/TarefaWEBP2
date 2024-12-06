from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
import datetime
from . import forms
from . import models

def index(request):
    return render(request, 'app/index.html', {})

def exibir_cursos(request):
    cursos = models.Curso.objects.all()
    try:
        email = request.session['email'];
        user = models.User.objects.get(email=email)
        return render(
            request, 'app/cursos.html',
            {'cursos': cursos,
            'is_logged_in': True,
            'user': user})
    except:
        return render(
            request, 'app/cursos.html',
            {'cursos': cursos,
            'is_logged_in': False,
            'user': None})

def curso(request):
    if request.POST:
        new_curso = forms.CursoForm(request.POST, request.FILES)
        if new_curso.is_valid():
            new_curso.save()
            messages.success(request, "Curso cadastrado com Sucesso!")
            return redirect('app:get-cursos')
    new_curso = forms.CursoForm()
    return render(request, 'app/add_curso.html', {'form': new_curso})

def comprar_curso(request, id_curso):
    if request.POST:
        curso = models.Curso.objects.get(pk=id_curso)
        if curso.estoque <= 0:
            messages.error(request, "Estoque do curso esgotado")
            return redirect('app:get-cursos')
        email = request.session["email"]
        user = models.User.objects.get(email=email)
        estoque_atual = curso.estoque
        curso.estoque = estoque_atual - 1
        curso.save()
        venda = models.Venda(user=user, curso=curso)
        venda.save()
        messages.success(request, "Curso comprado com Sucesso!")
        return redirect('app:get-cursos')

def signup(request):
    if request.POST:
        new_user = forms.UserForm(request.POST, request.FILES)
        if models.User.objects.filter(email=request.POST["email"]).exists():
            messages.error(request, "Email informado já está cadastrado")
            return render(request, 'app/signup.html', {'form': new_user})
        if new_user.is_valid():
              new_user.save()
              messages.success(request, "Usuario Cadastrado com Sucesso!")
              return redirect('app:form_login')
    new_user = forms.UserForm()
    return render(request, 'app/signup.html', {'form': new_user})

def form_login(request):
    form_login = forms.FormLogin(request.POST or None)
    if request.POST:
        _email = request.POST['email']
        _senha = request.POST['hash_senha']
        try:
            usuario = models.User.objects.get(email=_email)
            if check_password(_senha, usuario.hash_senha):
                messages.success(request, 'Usuario encontrado sucesso')
                request.session.set_expiry(datetime.timedelta(seconds=60))
                request.session['email'] = _email
                return redirect('app:dashboard')
        except Exception:
            messages.error(request, 'Usuario não encontrado')
            return redirect('app:form_login')
    context = { 'form': form_login }
    return render(request, 'app/form-login.html', context)

def dashboard(request):
    email = request.session.get('email')
    if email is not None:
        user = models.User.objects.get(email=email)
        return render(request, 'app/dashboard.html', { 'user': user })
    return redirect('app:form_login')

def edit_user(request, id_usuario):
    usuario = models.User.objects.get(pk=id_usuario)
    form = forms.UserForm(request.POST or None, instance=usuario)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('app:get-users')
    return render(request, 'app/edit_user.html', { 'form': form })

def change_password(request, id_usuario):
    usuario = models.User.objects.get(pk=id_usuario)
    form = forms.ChangePassword(request.POST or None, instance=usuario)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('app:dashboard')
        else:
            messages.error(request, "Senha incorreta")
    return render(request, 'app/change_pass.html', { 'form': form, 'id': id_usuario })

def delete_user(request, id_usuario):
    usuario = models.User.objects.get(pk=id_usuario)
    usuario.delete()
    messages.success(request, "Usuario Deletado!")
    return redirect('app:index')

def upload_foto(request):
    if request.POST:
        form = forms.FotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Imagem salva")
            return redirect('app:galeria')
        else:
            messages.error(request, "Erro")
            return render(request, 'app/upload_foto.html', {'form': form})
    else:
        form = forms.FotoForm()
        return render(request, 'app/upload_foto.html', {'form': form})

def galeria(request):
    fotos = models.Foto.objects.all()
    return render(request, "app/galeria.html", {"fotos": fotos})

def contato(request):
    return render(request, "app/contato.html", {})

def grafico_vendas(request):
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64
    from datetime import date
    today = date.today()
    current_month = today.month
    vendas = models.Venda.objects.filter(date__month=current_month)
    total_vendas = vendas.count()
    venda_por_curso = dict()
    for v in vendas:
        if venda_por_curso.get(v.curso.name, None):
            venda_por_curso[v.curso.name] = venda_por_curso[v.curso.name] + 1
        else:
            venda_por_curso[v.curso.name] = 1
    fig, axs = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [1, 1]})
    axs[0].bar(
        venda_por_curso.keys(),
        venda_por_curso.values(),
        color='skyblue'
    )
    axs[0].set_xlabel('Cursos')
    axs[0].set_ylabel('Vendas')
    axs[0].set_title('Vendas por curso no mês')
    buffer = BytesIO()
    axs[1].bar(
        ["total"],
        [total_vendas],
        color='skyblue'
    )
    axs[1].set_title('Total de Vendas')
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return render(request, "app/graficos.html", {"image": image_base64})
