function fuclose()
{
    $("#fu").css('display','none');
}
function fudown()
{
    console.log('in fudowndog');
    if ($("#down").hasClass("flip")){

        $(".fufilewrapper").css('display','flex');
        $("#down").removeClass('flip');

    }else{

        $("#down").toggleClass('flip');
        $(".fufilewrapper").css('display','none');
    }

}
