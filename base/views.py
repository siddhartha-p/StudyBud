from django.shortcuts import render,redirect # type: ignore
from django.contrib import messages #type:ignore
from django.http import HttpResponse         # type: ignore
from django.contrib.auth.decorators import login_required #type:ignore
from django.db.models import Q # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.forms import UserCreationForm #type:ignore
from django.contrib.auth import authenticate,login,logout #type:ignore
from .models import Room,Topic,Message
from .forms import RoomForm
# Create your views here.



def loginPage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
        
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user) #creates a session in the database and inside the browser
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist")
            

    context={'page':page}
    return render(request,'base/login_register.html',context)


def logoutUser(request):
    
    logout(request) #deletes the session from the browser
    return redirect('home')


def registerPage(request):
    form=UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "There was some error processing your registration")
        
        
    return render(request,'base/login_register.html',{'form':form})


def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(decription__icontains=q)
        )
    room_count=rooms.count()
    topics=Topic.objects.all()
    context={'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()

    

    if request.method=="POST":
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room',pk=room.id)
        

    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You dont have the authority to update this room")

    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context={'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You dont have the authority to delete this room")
    
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})


