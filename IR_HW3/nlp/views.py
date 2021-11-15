from nltk.util import pr
import nlp
from nlp.models import PubMed, withoutPuncTokens
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
import nltk
nltk.download('punkt')
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.metrics import edit_distance
from nltk.stem import PorterStemmer
from gensim.models import Word2Vec, word2vec
import plotly
import numpy as np
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

model = Word2Vec.load('files/word2vec.model')

# Create your views here.
def home(request):      
    return render(request, 'nlp/index.html')


def append_list(sim_words, words):
    
    list_of_words = []
    
    for i in range(len(sim_words)):
        
        sim_words_list = list(sim_words[i])
        sim_words_list.append(words)
        sim_words_tuple = tuple(sim_words_list)
        list_of_words.append(sim_words_tuple)
        
    return list_of_words

def get_word2vec(words, sample):
    if words == None:
      if sample > 0:
        words = np.random.choice(list(model.vocab.keys()), sample)
      else:
        words = [ word for word in model.vocab ]

    word_vectors = []
    for w in words:
      try:
        word_vectors.append(model[w])
      except:
        word_vectors.append(model[PorterStemmer().stem(w)])

    word_vectors = np.array(word_vectors)  
    return word_vectors  

@csrf_exempt
def drawPCA(request):
    input_word = request.POST['keyword']
    PCA_type = request.POST['type']
    
    user_input = [x.strip() for x in input_word.split(' ')]
    result_word = []
    sim_list = []

    for words in user_input:
        sim_words = model.most_similar(PorterStemmer().stem(words), topn=5)
        sim_words = append_list(sim_words, words)
            
        result_word.extend(sim_words)
        
    similar_word = [word[0] for word in result_word]
    similarity = [word[1] for word in result_word] 
    similar_word.extend(user_input)
    labels = [word[2] for word in result_word]
    label_dict = dict([(y,x+1) for x,y in enumerate(set(labels))])
    color_map = [label_dict[x] for x in labels]
    
    
    if(PCA_type == '2D'):
        graph = display_PCA_2D(model, user_input, similar_word, labels, color_map, annotation='On', topn=5, sample=10)
        return HttpResponse(graph)

    if(PCA_type == '3D'):
        sim_org = model.most_similar(PorterStemmer().stem(input_word), topn=5)
        for item in sim_org:
            sim_list.append({item[0]: item[1]})        
        graph = display_PCA_3D(model, user_input, similar_word, labels, color_map, topn=5, sample=10)
        return HttpResponse(json.dumps({'graph': graph, 'similarity': sim_list}))
    


def display_PCA_2D(model, user_input=None, words=None, label=None, color_map=None, annotation='On', topn=0, sample=10):
    word_vectors = get_word2vec(words, sample)
    two_dim = PCA(random_state=0).fit_transform(word_vectors)[:,:2]
    
    data = []
    count = 0
    for i in range (len(user_input)):
      trace = go.Scatter(
          x = two_dim[count:count+topn,0], 
          y = two_dim[count:count+topn,1],  
          text = words[count:count+topn] if annotation == 'On' else '',
          name = user_input[i],
          textposition = "top center",
          textfont_size = 10,
          mode = 'markers+text',
          marker = {
              'size': 15,
              'opacity': 0.8,
              'color': 2
          }

      )
      
      data.append(trace)
      count = count+topn

    trace_input = go.Scatter(
              x = two_dim[count:,0], 
              y = two_dim[count:,1],  
              text = words[count:],
              name = 'input words',
              textposition = "top center",
              textfont_size = 10,
              mode = 'markers+text',
              marker = {
                  'size': 15,
                  'opacity': 1,
                  'color': 'black'
              }
            )

    data.append(trace_input)
    
    # Configure the layout.
    layout = go.Layout(
      margin = {'l': 0, 'r': 0, 'b': 0, 't': 0},
      showlegend=True,
      hoverlabel=dict(
          bgcolor="white", 
          font_size=20, 
          font_family="Courier New"),
      legend=dict(
            x=1,
            y=0.5,
            font=dict(
                family="Courier New",
                size=25,
                color="black"
            )),
            font = dict(
                family = " Courier New ",
                size = 15),
            autosize = False,
            width = 1000,
            height = 500
            )


    plot_figure = go.Figure(data = data, layout = layout)
    graph = plot_figure.to_html(full_html=False)
    return graph

def display_PCA_3D(model, user_input=None, words=None, label=None, color_map=None, topn=0, sample=10):
    word_vectors = get_word2vec(words, sample)
    three_dim = PCA(random_state=0).fit_transform(word_vectors)[:,:3]


    data = []
    count = 0

    for i in range (len(user_input)):
        trace = go.Scatter3d(
            x = three_dim[count:count+topn,0], 
            y = three_dim[count:count+topn,1],  
            z = three_dim[count:count+topn,2],
            text = words[count:count+topn],
            name = user_input[i],
            textposition = "top center",
            textfont_size = 20,
            mode = 'markers+text',
            marker = {
                'size': 10,
                'opacity': 0.8,
                'color': 2
            }

        )

    data.append(trace)
    count = count+topn

    trace_input = go.Scatter3d(
            x = three_dim[count:,0], 
            y = three_dim[count:,1],  
            z = three_dim[count:,2],
            text = words[count:],
            name = 'input words',
            textposition = "top center",
            textfont_size = 20,
            mode = 'markers+text',
            marker = {
                'size': 10,
                'opacity': 1,
                'color': 'black'
            }
            )

    
    data.append(trace_input)

    # Configure the layout

    layout = go.Layout(
    margin = {'l': 100, 'r': 100, 'b': 100, 't': 0},
    showlegend=True,
    legend=dict(
            x=1,
            y=0.5,
            font=dict(
                family="Courier New",
                size=25,
                color="black"
            )),
            font = dict(
                family = " Courier New ",
                size = 15),
            autosize = True,
            width = 1000,
            height = 800
            )


    plot_figure = go.Figure(data = data, layout = layout)
    graph = plot_figure.to_html(full_html=False)
    return graph