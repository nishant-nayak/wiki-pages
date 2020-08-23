from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown2 import markdown
from . import util
from django import forms
from random import choice
from django.urls import reverse

class NewForm(forms.Form):
    title = forms.CharField(label="", strip=True, required=True, widget=forms.TextInput(attrs={'placeholder':'Title'}))
    text = forms.CharField(label="", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, title):
    text = util.get_entry(title)
    if text:
        title = text.split('\n', 1)[0].split(' ')[1]
        html_text = markdown(text)
        return render(request, "encyclopedia/content.html", {
            "title": title.strip(),
            "text": html_text
        })
    else:
        return render(request, "encyclopedia/apology.html", {
            "title": title
        })

def search(request):
    q = request.POST.get("q")
    entries = util.list_entries()
    for entry in entries:
        if entry.lower() == q.lower():
            return HttpResponseRedirect(reverse('content', args=[entry]))
    
    results = []
    q = q.lower()
    for entry in entries:
        if entry.lower().count(q) > 0:
            results.append(entry)
    print(results)
    return render(request, "encyclopedia/search.html", {
        "query" : q,
        "results" : results,
        "entries" : entries
    })

def new(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            entries = util.list_entries()
            for entry in entries:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/error.html", {
                        "title" : title
                    })
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse('content', args=[title]))
        else:
            return render(request, "encyclopedia/new.html", {
                "form" : form
            })

    form = NewForm()
    return render(request, "encyclopedia/new.html", {
        "form" : form
    })

def edit(request, title):
    if request.method == "POST":
        text = request.POST.get('text')
        util.save_entry(title, text)
        return HttpResponseRedirect(reverse('content', args=[title]))
    
    text = util.get_entry(title)
    return render(request, "encyclopedia/edit.html",{
        "title" : title,
        "text" : text
    })

def random(request):
    entries = util.list_entries()
    page = choice(entries)
    return HttpResponseRedirect(reverse('content', args=[page]))