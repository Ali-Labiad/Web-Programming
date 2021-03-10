from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

from . import util
from .forms import NewWikiForm
from .forms import EditWikiForm
from markdown2 import Markdown
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request , name):

    data = util.get_entry(name)
    if (data == None):
      messages.error(request, "The Page Not Found")
      return render(request, "encyclopedia/wiki.html" , {
        "name" : name
      })
    else:
       markdowner = Markdown()
       dataMark = markdowner.convert(data)
       return render(request, "encyclopedia/wiki.html", {
        "name": name,
        "data": dataMark
      })

def search(request):

    entries = util.list_entries()
    results =  []
    name = request.GET['q']
    found = False
    
    for entry in entries :
      if name.lower() in entry.lower():
        found = True
        results.append(entry)

    if found :
      return render(request, "encyclopedia/search.html", {
        "entries": results
      })
    else:
      return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new(request):

    if request.method == 'POST':
        form = NewWikiForm(request.POST)
        if form.is_valid():
          title = form.cleaned_data['title']
          content = form.cleaned_data['content']
          entries = [x.lower() for x in util.list_entries()]
          if title.lower() in entries:
            messages.error(request, "The Page Already Exists")
          else:
            util.save_entry(title, content)
            url = reverse('wiki', kwargs={'name': title})
            return HttpResponseRedirect(url)

    else:
        form = NewWikiForm()

    return render(request, "encyclopedia/new.html", {
          "form": form
    })

def edit(request , name):

    content = util.get_entry(name)
    form = EditWikiForm(initial={'content': content})

    if request.method == 'POST':
      form = EditWikiForm(request.POST)
      if form.is_valid():
        content = form.cleaned_data['content']
        util.save_entry(name, content)
        url = reverse('wiki', kwargs={'name': name})
        return HttpResponseRedirect(url)
          
    return render(request, "encyclopedia/edit.html",{
          "form": form
    })

def randomwiki(request):

  content = util.list_entries()
  wiki = random.choice(content)
  url = reverse('wiki', kwargs={'name': wiki})
  return HttpResponseRedirect(url)

