var count = 0;
var numdone = 0;
var fileid = 0;
function startHover(){
$(document).on("mouseenter", ".fufilewrapper", function() {
    console.log("mouseneter");
    console.log(this);
  var elecheck = 'check' + this.id;
  $(this).children('.fucheck').css('display','none');
   $(this).children('.fufolder').css('display','flex');

});

$(document).on("mouseleave", ".fufilewrapper", function() {
    // hover ends code here
          $(this).children('.fufolder').css('display','none');
      $(this).children('.fucheck').css('display','flex');

      
});
}
$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,

    start: function (e) {
       $("#fu").css('display','block');
       $("#mbody").css('display','block');
      startHover();
      $(".fuheader").css('display','flex');
      $(".foldera").css('display','block');
        if(count == 0)
        {
            $(".futitle").text("Uploading 1 item");
        }
        else
        {
            $(".futitle").text("Uploading"+count+" items");
        }
        count = count + 1;
    },

    stop: function (e) {
      numdone = 0;
    },

    progressall: function (e, data) {
      console.log(data);
        if(count == 0)
        {
            $(".futitle").text("Uploading 1 item");
        }
        else
        {
            $(".futitle").text("Uploading "+count+" items");
        }
        count = count + 1;
      var $fufilewrapper = $("<div class='fufilewrapper'><i id='futype' class='far fa-image fa-lg'></i><span id='funame'>"+"</span></div>");
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },
    done: function (e, data) {
        //get id of last file in flexbox container
       if(numdone == 0){
              fileid = $('.flexbox').children().last().prev().attr('id');
              if(fileid){
                fileid = fileid.substring(1);

              }

       }
       $("#fu").css('display','block');
        numdone++;
        if(numdone== 1)
        {
            $(".futitle").text("Uploaded 1 item");
        }
        else
        {
            $(".futitle").text("Uploaded "+numdone+" items");
        }
      if (data.result.is_valid) {
           fileid++;
      //add file to upload popup
      var checkid = 'check' + numdone;
      var folderid = 'folder' + numdone;
      var $fufilewrapper = $("<div class='fufilewrapper' id=result-"+data.result.fileid+" onclick='findfile(this.id)'><i id='futype' class='far fa-image fa-lg'></i><span id='funame'>"+data.result.name+"</span><div class='fucheck' id="+checkid+"><i class='fas fa-check'></i></div><div id="+folderid+" class='fufolder'><i class='far fa-folder fa-lg'></i></div></div></div>");
      $("#mbody tbody").prepend($fufilewrapper);
        $("#gallery tbody").prepend(
          "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
        )
      }
      
      var id = data.result.fileid;
      var fid = 'f'+id;
      var newfileid = "f-" + id;
      var fcontentid = "fcontent-"+data.result.fileid;
      var imageid = 'img-' + id;
      //get file type
      var filetype = data.result.url.split('.').pop();
      console.log('filetype',filetype);
      var fileurl = 0;
      var footerid = "file-infof"+id;
    
        fileurl = data.result.url;
     
        var newfile =  "<div id='filetablerow-"+id+"' class='tablerowwrapper filetablerow' onclick='filetablerow(event,this.id)'>" +
        "<div class='tablenamecontainer'><div class='tableiconwrapper'><i class='fas fa-image'></i></div><div class='tablenamewrapper'><span>"+data.result.name+"</span>" +
        "</div></div><div class='tablerightwrapper'><div class='tablerightowner'><span>Me</span></div><div class='tablerightmodified'><span>Now</span></div><div class='tablerightfile'><span>-</span></div></div></div></div>";
    
      $(".filetablerow:last").after(newfile);

      
    }

  });

});
