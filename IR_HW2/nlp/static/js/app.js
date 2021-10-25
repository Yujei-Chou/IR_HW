function handle_content(articleID, articleTitle){
    $.ajax({
        url: 'handle_content',
        method: 'POST',
        data: {
            id: articleID,
            keyword: $('input[name=searchWord]').val()
        },
        success: function(data){
            $('#articleModal > div > div > div.modal-body').html(data)
            $('#articleModal > div > div > div.modal-header > h5').html(articleTitle)
        }
    })
}

function partial_matching(){
    $('#search-btn').prop('disabled', true)
    $('.bi-search').hide()
    $('#search-div > div > button > span').css('display', 'flex')
    $('.list-group').empty()
    $.ajax({
        url: 'partial_matching',
        method: 'POST',
        data: {
            searchWord: $('input[name=searchWord]').val()
        },
        success: function(data){
            $('#search-btn').prop('disabled', false)
            $('.bi-search').show()
            $('#search-div > div > button > span').hide()
            $('#searchModal').modal('show')
            $('.list-group').append(`<input type="hidden" class="form-control" name="keyword">`)
            JSON.parse(data).forEach(element => {
                $('.list-group').append(`<button type="submit" class="list-group-item list-group-item-action" onclick="select_matching($(this).html())">${element}</button>`)                
            })
        }
    })
}

function select_matching(selectedWord){
    $('input[name=keyword]').val(selectedWord)
}

function show_Zipf(){
    $('#Zipf').css('display', 'block')
}