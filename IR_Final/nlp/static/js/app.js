function handle_content(articleID, articleTitle){
    $.ajax({
        url: 'handle_content',
        method: 'POST',
        data: {
            id: articleID
        },
        success: function(data){
            console.log(articleID)
            $('#articleModal > div > div > div.modal-body').html(data)
            $('#articleModal > div > div > div.modal-header > div').html(articleTitle)
            $('#articleModal > div > div > div.modal-footer > a').attr('href', `https://www.ncbi.nlm.nih.gov/research/pubtator/?view=docsum&query=${articleID}`)
        }
    })
}


function search(){
    $('#search-btn').prop('disabled', true)
    $('.bi-search').hide()
    $('#search-div > div > button > span').css('display', 'flex')    
    $('#queryArticles').empty()
    $.ajax({
        url: 'search',
        method: 'POST',
        data: {
            search_str: $('input[name=searchInput]').val()
        },
        success: function(data){
            $('#search-btn').prop('disabled', false)
            $('.bi-search').show()
            $('#search-div > div > button > span').hide()
            // console.log(data)

            JSON.parse(data).forEach((element, idx) => {
                $('#queryArticles').append(`<h4 data-toggle="modal" data-target="#articleModal" articleID="${element[1]}" onclick="handle_content($(this).attr('articleID'), $(this).html())">${element[3]}</h4>
                                            <span class="badge badge-success">similarity score: ${element[0]}</span>
                                            <div id="tags_${element[1]}"></div>
                                            <p>${element[4]}</p>
                                            <hr>`)
                

                $.each(element[2], function(index, tag) {
                    $('#tags_' + element[1]).append(`<span class="badge badge-warning"><i class="bi bi-tags-fill"></i>&nbsp; ${tag}&nbsp;</span>`)
                  });
            })            

        }
    })     
}

