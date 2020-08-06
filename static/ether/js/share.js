$( "#sharecontext" ).click(function() {

	$("#share-popup").css("display","block");
	$("#shareinput").focus();
	$(".imgcover").fadeTo(500, 0.5);

});

function shareClose(){
	$("#share-popup").css("display","none");
}
function shareFolderClose(){
  $("#sharefolder-popup").css("display","none");
}
$( "#sharefolder" ).click(function() {
  console.log('share clicked')
  $("#sharefolder-popup").css("display","block");
  $("#sharefolderinput").focus();
  $(".imgcover").fadeTo(500, 0.5);

});

function shareClose(){
  $("#share-popup").css("display","none");
}



$( "#subhshare" ).click(function() {
	$("#share-popup").css("display","block");
	$("#shareinput").focus();
	console.log('lastid',lastClickedEle);
	//check if quickaccess was select if so format id
	if(lastClickedEle[0] == 'q'){
		console.log('qa');
		let id= [lastClickedEle.slice(0,1),'-', lastClickedEle.slice(1)].join('');
		console.log('format id',id);
		$("#shareform").attr('action','/share/'+id + '/');
		console.log($("#shareform").attr('action'));
	}
	else{
			$("#shareform").attr('action','/share/'+lastClickedEle + '/');
			console.log($("#shareform").attr('action'));
	}
	$(".imgcover").fadeTo(500, 0.5);

});

