function showImg(e){
	console.log('e',e);
	
	var id = e.split("-");
	id = id[1];
	console.log('id',id);

if (parentDiv.contains(childDiv)) {
  alert("yes");
}
	let x = $(e).attr('src');
	console.log('src',x);
	let ele = "<img src='"+x+"'></img>";
	
    $('.imgscreen').css('display','flex');
    $(".imgcover").fadeTo(500, 0.5);
	$(".imgscreen").css("background-image","url("+x+")");
	$(".imgscreen").css("background-repeat","no-repeat")
	$(".imgcoverclose").css('display','flex');
	

	


}

function showImgClose(){
	$(".imgcoverclose").css('display','none');
    $('.imgscreen').css('display', 'none');
    $(".imgcover").fadeOut(500);

}