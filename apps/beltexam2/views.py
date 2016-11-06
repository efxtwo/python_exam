from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Quotes
from django.db.models import Count

def index(request):
    return render(request,'beltexam2/index.html')

def register(request):
    if request.method == "POST":
        valid_reg = User.objects.validate_user_info(request.POST)
        if len(valid_reg) > 0:
            for error in valid_reg:
                messages.error(request, error)
        else:
            User.objects.register(request.POST)
            messages.success(request, "Nice Job, You are now registered!")

    return redirect('/')


def login(request):
    if request.method == "POST":
        errors = User.objects.login(request.POST['email'], request.POST['pw'])
        if len(errors) > 0:
            for error in errors:
                messages.error (request, error)
            return redirect ('/')
        else:
            request.session['humanbeing'] = User.objects.get(email=request.POST['email']).id
            return redirect('quotes')

def quotes(request):
    if 'humanbeing' not in request.session:
        return redirect('/')
    me = User.objects.get(id=request.session['humanbeing'])
    thequotes = Quotes.objects.all() | Quotes.objects.exclude(favoriter=me)
    otherquotes = Quotes.objects.filter(favoriter=me)

    context = { 'user': me, 'created':thequotes, 'others':otherquotes}

    return render(request, 'beltexam2/quotes.html', context)


def remove(request, id):
    if 'humanbeing' not in request.session:
        return redirect('/')
    me = User.objects.get(id=request.session['humanbeing'])
    quotes = Quotes.objects.get(id=id)
    quotes.favoriter.remove(me)
    quotes.save()
    return redirect('quotes')

def user(request, id):
    posts = Quotes.objects.filter(id=id)
    context = {'data':posts,}
    return render(request, 'beltexam2/user.html', context)


def create(request):
    if 'humanbeing' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        valid_post = User.objects.validate_user_post(request.POST)
        if len(valid_post) > 0:
            for error in valid_post:
                messages.error(request, error)
        else:
            user_id = request.session['humanbeing']
            user = User.objects.get(id=user_id)
            Quotes.objects.create(author=request.POST['quotedby'], comment=request.POST['message'], creator=user)
            print Quotes.comment
    return redirect ('quotes')

def add(request, id):
    if 'humanbeing' not in request.session:
        return redirect('/')
    me = User.objects.get(id=request.session['humanbeing'])
    quotes = Quotes.objects.get(id=id)
    quotes.favoriter.add(me)
    quotes.save()
    return redirect('quotes')

def logout(request):
    if 'humanbeing' not in request.session:
        request.session.pop('humanbeing')
    return redirect('/')
