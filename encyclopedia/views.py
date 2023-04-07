from django.shortcuts import render
from . import util
from markdown2 import Markdown
import re
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random




class newTaskForm(forms.Form):
    task = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search encyclopedia','autocomplete':'off'}))


class newPageForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder':'Title of the entry','class':'form-head'}))
    body = forms.CharField(label='Enter the entry in markdown format', widget=forms.Textarea(attrs={'placeholder': 'Entry in markdown format','class':'form-body'}))


class editPageForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder':'Title of the entry','class':'form-head'}))
    body = forms.CharField(label='Enter the entry in markdown format', widget=forms.Textarea(attrs={'placeholder': 'Entry in markdown format','class':'form-body'}))


# find matching title or list of similar title
def find_matching_title(title):
 
    get_list = util.list_entries()
    
    matched_titles = []

    for list_item in get_list:
        title_match = re.search(title, list_item, re.IGNORECASE)

        if title_match != None :
            matched_titles.append(list_item)

    return matched_titles




        

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": newTaskForm()
    })



def entry(request, title):

    markdowner = Markdown()
    entrys_data = util.get_entry(title)
    if entrys_data:
        return render (request, "encyclopedia/title.html",{
            "entry": markdowner.convert(entrys_data),
            "form": newTaskForm(),
            "title": title
        })

    else:
        similar_titles = find_matching_title(title)
        if similar_titles:
            return render (request, "encyclopedia/searchresult.html",{
                "similar_titles": similar_titles,
                "form": newTaskForm()
            })
        else:
            return render (request, "encyclopedia/error.html",{
                "message": "Requested page was not found...",
                "form": newTaskForm()
            })
    
   
def entry_search(request):

    if request.method == "POST":

        markdowner = Markdown()
        form = newTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["task"]
            title_data = util.get_entry(title)
            if title_data:
                return render(request,"encyclopedia/title.html",{
                    "entry": markdowner.convert(title_data),
                    "form": newTaskForm
                })
            else:
                similar_titles = find_matching_title(title)
                if similar_titles:
                    return render (request, "encyclopedia/searchresult.html",{
                        "similar_titles": similar_titles,
                        "form": newTaskForm()
                    })
                else:
                    return render (request, "encyclopedia/error.html",{
                    "message": "Requested page was not found...",
                    "form": newTaskForm()
                    })
        else:
            return render (request, "encyclopedia/error.html",{
                    "message": "Requested page was not found...",
                    "form": newTaskForm()
                    })
      



def new_page(request):

    if request.method == "POST":
        form = newPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            title_already = util.get_entry(title)
            if title_already:
                return render(request, "encyclopedia/newpage.html",{
                    "new_page_form": newPageForm(),
                    "form": newTaskForm(),
                    "message": "File already exist"
                })
            else:
                util.save_entry(title, body)
                return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "encyclopedia/newpage.html",{
                    
                    "form": newTaskForm(),
                    "message": form
                })


    
    else:
        return render(request, "encyclopedia/newpage.html",{
            "new_page_form": newPageForm(),
            "form": newTaskForm()
        })


def edit_page(request):
    if request.method == "POST":
        form = editPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            util.save_entry(title, body)
            return HttpResponseRedirect(reverse("index"))




    elif request.method == "GET":
        title = request.GET.get("title")

        title_data = util.get_entry(title)
        context = {}

        initial_dict = {
            "title": title,
            "body": title_data
        }

        form = editPageForm(initial = initial_dict)
        return render(request, "encyclopedia/editpage.html", {
            "edit_page_form": form,
            "form": newTaskForm()
        })


def random_page(request):
    markdowner = Markdown()
    list = util.list_entries()
    random_entry = random.choice(list)
    entry_data = util.get_entry(random_entry)
    return render(request, "encyclopedia/randompage.html",{
        "entry": markdowner.convert(entry_data),
        "form": newTaskForm(),   
    })
        

    



