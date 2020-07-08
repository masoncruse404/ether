$(document)
    .on('contextmenu', '.file-content', function(e) {
       resetQA();
        resetFile();
        e.preventDefault();
        var i = this.id

        console.log('i',i);
        var fileid  = i.substring(i.indexOf("-") + 1);
        console.log('fileid',fileid);
        var fid = '#file-infof' + fileid;
        var filefooterid = '#filefooter' + fileid;
        console.log('filefooterid',filefooterid);
        resetFile();
        console.log('fid',fid);
        $(fid).css('background', '#e8f0fe');
        $(filefooterid).css('color', '#1967d2');
        var url = "/removestar/";

        var full = url + i;
        var turl = "/trash/";
        var tfull = turl + i;
        var shareurl = "/share/"+ i + '/';
        var renameurl = "/renamestar/g-" + fileid;
        var movetourl = "/moveto/" + i;
        console.log(full);
      document.getElementById("rmenu").className = "show";
      document.getElementById("rmenu").style.top = mouseY(event) + 'px';
      document.getElementById("rmenu").style.left = mouseX(event) + 'px';
        document.getElementById("starred").onclick = function(){
            document.getElementById("addtostar").href = full;
        }

        document.getElementById("trash").onclick = function(){
            document.getElementById("addtotrash").href = tfull;
        }


           document.getElementById("sharecontext").onclick = function(){
             document.getElementById("shareform").action = shareurl;

        }

           document.getElementById("renamestar").onclick = function(){
            $('#rename-popup').css('display','block');
            $(".cover").fadeTo(500, 0.5);
            $('#renameinput').focus();
            renameurl = renameurl + '/'
            console.log('renameurl ',renameurl);
            $("#renameform").attr('action',renameurl);
        }
    
        document.getElementById("download").onclick = function(){
            document.getElementById("download").href = durl;
        }
        document.getElementById("moved").onclick = function(){
            $("#movetopopupwrap").css("display","flex");
            $("#movetoform").attr('action',movetourl)


        }


        document.getElementById("makeacopy").onclick = function(){
            document.getElementById("makeacopy").href = '/copyfile/'+i;
        }



      window.event.returnValue = false;
});

$(document).ready(function() {


  if ($(".file").addEventListener) {
    $(".file").addEventListener('contextmenu', function(e) {
      e.preventDefault();
    }, false);
  } else {

    //document.getElementById("test").attachEvent('oncontextmenu', function() {
    //$(".test").bind('contextmenu', function() {
    $('body').on('contextmenu', 'a.file', function() {


      //alert("contextmenu"+event);


    });
  }

});

// this is from another SO post...
$(document).bind("click", function(event) {
  document.getElementById("rmenufolderstar").className = "hide";
  document.getElementById("rmenu").className = "hide";
});



function mouseX(evt) {
  if (evt.pageX) {
    return evt.pageX;
  } else if (evt.clientX) {
    return evt.clientX + (document.documentElement.scrollLeft ?
      document.documentElement.scrollLeft :
      document.body.scrollLeft);
  } else {
    return null;
  }
}

function mouseY(evt) {
  if (evt.pageY) {
    return evt.pageY;
  } else if (evt.clientY) {
    return evt.clientY + (document.documentElement.scrollTop ?
      document.documentElement.scrollTop :
      document.body.scrollTop);
  } else {
    return null;
  }
}

$(document)
    .on('contextmenu', '.foldercontainer', function(e) {
        e.preventDefault();
        var i = this.id
        var url = "/removefolderstar/";
        var full = url + i;
        var turl = "/trashfolder/";
        var tfull = turl + i;
        var durl = "/downloadfolder/" + i;
        var renameurl = "/renamefolderstar/" + i;
        var movetofolderurl = "/movefolderto/" + i;

      document.getElementById("rmenufolderstar").className = "show";
      document.getElementById("rmenufolderstar").style.top = mouseY(event) + 'px';
      document.getElementById("rmenufolderstar").style.left = mouseX(event) + 'px';
        document.getElementById("starredfolder").onclick = function(){
            document.getElementById("addtostarfolder").href = full;
        }

        document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = durl;
        }


        document.getElementById("renamefolderstar").onclick = function(){
            $('#renamefolder-popup').css('display','block');
                        console.log('renameurl',renameurl);

            $(".cover").fadeTo(500, 0.5);
            $('#renamefolderinput').focus();
            renameurl = renameurl + '/'
            $("#renamefolderform").attr('action',renameurl)
        }


        document.getElementById("movetofolder").onclick = function(){
            $("#movetopopupwrap").css("display","flex");
            $("#movetoform").attr('action',movetofolderurl)


        }

      window.event.returnValue = false;
});