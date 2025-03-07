from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

rooms=[
    {'id':1, 'name':'lets learn Python'},
    {'id':2, 'name':'lets learn javascript'},
    {'id':3, 'name':'lets learn C#'}
]

def home(request):
    context={'rooms':rooms}
    return render(request,'home.html',context)

def room(request,pk):
    room=None
    for i in rooms:
        if i['id']==int(pk):
            room=i
    context={'room':room}
    return render(request,'room.html',context)
