from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from .models import Quotes
import random
import json

def index(request):
    result = Quotes.objects.all()
    count = len(result)
    if count > 0:
        total = 0
        for line in result:
            total += line.weight
        number = random.randint(1, total)
        for line in result:
            if number - line.weight <= 0:
                line.views += 1
                line.save()
                quote = line
                break
            number -= line.weight
        context = {'quote': quote}
        return render(request, "index.html", context)
    else:
        return render(request, "index_empty.html")

def form(request):
    result = Quotes.objects.all()
    context = {'quotes': result}
    return render(request, "form.html", context)

def edit(request, id):
    if request.method == "POST":
        name = request.POST.get("name", "Undefined")
        source = request.POST.get("source", "Undefined")
        weight = request.POST.get("weight", 1)
        edited = Quotes.objects.get(id=id)
        edited.name = name
        edited.source = source
        edited.weight = weight
        edited.save()
    quote = Quotes.objects.get(id=id)
    if request.method == "POST":
        quote_json = model_to_dict(quote)
        return JsonResponse(quote_json, safe=False)
    else:
        context = {'quote': quote}
        return render(request, "edit.html", context)

def postquote(request):
    name = request.POST.get("name", "Undefined")
    source = request.POST.get("source", "Undefined")
    weight = request.POST.get("weight", 1)
    is_exist = Quotes.objects.filter(name=name).exists()
    if is_exist:
        return JsonResponse({"error": "Данная цитата уже добавлена"})
    else:
        is_source = Quotes.objects.filter(source=source).count()
        if is_source == 3:
            return JsonResponse({"error": "Нельзя добавить больше трёх цитат для одного источника"})
        newquote = Quotes.objects.create(name=name, source=source, weight=weight)
        quotes = Quotes.objects.all()
        quotes_list = [model_to_dict(quote) for quote in quotes]
        result = json.dumps(quotes_list, ensure_ascii=False)
        return JsonResponse(result, safe=False)

def delete(request, id):
    quote = Quotes.objects.get(id=id)
    quote.delete()
    quotes = Quotes.objects.all()
    quotes_list = [model_to_dict(quote) for quote in quotes]
    result = json.dumps(quotes_list, ensure_ascii=False)
    return JsonResponse(result, safe=False)

def rate(request):
    quoteId = request.POST.get("quote", 1)
    mark = request.POST.get("mark", "Undefined")
    targetQuote = Quotes.objects.get(id=quoteId)
    if mark == "like":
        targetQuote.likes += 1
    if mark == "dislike":
        targetQuote.dislikes +=1
    targetQuote.save()
    quote_json = model_to_dict(targetQuote)
    return JsonResponse(quote_json, safe=False)

def dashboard(request):
    top10 = Quotes.objects.order_by("-likes")[:10]
    context = {'quotes': top10}
    return render(request, "dashboard.html", context)
