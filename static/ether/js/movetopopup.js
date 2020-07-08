var old = 0;

document.addEventListener("DOMContentLoaded", function() {
  // code...

        $('.movetoactive').find(".chevwrap").css("display","none");
        $('.movetofolderrow').click(function(id) {
        if(old){
           $(".chevwrap").removeClass("disblock");
        }
        $('.movetoactive').addClass("movetofolderrow");
        $(".movetofolderrow").removeClass("movetoactive");
        $(this).addClass("movetoactive");
        $(this).find(".chevwrap").addClass("disblock");
        $(this).removeClass('movetofolderrow');
         old = $(this)
        });
});
//moved is set to turn when a row in movetopopup is clicked
var moved = 0;
function movetorowclick(ele){
    var atc = $("#movetoform").attr('action');

    //if folder has been selected and the file has not been moved and another folder has been select
    //we remove the old folder id from the action url
    if(moved){
       atc = atc.slice(0,atc.length-ele.length-1);
       console.log('atc',atc.length);
       console.log('ele',ele.length);
    }

    //folder has been selected
    //format action for selected folder id
    atc += '-' + ele;
    $("#movetoform").attr('action', atc);
    moved = 1;

}

function movetopopupclose(){
    $("#movetopopupwrap").css("display","none");
}

