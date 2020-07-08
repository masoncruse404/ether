//after login the is no active class on the nav items the is an easy temp fix
//if the is no active class make mydrive the active class
    $( document ).ready(function() {
      var isActive = 0;

    $(".nav-link").each(function(){
        if($(this).hasClass("active")){
          isActive = 1;
          
        }
    });
    if(!isActive){
      $("#mydrivelink").addClass("active");
      $("#mydrivenavitem").addClass("active");

    }
    console.log('isActive',isActive);
});