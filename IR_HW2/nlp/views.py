import nlp
from nlp.models import PubMed, withoutPuncTokens
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
import nltk
# import pandas as pd
import pickle
nltk.download('punkt')
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.metrics import edit_distance
from nltk.stem import PorterStemmer

word_index = pickle.load(open("files/word_index.pkl", "rb"))


# Create your views here.
def home(request):      
    return render(request, 'nlp/index.html')

def label_keyword(text, loc_list):
    tokens = word_tokenize(text)
    for loc in loc_list:
        tokens[loc] = '<span class="label">' + tokens[loc] + '</span>'
    return TreebankWordDetokenizer().detokenize(tokens)


@csrf_exempt
def handle_content(request):
    if request.method == 'POST':
        porter_keyword = PorterStemmer().stem(request.POST['keyword'])
        abstract = PubMed.objects.values_list('abstract', flat=True).filter(id = int(request.POST['id']))[0]
        content = label_keyword(abstract, word_index[porter_keyword][int(request.POST['id'])])
        return HttpResponse(content)


def search_keyword(request):
    if request.method == 'GET':
        page_number = request.GET.get('page')
        keyword = request.GET.get('keyword')
        porter_keyword = PorterStemmer().stem(keyword)     
        articles = PubMed.objects.filter(pk__in =list(word_index[porter_keyword].keys())) 
        articles_paginator = Paginator(articles, 20)
        page = articles_paginator.get_page(page_number)

        context = {
            'count': articles_paginator.count,
            'page': page,
            'keyword': keyword
        }
        return render(request, 'nlp/index.html', context)

@csrf_exempt
def partial_matching(request):
    tokens = list(withoutPuncTokens.objects.values_list('word', flat=True))
    matching_words = {}
    for token in tokens:
        matching_words[token] = edit_distance(token, request.POST['searchWord'])
    Top5_matching = [item[0] for item in sorted(matching_words.items(), key=lambda x:x[1])[:5]]
    return HttpResponse(json.dumps(Top5_matching))

