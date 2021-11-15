function drawPCA_3D(keyword){
    $('#Graph3D-Body').empty()
    $.ajax({
        url: 'drawPCA',
        method: 'POST',
        data: {
            keyword: keyword,
            type: '3D'
        },
        success: function(data){
            $('#Graph3D-Body').html(data.graph) 
            console.log(data.sim_list)
            $('.CS-Header').show()
            window.scrollTo(0,document.body.scrollHeight)
            $('#CS-Body').append(`<h4 class="fw-bold">Server migration<span style="float: right">20%</span></h4>
                                  <div class="progress"><div class="progress-bar progress-bar-striped" role="progressbar" style="width: 50%" aria-valuemin="0" aria-valuemax="100"></div></div>`)
        }
    }) 
}

function drawPCA_2D(){
    let keywordList = $('input[name=searchVec]').val().split(' ')
    $('#search-btn').prop('disabled', true)
    $('.bi-search').hide()
    $('#search-div > div > button > span').css('display', 'flex')
    $('#keywords').empty()
    $('#Graph3D-Body').empty() 
    $('#Graph2D-Body').empty()
    $.ajax({
        url: 'drawPCA',
        method: 'POST',
        data: {
            keyword: $('input[name=searchVec]').val(),
            type: '2D'
        },
        success: function(data){
            $('#search-btn').prop('disabled', false)
            $('.bi-search').show()
            $('#search-div > div > button > span').hide()            
            for(let i=0; i<keywordList.length; i++){
                $('#keywords').append(`<a href="#" class="badge badge-info" onclick="drawPCA_3D('${keywordList[i]}')">${keywordList[i]}</a>`)
            }
            $('#Graph2D-Body').html(data)
            $('.Graph2D-Header').show()
            $('.Graph3D-Header').show()
        }
    })    
}