var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);

//if the broswer is chrome move labels to correct since it was developed on firefox
if(isChrome){
	console.log("it is chrome");
	$("#confirmlabel").css("left","335px");
	$("#lnlabel").css("left","235px");
	$("#emlabel").css("top","300px");
}