from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from . import util
from django import forms
import random
class User(forms.Form):
    title=forms.CharField(max_length=64)
    content=forms.CharField(widget=forms.Textarea())
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def view(request,title):
    cont=util.get_entry(title)
    mar=Markdown()
    return render(request,"encyclopedia/view.html",{
        "text":mar.convert(cont),
        "title":title
        })
def create(request):
    if(request.method == 'POST'):
        frm=User(request.POST)
        if(frm.is_valid()):
            title=frm.cleaned_data["title"]
            conte=frm.cleaned_data["content"]
            print(frm.cleaned_data)
            if("edit" in request.POST):
                util.save_entry(title,conte)
                return HttpResponseRedirect(reverse('title',args={title}))
            else:
                if title in util.list_entries():
                    msg="Error:Entry Already Exists!"
                    return render(request,'encyclopedia/error.html',{
                    "message":msg
                    })
                util.save_entry(title,conte)
                return HttpResponseRedirect(reverse('title',args={title}))
    form=User()
    return render(request,'encyclopedia/create.html',{
        "forms":form
        })
def search(request):
    lst=[]
    c=0;
    if(request.method=='POST'):
        sear=request.POST['q']
        for i in util.list_entries():
            if(i.find(sear)!=-1):
                lst.append(i)
                c=c+1
        print(lst)
        print(util.list_entries())
    if(c==0):
        return HttpResponse("No record found")
    if(c==1):
        cont=util.get_entry(lst[0])
        mar=Markdown()
        return render(request,"encyclopedia/view.html",{
        "text":mar.convert(cont),
        "title":lst[0]
        })
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": lst})
def rand(request):
    it=random.choice(util.list_entries())
    cont=util.get_entry(it)
    mar=Markdown()
    return render(request,"encyclopedia/view.html",{
        "text":mar.convert(cont),
        "title":it
        })
def edit(request):
    if(request.method=='POST'):
        titl=request.POST['tit']
        cont=util.get_entry(titl)
        form=User({"title":titl,"content":cont})
        return render(request,'encyclopedia/edit.html',{
        "forms":form
        })


