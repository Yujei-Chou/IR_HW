import nlp
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import xml.etree.ElementTree as ET
from json import dumps
import nltk
import json
nltk.download('punkt')
from nltk import word_tokenize, sent_tokenize


# Create your views here.

def home(request):
    return render(request, 'nlp/index.html')

def handle_uploadFiles(request):
    files = request.FILES.getlist('choseFiles')
    PubMedDocs = {}
    TweetDocs = {}
    for file in files:
        if file.name.endswith('.xml'):
            PubMedDocs[file.name] = {}
            tree = ET.parse(file)
            PMIDs = [ele.text for ele in tree.iter(tag='PMID')]
            PMTitles = [ele.text for ele in tree.iter(tag='ArticleTitle')]
            
            for ele in tree.iter(tag='Article'):
                abstract = {}
                sentenceCnt = 0 
                wordCnt = 0
                charCnt = 0
                not_asciiCnt = 0

                for abs in ele.iter(tag='Abstract'):
                    for node in abs.findall('AbstractText'):
                        for word in word_tokenize(node.text):
                            if(word.isascii()):
                                wordCnt += 1
                            else:
                                for char in word:
                                    if(char.isascii() == False):
                                        not_asciiCnt += 1
                        abstract[node.get('Label')] = [node.text]
                        sentenceCnt += len(sent_tokenize(node.text))
                        charCnt += len(node.text)
                    
                    charCnt -= not_asciiCnt


                    
                PMID = PMIDs.pop(0)
                PMTitle = PMTitles.pop(0)
                PubMedDocs[file.name][PMID] = {'Abstract': abstract,
                                               'Title': PMTitle,
                                               'SentenceCnt': sentenceCnt,
                                               'WordCnt': wordCnt,
                                               'CharCnt': charCnt}
        else:
            TweetDocs[file.name] = {}
            data = json.load(file)
            for ele in data:
                sentenceCnt = 0
                wordCnt = 0
                charCnt = 0
                not_asciiCnt = 0
                for sentence in ele['tweet_text'].split('\n'):
                    sentenceCnt += len(sent_tokenize(sentence))
                    for word in word_tokenize(sentence):
                        if(word.isascii()):
                            wordCnt += 1
                        else:
                            for char in word:
                                if(char.isascii() == False):
                                    not_asciiCnt += 1
                    
                    charCnt += len(sentence)
                charCnt -= not_asciiCnt

                TweetDocs[file.name][ele['twitter_url']]={'Abstract': ele['tweet_text'].split('\n'),
                                                          'Title': ele['full_name'],
                                                          'SentenceCnt': sentenceCnt,
                                                          'WordCnt': wordCnt,
                                                          'CharCnt': charCnt}
                

    return render(request, 'nlp/index.html', {'PubMedDocs':dumps(PubMedDocs), 'TweetDocs':dumps(TweetDocs)}) 









