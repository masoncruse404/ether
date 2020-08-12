 $(function(){
            $("#searchuinput").keyup(function () {
      var searchq = $("#searchuinput").val();
      console.log(searchq);
      $.ajax({
        type: "POST",
        url: '/ajax/searchajax/',
        data: {
          'searchq': searchq
        },
        success: searchSuccess,
        dataType: 'html'
        

    });
    });
});
function searchSuccess(data, textStatus, jqXHR){
      var searchq = $("#searchuinput").val();
    if(searchq.length === 0){

    $('#search-results-wrapper').css('display','none');
    $('#searchtypewrapper').css('display','block');
    }
    else
    {
    $('#search-results-wrapper').css('display','block');
    $('#searchtypewrapper').css('display','none');
    }
    $('#search-results-wrapper').html(data);
    console.log(data);
}   

 $(".shareuser").click(function(e) {
       alert('fucker');
        e.stopPropagation();
   });

