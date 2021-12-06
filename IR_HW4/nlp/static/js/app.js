function handle_content(articleID, articleTitle){
    $.ajax({
        url: 'handle_content',
        method: 'POST',
        data: {
            id: articleID
        },
        success: function(data){
            $('#articleModal > div > div > div.modal-body').html(data)
            $('#articleModal > div > div > div.modal-header > h5').html(articleTitle)
        }
    })
}

function checkbox_result(){
    let TF, IDF
    if($('#TF-1').is(":checked")){
        TF = 1
    }else{
        TF = 2
    }

    if($('#IDF-1').is(":checked")){
        IDF = 1
    }else{
        IDF = 2
    }    

    return {'TF':TF, 'IDF':IDF}
}

function search(){
    $('#queryArticles').empty()
    TF_IDF_fm = checkbox_result()
    $.ajax({
        url: 'search',
        method: 'POST',
        data: {
            search_str: $('input[name=searchInput]').val(),
            TF: TF_IDF_fm.TF,
            IDF: TF_IDF_fm.IDF
        },
        success: function(data){
            JSON.parse(data).forEach((element, idx) => {
                console.log(element)
                $('#queryArticles').append(`<h4 data-toggle="modal" data-target="#articleModal" articleID="${element[1]}" onclick="handle_content($(this).attr('articleID'), $(this).html())">${element[2]}</h4>
                                            <span class="badge badge-warning">doc len: ${element[4]}</span>
                                            <span class="badge badge-success">cos sim: ${element[0]}</span>
                                            <p>${element[3]}</p>
                                            <hr>`)
            })            
            // $('#queryArticles').append
        }
    })     
}

