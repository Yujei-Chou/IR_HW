function drawPCA_3D(keyword){
    $('#Graph3D-Body').empty()
    $('#CS-Body').empty()
    $.ajax({
        url: 'drawPCA',
        method: 'POST',
        data: {
            keyword: keyword,
            type: '3D'
        },
        success: function(data){
            $('#Graph3D-Body').html(JSON.parse(data).graph) 
            console.log(JSON.parse(data).similarity)
            $('.CS-Header').show()
            window.scrollTo(0,document.body.scrollHeight)
            let progressList = ['bg-success', 'bg-success', 'bg-warning', 'bg-warning', 'bg-danger']
            JSON.parse(data).similarity.forEach((element, idx) => {
                let key = Object.keys(element)[0]
                let value = (element[Object.keys(element)[0]]*100).toFixed(2)
                console.log(idx)
                $('#CS-Body').append(`<h4 class="fw-bold">${key}<span style="float: right">${value}%</span></h4>
                                      <div class="progress"><div class="progress-bar progress-bar-striped ${progressList[idx]}" role="progressbar" style="width: ${value}%" aria-valuemin="0" aria-valuemax="100"></div></div>`)
            })
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
    $('#CS-Body').empty()
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