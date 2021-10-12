# IR_HW1

### Environment
- Django 2.2
- Python 3.10.0
- Docker

### Run website
- <h4>Command</h4>
```
cd IR_HW1
docker-compose up
```
- <h4>Open website</h4>
```
127.0.0.1:5000/nlp/home
```

### Function
- <h4>Statistics:</h4>
  <h5>Number of sentence:</h5> &nbsp&nbsp Use nltk <a href="https://www.nltk.org/api/nltk.tokenize.html">sent_tokenize</a> function to calculate number of sentence.
  <h5>Number of word:</h5> &nbsp&nbsp Use nltk <a href="https://www.nltk.org/api/nltk.tokenize.html">word_tokenize</a> function to calculate number of word.


- <h4>Label keyword:</h4>
```
function annotate_keyword(text, keyword){
    let search_idx = 0;
    let res = '';
    let found = false;

    while(text.slice(0).indexOf(keyword) != -1 && keyword.length != 0){
        found = true;
        search_idx = text.slice(0).indexOf(keyword);
        res = res.concat(text.slice(0, search_idx), '<span class="label">', keyword, '</span>');
        text = text.slice(search_idx+keyword.length);
    }
    res = res.concat(text);
    return {res:res, found:found};   
}
```

### Website
- <h4>Upload xml or json files:</h4>
<p align="center"><img src="https://user-images.githubusercontent.com/56510169/136833318-eb7107f4-38e4-4833-9c6d-b406d207a7e9.png" width="60%"/></p>

- <h4>Search keyword and list matching files:</h4>
<p align="center"><img src="https://user-images.githubusercontent.com/56510169/136834171-c44383c7-9ea6-480e-8e1f-a0077c02fd94.png" width="60%"/></p>

- <h4>Label keyword and show statistics data:</h4>
<p align="center"><img src="https://user-images.githubusercontent.com/56510169/136834020-1800b74c-f3bf-466d-bc2c-2b58700b2c23.png" width="60%"/></p>
