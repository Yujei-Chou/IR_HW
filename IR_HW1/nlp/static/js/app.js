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

function PubMed_exist_handle(){
    if($('#PubMed-select option:visible').length > 0){
        $('#PubMedAlert').hide();
        $('#PubMedCard').show();
    }else{
        $('#PubMedAlert').show();
        $('#PubMedCard').hide();            
    }        
}

function Tweet_exist_handle(){
    if($('#Twitter-select option:visible').length > 0){
        $('#TweetAlert').hide();
        $('#TweetCard').show();
    }else{
        $('#TweetAlert').show();
        $('#TweetCard').hide();            
    }             
}

function find_keyword(PubMedDocs, TweetDocs, keyword){
    //Check if keyword in PubMed data
    let PubMed_foundCnt = 0
    $('#PubMed-select > option').hide();
    $('#PubMed-select > option').each(function(){
        let PMID = $(this).attr('pmid');
        let fileName = $(this).attr('filename');
        $.each(PubMedDocs[fileName][PMID]['Abstract'], function(key, value){
            if(annotate_keyword(value[0], keyword).found){
                PubMed_foundCnt += 1
                $(`#PubMed-select > option[pmid=${PMID}]`).show();
                return false;    
            }
        })
    });
    if(PubMed_foundCnt > 0){
        if($(`#PubMed-select > option:nth-child(${$('#PubMed-select').prop('selectedIndex')+1})`).is(":hidden")){
            $('#PubMed-select')
                .val($('#PubMed-select > option:visible:first').val())
                .trigger('change');
        }
    }
    PubMed_exist_handle()
    
    //Check if keyword in Twitter data
    let Tweet_foundCnt = 0
    $('#Twitter-select > option').hide();
    $('#Twitter-select > option').each(function(){
        let TWID = $(this).attr('twid');
        let fileName = $(this).attr('filename');
        $.each(TweetDocs[fileName][TWID]['Abstract'], function(index, value){
            if(annotate_keyword(value, keyword).found){
                Tweet_foundCnt += 1;
                $(`#Twitter-select > option[twid='${TWID}']`).show();
                return false;    
            }
        })
    });
    if(Tweet_foundCnt > 0){
        if($(`#Twitter-select > option:nth-child(${$('#Twitter-select').prop('selectedIndex')+1})`).is(":hidden")){
            $('#Twitter-select')
                    .val($('#Twitter-select > option:visible:first').val())
                    .trigger('change');     
        }         
    }
    Tweet_exist_handle();          
}

function PubMed_annotated(Obj, keyword){
    if($('#PubMed-select option').length > 0){
        $('#PubMedCard > div.card-body').empty();
        $.each(Obj['Abstract'], function(key, value){
            if(key !== "null"){
                $('#PubMedCard > div.card-body').append(`<b>${key}: </b>${annotate_keyword(value[0], keyword).res}<br><br>`);
            }else{
                $('#PubMedCard > div.card-body').append(`${annotate_keyword(value[0], keyword).res}`);
            }

        })    
    }    

}

function Tweet_annotated(Obj, keyword){
    if($('#Twitter-select option').length > 0){
        $('#TweetCard > div.card-body').empty();
        $.each(Obj['Abstract'], function(index, value){
            $('#TweetCard > div.card-body').append(`${annotate_keyword(value, keyword).res}<br>`)
        })
    }       
}


