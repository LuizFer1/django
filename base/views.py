from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .forms import RoomForm
from .models import Room, Topic, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm


# rooms = [
#   {'id' : 1 , 'name' : 'lets learn python'},  
#   {'id' : 2 , 'name' : 'lets learn Django'},
#   {'id' : 3 , 'name' : 'lets learn JS'}
# ]

# Create your views here.

def loginPage(request):
  page = 'login'

  if request.user.is_authenticated:
    return redirect('home')

  if request.method == "POST":
    username = request.POST.get('username').lower()
    password = request.POST.get('password')

    try:
      User.objects.get(username = username)
    except:
      messages.error(request, 'User does not exist')

    user = authenticate(request, username=username, password=password)
    if user != None:
      login(request,user)
      return redirect('home')
    else:
      messages.error(request, 'Username or password does not exist')


  context = {'page' : page}
  return render(request, 'base/login__register.html', context)

def logoutUser(request):
  logout(request)
  return redirect('home')

def registerPage(request):
  form = UserCreationForm()

  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Some error occurred during registration!')
  context = {'form' : form}
  return render(request, 'base/login__register.html', context)


def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  topics = Topic.objects.all()
  rooms = Room.objects.filter(Q(topico__name__icontains = q) | Q(name__icontains = q) | Q(description__icontains = q))
  room_message = Message.objects.filter(Q(room__topico__name__icontains = q))
  room_count = rooms.count()

  context =  {'rooms' : rooms, 'topics' : topics, 'room_count' : room_count, 'room_messages': room_message}
  return render(request,'base/home.html',context)

def room(request, pk):
  room = Room.objects.get(id = pk)
  participants = room.participants.all()
  room_messages = room.message_set.all().order_by('-create')

  if request.method == 'POST':
    message = Message.objects.create(
       user = request.user,
       room = room,
       body = request.POST.get('body')
    )
    room.participants.add(request.user)
    return redirect('room', pk = room.id)

  context = {'room' : room, 'room_messages' : room_messages, 'participants' : participants}
  return render(request, 'base/room.html', context)

def userProfilePage(request, pk):
  user = User.objects.get(id = pk)
  rooms = user.room_set.all()
  room_message = user.message_set.all()
  topics = Topic.objects.all()

  context = {'user' : user, 'rooms' : rooms, 'room_messages' : room_message, 'topics' : topics}
  return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
  form = RoomForm()
  topics =Topic.objects.all()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    topic_name = request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)

    Room.objects.create(
      host = request.user,
      topico = topic,
      name = request.POST.get('name'),
      description = request.POST.get('description')
    )
    
    return redirect('home')
  
  context = {'form':form, 'topics' : topics}
  return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
  room = Room.objects.get(id = pk)
  form = RoomForm(instance=room)

  if request.user != room.host:
    return HttpResponse("Your aren't allowed here!")

  if request.method == 'POST':
    topic_name = request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)
    form = RoomForm(request.POST, instance=room)
    room.name = request.POST.get('name')
    room.topico = topic
    room.description = request.POST.get('description')
    room.save()
    
    return redirect('home')

  context = { 'form' : form}
  return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
  room = Room.objects.get(id = pk)

  if request.user != room.host:
    return HttpResponse("Your aren't allowed here!")

  if request.method == "POST":
    room.delete()
    return redirect('home')

  return render(request, 'base/delete.html', {'obj' : room})


@login_required(login_url='login')
def deleteMessage(request, pk):
  message = Message.objects.get(id = pk)

  if request.user != message.user:
    return HttpResponse("Your aren't allowed here!")

  if request.method == "POST":
    message.delete()
    return redirect('home')

  return render(request, 'base/delete.html', {'obj' : message})