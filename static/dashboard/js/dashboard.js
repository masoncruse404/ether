var isOpen = true;
//detach submenu
       
var sub = 0;
var isSmallSearch = false;
$(".searchwrappersmall").click(function(event){
    if(!isSmallSearch)
    {
        $("#small").css("display","flex");
        $("#small").css("justify-content","center");
        $("#small").css("align-items","center");
        $("#smallsearch").css("display","flex");
        isSmallSearch = true;
    }
    else
    {
        $("#small").css("display","none");
        isSmallSearch = false;
    }  
            
});
$(".navopenclose").click(function(event){

    event.preventDefault();
    if(isOpen){

        $(".sidenav").css("display","none");
        $(".wrapper").css("grid-template-columns","104px 1fr");
        $(".sidenavsmall").css("display","block");
        isOpen = false;
    }
    else
    {
        $(".sidenav").css("display","block");
        $(".wrapper").css("grid-template-columns","224px 1fr");
        $(".sidenavsmall").css("display","none");
        isOpen = true;
        location.reload()
    }
});

var isMenu = true;

var isSmall = $(".sidenavsmall").css('display') == 'none';

function myFunctionY(y) {
  if (y.matches){ // If media query matches
          $(".sidenav").css("display","block");
          $(".wrapper").css("grid-template-columns","224px 1fr");
          $(".sidenavsmall").css("display","none");
          $("#small").css("display","none");
          isOpen = true;
  } else {
          $(".sidenav").css("display", "none");
          $(".wrapper").css("grid-template-columns","104px 1fr");
          $(".sidenavsmall").css("display", "block");
          isOpen = false;
  }
}


function myFunction(x) {
  if (x.matches){ // If media query matches
        $(".sidenav").css("display", "none");
          $(".wrapper").css("grid-template-columns","104px 1fr");
          $(".sidenavsmall").css("display", "block");

  } 
}


    //remove small search Fsmall
function myFunctionZ(z) {
  if (z.matches){ // If media query matches
        $("#small").css("display", "none");
          

  } else {
         
  }
}

var y = window.matchMedia("(min-width:1200px)")
var x = window.matchMedia("(max-width: 920px)")
var z = window.matchMedia("(min-width: 695px)")
myFunction(x) // Call listener function at run time
x.addListener(myFunction)
myFunctionY(y)
y.addListener(myFunctionY)
myFunctionZ(z)
z.addListener(myFunctionZ)
      

 
    var menuWidth;

    $("#barswrapper").click(function(event) {
       let shown = $(".sidenavsmall").css("display") == 'none';

       if(shown){
            $(".wrapper").css("grid-template-columns","104px 1fr");
            $(".sidenavsmall").css("display", "block");
       } else {
            $(".sidenavsmall").css("display", "none");
            $(".wrapper").css("grid-template-columns","1fr");
       }

    });
       
    $(".sidebar-dropdown > a").click(function () {
        $(".sidebar-submenu").slideUp(200);
        if ($(this).parent().hasClass("active")) {
            $(".sidebar-dropdown").removeClass("active");
            $(this).parent().removeClass("active");
        } else {
            $(".sidebar-dropdown").removeClass("active");
            $(this).next(".sidebar-submenu").slideDown(200);
            $(this).parent().addClass("active");
        }

    });


     $(".sidebarsmall-dropdown > a").click(function () {
        $(".sidebar-submenu").slideUp(200);
        if ($(this).parent().hasClass("active")) {
            $(".sidebarsmall-dropdown").removeClass("active");
            $(this).parent().removeClass("active");
        } else {
            $(".sidebarsmall-dropdown").removeClass("active");
            $(this).next(".sidebar-submenu").css("position","absolute");
            $(this).next(".sidebar-submenu").css("left","120");
            $(this).next(".sidebar-submenu").css("width","200px");
            $(this).next(".sidebar-submenu").slideDown(200);


            $(this).parent().addClass("active");
        }

    });
    
    
      
      