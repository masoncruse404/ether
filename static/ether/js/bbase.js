var box = document.querySelector('#newfolder-popup');
var lastID = 0;
var lastClickedEle = 0;
//show newsubfolder popup
function newFolder(){
    $('#newfolder-popup').css('display','block');
    $(".cover").fadeTo(500, 0.5);
    $('#newfolderinputq').focus();
}


//show newsubfolder popup
function newSubFolder(){
    $('#newsubfolder-popup').css('display','block');
    $(".cover").fadeTo(500, 0.5);
    $('#newsubfolderinput').focus();
}

//reset style of file container
function resetFile(){
    $('.list-footer').css('background', '#ffffff');
    $('.file-icon').css('color','black');
    $('.list-footer').css('color', 'black');
    $('.filenamespan').css('color', 'black');
}

function resetTableRow(){
	$('.filetablerow').css('background','#ffffff');
}
var audiostate = 0;
function showImg(e){

    //image has been shown reset clicks to first click
    firstQaClick = 1;
    firstFileClick = 1;

    //e is id number
    //format e to be the class name of the selected img
    lastID = e;
    var a = '.audio-'+e;
    var ap = '.audiopopup-'+e;
    var audiosrcid = '#audiosource-'+e;
    console.log('audiosrcid',audiosrcid);
    var audiosrc = $(audiosrcid).attr('src');
    $("#theaudiosource").attr('src',audiosrc);
    console.log('audiosrc',audiosrc);
    e = '.img-' + e;
    console.log('e',e);
    var parentEle = $(e);
    $("#theaudioplayer").css("display","block");


    var isAudio = parentEle.hasClass("audiofile");
    var isVideo = parentEle.hasClass("videofile");

    if(isAudio && !audiostate){
        console.log('herein auido');
        $(a).detach().appendTo("body");
        audiostate = 1;
        console.log('audio');
        console.log('a',a);
        $(a).css("display","block");
        $(a).addClass("audiopopup");
        $(".audiopopup").css("display","block");
        $(ap).css("display","block");
        console.log
        $("#audio-"+lastID).css("display","block");
        $("#audio-"+lastID).removeClass("audiosidebar").addClass("audiopopup");
        $(".imgcover").fadeTo(500, 0.5);


    }else if(isVideo){
        console.log('it is a video');
    }
    else{


    let x = $(e).attr('src');
    console.log('src',x);
    let ele = "<img src='"+x+"'></img>";
    $('.imgscreen').css('display','flex');
    $(".imgcover").fadeTo(500, 0.5);
    $(".imgscreen").css("background-image","url("+x+")");
    $(".imgscreen").css("background-repeat","no-repeat")
    $(".imgcoverclose").css('display','flex');
    }
    //show image

}

//closes fullscreen image
function showImgClose(){
    $(".imgcoverclose").css('display','none');
    $('.imgscreen').css('display', 'none');
    $(".imgcover").fadeOut(500);

}

//when

var lastClickedID = 0;
var lastClicked = 0;
var firstFileClick = 1;
var isViewed = 0;
var selectedfile = 0;
var fileViewed = 0;
function t(event, ele){
    lastClickedEle = ele;
    //hide context menu if file is left clicked
    document.getElementById("rmenu").className = "hide";
    //save the original element id for use later
    var savedele = ele;
    lastClickedID = ele;
    if(firstFileClick){
        console.log('first click');

        //extract the id number from class name
        selectedfile = ele.substring(ele.indexOf("-") + 1);
        ele = ele.substring(ele.indexOf("-") + 1);
        console.log('selectedfile',selectedfile);
        firstFileClick = 0;
    }else{
        //removing characters infront of id number
        console.log('second click');
        ele = ele.substring(ele.indexOf("-") + 1);
        console.log('ele',ele);
        console.log('selectedfile',selectedfile);
        //file is clicked twice in a row
        if(selectedfile == ele){
            //display image
            showImg(ele);
        }
            //after an image has been viewed treat next click as first click
            firstFileClick = 1;

    }

    //a file has been selected reset all style
    resetQA();
    resetFile();
    resetTableRow();

    //display actions for file in subheader
    $('#file-icon').css('color','black');
    $('.sub-wrapper').css('display', 'block');
    $('.vert').css('display', 'block');


    //set subheader trash icon to correct url
    document.getElementById('subhtrash').href = '/trash/' + savedele;


    //set style of selected file
    var fileid = '#file-infof'+ele;
    console.log('fileid',fileid);
    $(fileid).css('background-color', '#e8f0fe');
    $('#filefooter'+ele).css('color', '#1967d2');

    //stop multiple fires 'clicks' from one single click
    $(this).off('click');
    event.stopPropagation? event.stopPropagation() : event.cancelBubble = true;
    return false;
}

