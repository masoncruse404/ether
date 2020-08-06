$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,

    start: function (e) {
      console.log('upload started');
      $("#modal-progress").modal("show");
      $(".fuheader").css('display','flex');

    },

    stop: function (e) {
      $("#modal-progress").modal("hide");
    },

    progressall: function (e, data) {
      console.log('done');
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";

    },

    done: function (e, data) {
        console.log('done');
      if (data.result.is_valid) {
        console.log('done');
      }
    }

  });

});
