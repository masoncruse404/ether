var globalid;
$(document)
    .on('contextmenu', '.file-content', function(e) {
        //remove style from previous selected
        resetQA();
        resetFile();
        e.preventDefault();
        var i = this.id
        globalid = i;
        document.getElementById("rmenufolder").className = "hide";
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
        //if file is selected do not view on right click
        
        var url = "/star/";
        var renameurl = "/rename/";
        var full = url + i;
        renameurl = renameurl + i;
        var shareurl = "/share/"+ i + '/';
        var turl = "/trash/";
        var tfull = turl + i;
        var durl = "/download/" + i;
        var dfurl = "/downloadfolder/" + i;
        var movetourl = "/moveto/" + i;
      document.getElementById("rmenu").className = "show";
      document.getElementById("rmenu").style.top = mouseY(event) + 'px';
      document.getElementById("rmenu").style.left = mouseX(event) + 'px';
        document.getElementById("starred").onclick = function(){
            document.getElementById("addtostar").href = full;
        }

        document.getElementById("renamecontext").onclick = function(){
            $('#rename-popup').css('display','block');
            $(".cover").fadeTo(500, 0.5);
            $('#renameinput').focus();
            renameurl = renameurl + '/'
            $("#renameform").attr('action',renameurl)
        }
    
        document.getElementById("sharecontext").onclick = function(){
             document.getElementById("shareform").action = shareurl;

        }


        document.getElementById("download").onclick = function(){
            document.getElementById("download").href = durl;
        }

        document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = dfurl;
        }

        document.getElementById("trash").onclick = function(){
            document.getElementById("addtotrash").href = tfull;
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
$(document)
    .on('contextmenu', '.filetablerow', function(e) {
        //remove style from previous selected
        resetQA();
        resetFile();
	resetTableRow();
          document.getElementById("rmenufolder").className = "hide";

        e.preventDefault();
        var i = this.id
        globalid = i;
        console.log('i',i);
        var fileid  = i.substring(i.indexOf("-") + 1);
        console.log('fileid',fileid);
        var fid = '#filetablerow-' + fileid;
        console.log('fid',fid);
        $(fid).css('background', '#e8f0fe');
        //if file is selected do not view on right click
        
        var url = "/star/";
        var renameurl = "/rename/";
        var full = url + i;
        renameurl = renameurl + i;
        var shareurl = "/share/"+ i + '/';
        var turl = "/trash/";
        var tfull = turl + i;
        var durl = "/download/" + i;
        var dfurl = "/downloadfolder/" + i;
        var movetourl = "/moveto/" + i;
      document.getElementById("rmenu").className = "show";
      document.getElementById("rmenu").style.top = mouseY(event) + 'px';
      document.getElementById("rmenu").style.left = mouseX(event) + 'px';
        document.getElementById("starred").onclick = function(){
            document.getElementById("addtostar").href = full;
        }

        document.getElementById("renamecontext").onclick = function(){
            $('#rename-popup').css('display','block');
            $(".cover").fadeTo(500, 0.5);
            $('#renameinput').focus();
            renameurl = renameurl + '/'
            $("#renameform").attr('action',renameurl)
        }
    
        document.getElementById("sharecontext").onclick = function(){
             document.getElementById("shareform").action = shareurl;

        }


        document.getElementById("download").onclick = function(){
            document.getElementById("download").href = durl;
        }

        document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = dfurl;
        }

        document.getElementById("trash").onclick = function(){
            document.getElementById("addtotrash").href = tfull;
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


$(document)
    .on('contextmenu', '.qafilea', function(e) {
        //reset selected style
        resetFile();
        e.preventDefault();
        document.getElementById("rmenufolder").className = "hide";
        var i = this.id
        globalid = i;
        console.log('i',i);
        var qaid = '#qfooter' + i;
        var qafooterid = '#qaname' + i;
        console.log('qafooterid',qafooterid);
        resetQA();
        console.log('qaid',qaid);
        $(qaid).css('background', '#e8f0fe');
        $(qafooterid).css('color', '#1967d2');
        let b = "-";
        let position = 1;
        var trashid = i.substring(0, position) + b + i.substring(position);
        var url = "/star/";
        var full = url + trashid;
        var turl = "/trash/";
        let qid = i.substring(1);

        var renameurl = "/rename/g-" + qid;
        var tfull = turl + trashid;
        var durl = "/download/" + trashid;
        var dfurl = "/downloadfolder/" + trashid;
      document.getElementById("rmenu").className = "show";
      document.getElementById("rmenu").style.top = mouseY(event) + 'px';
      document.getElementById("rmenu").style.left = mouseX(event) + 'px';
        document.getElementById("starred").onclick = function(){
            document.getElementById("addtostar").href = full;
        }
          document.getElementById("starred").onclick = function(){
            document.getElementById("addtostar").href = full;
            
        }

        document.getElementById("moved").onclick = function(){
            $("#movetopopupwrap").css("display","flex");
            $("#movetoform").attr('action',movetourl)
        }



         document.getElementById("renamecontext").onclick = function(){
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

        document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = dfurl;
        }

        document.getElementById("trash").onclick = function(){
            document.getElementById("addtotrash").href = tfull;
        }

      window.event.returnValue = false;
});




// this is from another SO post...
$(document).bind("click", function(event) {
  //alert('here');

  document.getElementById("rmenu").className = "hide";
  document.getElementById("rmenufolder").className = "hide";
  document.getElementById("rmenuqa").className = "hide";
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

//$(document)
    //.on('contextmenu', '.qafilea', function(e) {
        //e.preventDefault();
        //var i = this.id
        //document.getElementById(i).click();
        //console.log(this.id);
        //var url = "/star/";
        //var full = url + i;
        //var turl = "/trash/";
        //var tfull = turl + i;
        //var durl = "/download/" + i;
        //var dfurl = "/downloadfolder/" + i;
        //console.log(full);
      //document.getElementById("rmenuqa").className = "show";
      //document.getElementById("rmenuqa").style.top = mouseY(event) + 'px';
      //document.getElementById("rmenuqa").style.left = mouseX(event) + 'px';
        //document.getElementById("starred").onclick = function(){
            //document.getElementById("addtostar").href = full;
        //}
//
        //document.getElementById("download").onclick = function(){
            //document.getElementById("download").href = durl;
        //}
//
        //document.getElementById("downloadfolder").onclick = function(){
            //document.getElementById("downloadfolder").href = dfurl;
        //}
//
        //document.getElementById("trash").onclick = function(){
            //document.getElementById("addtotrash").href = tfull;
            //console.log(tfull);
        //}
//
      //window.event.returnValue = false;
//});
//


// this is from another SO post...
$(document).bind("click", function(event) {
  document.getElementById("rmenu").className = "hide";
  document.getElementById("rmenufolder").className = "hide";
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
        globalid = i;
        document.getElementById("rmenu").className = "hide";
        var url = "/starfolder/";
        var full = url + i;
        var turl = "/trashfolder/";
        var tfull = turl + i;
        var durl = "/downloadfolder/" + i;
        var renameurl = "/renamefolder/" + i;
        var movetofolderurl = "/movefolderto/" + i;

      document.getElementById("rmenufolder").className = "show";
      document.getElementById("rmenufolder").style.top = mouseY(event) + 'px';
      document.getElementById("rmenufolder").style.left = mouseX(event) + 'px';
        document.getElementById("starredfolder").onclick = function(){
            document.getElementById("addtostarfolder").href = full;
        }

        document.getElementById("downloadfolder").onclick = function(){
            document.getElementById("downloadfolder").href = durl;
        }

        document.getElementById("trashfolder").onclick = function(){
            document.getElementById("addtotrashfolder").href = tfull;
        }
         

        document.getElementById("renamefoldercontext").onclick = function(){
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


// this is from another SO post...
$(document).bind("click", function(event) {
  document.getElementById("rmenu").className = "hide";
  document.getElementById("rmenufolder").className = "hide";
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