var lastClickedID = 0;
var lastClicked = 0;
var firstFileClick = 1;
var isViewed = 0;
var selectedfile = 0;
var fileViewed = 0;
function filetablerow(event, ele){
    //hide context menu if file is left clicked
   
    document.getElementById("rmenu").className = "hide";
    //save the original element id for use later
    var savedele = ele;
    lastClickedID = ele;
    if(firstFileClick){
        console.log('first click');

        //extract the id number from class name
        selectedfile = ele.substring(ele.indexOf("-") + 1);
        ele = ele.substring(ele.indexOf("-") + 1);
        console.log('selectedfile',selectedfile);
        firstFileClick = 0;
    }else{
        //removing characters infront of id number
        console.log('second click');
        ele = ele.substring(ele.indexOf("-") + 1);
        console.log('ele',ele);
        console.log('selectedfile',selectedfile);
        //file is clicked twice in a row
        if(selectedfile == ele){
            //display image
            showImg(ele);
        }
            //after an image has been viewed treat next click as first click
            firstFileClick = 1;

    }

    //a file has been selected reset all style
    resetQA();
    resetFile();
    resetTableRow();

    //display actions for file in subheader
    $('#file-icon').css('color','black');
    $('.sub-wrapper').css('display', 'block');
    $('.vert').css('display', 'block');


    //set subheader trash icon to correct url
    document.getElementById('subhtrash').href = '/trash/' + savedele;


    //set style of selected file
    var fileid = '#filetablerow-'+ele;
    console.log('fileid',fileid);
    $(fileid).css('background-color', 'rgba(0,0,0,.05');

    //stop multiple fires 'clicks' from one single click
    $(this).off('click');
    event.stopPropagation? event.stopPropagation() : event.cancelBubble = true;
    return false;
}


function resetQA(){
    $('.qafooter').css('background', '#ffffff');
    $('.qafooter').css('color', 'black');
    $('.qaname').css('color', 'black');
    $('.qaicon').css('color','black');
}

var firstQaClick = 1;
var isViewedQ = 0;
var lastClickedQ = 0;
var selectedqa = 0;
var qaViewed = 0;

function q(event, ele){

    lastClickedEle = ele;
    console.log('lat clicked ',lastClickedEle)
     //hide context menu if file is left clicked

    document.getElementById("rmenu").className = "hide";
    let qaid = ele.substring(1,ele.length);
    if(firstQaClick){
        console.log('first click');
         //removing characters infront of id number
        selectedqa = ele.substring(1,ele.length);

        console.log('selectedfile',selectedqa);
        firstQaClick = 0;
    }else{
        //removing characters infront of id number
        console.log('second click');
        console.log('ele',qaid);
        console.log('selectedfile',selectedqa);
        if(selectedqa == qaid){
            showImg(qaid);

        }
            firstQaClick = 1;

    }
    console.log('lastClicked',lastClickedQ);


    //a file has been selected reset all style
    resetFile();
    resetTableRow();
    resetQA();

    if (ele != null){
    console.log(ele);
    // adding '-' the middle of name and id for regex
    var s = ele.substring(0,1) + '-' + ele.substring(1)
    }

    //set subheader trash icon to correct url
    document.getElementById('subhtrash').href = '/trash/' + s;

    //display actions for file in subheader
    $('#file-icon').css('color','black');
    $('.sub-wrapper').css('display', 'block');
    $('.vert').css('display', 'block');

    //set style of selected file
    $('#qfooter'+ele).css('background', '#e8f0fe');
    $('#qfooter'+ele).css('color', '#1967d2');
    $('#qaname'+ele).css('color', '#1967d2');

    //stop multiple fires 'clicks' from one single click
    $(this).off('click');
    event.stopPropagation? event.stopPropagation() : event.cancelBubble = true;
    return false;
}

//close new folder popup
function newFolderClose(){
    $('#newfolder-popup').css('display', 'none');
    $(".cover").fadeOut(500);

}

//close new folder popup
function newSubFolderClose(){
    $('#newfolder-popup').css('display', 'none');
    $(".cover").fadeOut(500);

}


//close rename poup
function renameClose(){
    $('#rename-popup').css('display', 'none');
    $(".cover").fadeOut(500);

}
function renameFolderClose(){
    $('#renamefolder-popup').css('display', 'none');
    $(".cover").fadeOut(500);

}
function showImgH(){

    let argid = 0;
    console.log('last lastClickedEle', lastClickedEle)
    console.log('in show img ',lastClickedID)
    if(lastClickedEle.toString().substring(0,1) == 'q'){
        //quick access file was selected
        argid = lastClickedEle.substring(1,lastClickedID.length)
    }
    else{
        //file container was selected
     
        argid = lastClickedID.substring(lastClickedID.toString().indexOf("-") + 1);

    }

    showImg(argid);
}

function userinfoclick(event){
    event.preventDefault()
}

//show or hide userinfo popup
function userinfoToggel(){
    if($('#user-info-p').css('display') == 'none'){
        $('#user-info-p').css('display', 'block');
    }
    else
    {
        $('#user-info-p').css('display', 'none');
    }
}

document.addEventListener("click", function(event){
    if (event.target.closest('.new-btn-wrapper')){
        console.log("inside");
        $('#new-popup').css('display', 'block');

    }
    else if (event.target.closest('.qafilea')){
            }
    else if (event.target.closest('.filecontainer-wrapper')){
            }
    else if (event.target.closest('.user-info')){
        console.log("user-info");
    }
    else if (event.target.closest('.file-content')){
    }
    else if (event.target.closest('#img')){
    }
    else if (event.target.closest('#fontent')){
    }
    else if (event.target.closest('#f')){
    }
    else if (event.target.closest("#subheye")){

    }
    else if (event.target.closest("#sharecontext")){

    }
    else if (event.target.closest("#shareinput")){

    }
    else if (event.target.closest("#subhshare")){

    }
    else if (event.target.closest(".shareuser")){

    }
    else if (event.target.closest("#user-info-p")){

    }
    else{
        console.log('audio-'+lastID);
        var myAudio = document.getElementById('audio-'+lastID);
        if(myAudio){
        if (myAudio.duration > 0 && !myAudio.paused) {
            $("#audio-"+lastID).attr('class','');
            $("#audio-"+lastID).attr('class','audiosidebar');
            audiostate = 1;
    //Its playing...do your job
        } else {
            $("#audio-"+lastID).attr("style","");
            $(".audiopopup").css("display","none");
            $("#audio-"+lastID).css("display","none");
            $("#audio-"+lastID).removeClass('audiosidebar')
            audiostate = 0;
    //Not playing...maybe paused, stopped or never played.

        }

        }
        //close viewed fullscreen img
        $(".imgcoverclose").css('display','none');
        $('.imgscreen').css('display', 'none');
        $(".imgcover").fadeOut(500);

        //close header features
        $('#new-popup').css('display', 'none');
        $('.filetablerow').css('background-color','#ffffff');
        $('#user-info-p').css('display', 'none');
        $('.sub-wrapper').css('display', 'none');
        $('.vert').css('display', 'none');
        $('.list-footer').css('background', '#ffffff');
        $('.list-footer').css('color', 'black');
        $('#file-icon').css('color', 'black');
        $('.qafooter').css('background', '#ffffff');
        $('.qaname').css('color', 'black');
        $('.qafooter').css('color', 'black');
        $('.filenamespan').css('color', 'black');
        $("#search-results-wrapper").css("display","none");
        $("#share-popup").css("display","none");


    }

});

