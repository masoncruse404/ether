window.mobileAndTabletcheck = function() {
  var check = false;
  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
  return check;
};

function firstnamemobile(){
        if($('#id_first_name').val() == ''){
        $('#fnlabel').css('top','10');
        $('#fnlabel').css('color','grey');
        }
        else{
        $('#fnlabel').css('color','grey');
        }
}

function lastnamemobile(){
        if($('#id_last_name').val() == ''){
        $('#lnlabel').css('top','10');
        $('#lnlabel').css('color','grey');
        }
        else{
        $('#lnlabel').css('color','grey');
        }
}


function emailmobile(){
        if($('#id_email').val() == ''){
        $('#emlabel').css('top','314');
        $('#emlabel').css('color','grey');
        }
        else{
        $('#emlabel').css('color','grey');
        }
}

function repasswordmobile(){
        if($('#id_re_password').val() == ''){
        $('#confirmlabel').css('top','457');
        $('#confirmlabel').css('color','grey');
        }
        else{
        $('#confirmlabel').css('color','grey');
        }
}

function passwordmobile(){
        if($('#id_password').val() == ''){
        $('#pwlabel').css('top','457');
        $('#pwlabel').css('color','grey');
        }
        else{
        $('#pwlabel').css('color','grey');
        }
}

function mobilereset(){
        $('#pwlabel').css('top','457');
        $('#confirmlabel').css('top','457');
        $('#lnlabel').css('left','175');
        $('#confirmlabel').css('left','270');
        $('#emlabel').css('top','314');
        $('#etlabel').css('top','314');
        $('#etlabel').css('left','300');

}
if(mobileAndTabletcheck()){
    $(document).ready(function(){
    $("#ca").click(function(){
        $(this).children("input").toggle();
        firstnamemobile();
        lastnamemobile();
        emailmobile();
        passwordmobile();
        repasswordmobile();
    });
   $("input").click(function(e) {
        e.stopPropagation();
   });
});

 
    mobilereset();
    $("#id_first_name").focus(function(){
        lastnamemobile();
        passwordmobile();
        repasswordmobile();
        emailmobile();
        $('#fnlabel').css('top','-10');
        $('#fnlabel').css('color','4285F4');
        dfname = 1;
    });
    $("#id_last_name").focus(function(){
        firstnamemobile();
        passwordmobile();
        repasswordmobile();
        emailmobile();
        $('#lnlabel').css('top','-10');
        $('#lnlabel').css('color','4285F4');
        dfname = 1;
    });
    $("#id_email").focus(function(){
        firstnamemobile();
        passwordmobile();
        repasswordmobile();
        lastnamemobile();
        $('#emlabel').css('top','288');
        $('#emlabel').css('color','4285F4');
        dfname = 1;
    });
    $("#id_password").focus(function(){
        firstnamemobile();
        emailmobile();
        repasswordmobile();
        lastnamemobile();
        $('#pwlabel').css('top','439');
        $('#pwlabel').css('color','4285F4');
        dfname = 1;
    });
 
    $("#id_re_password").focus(function(){
        firstnamemobile();
        passwordmobile();
        emailmobile();
        lastnamemobile();
        $('#confirmlabel').css('top','439');
        $('#confirmlabel').css('color','4285F4');
        dfname = 1;
    });
 
 
}
else
{
    dfname = 0;
    function firstname(){
        if($('#id_first_name').val() == ''){
        $('#fnlabel').css('top','10');
        $('#fnlabel').css('color','grey');
        }
        else{
        $('#fnlabel').css('color','grey');
        }
    }
    function lastname(){
        if($('#id_last_name').val() == ''){
        $('#lnlabel').css('top','10');
        $('#lnlabel').css('color','grey');
        }
        else{
        $('#lnlabel').css('color','grey');
        }
    }

    function email(){
        if($('#id_email').val() == ''){
        $('#emlabel').css('top','302');
        $('#emlabel').css('color','grey');
        }
        else{
        $('#emlabel').css('color','grey');
        }
    }

    function password(){
        if($('#id_password').val() == ''){
        $('#pwlabel').css('top','440');
        $('#pwlabel').css('color','grey');
        }
        else{
        $('#pwlabel').css('color','grey');
        }
    }

    function repassword(){
        if($('#id_re_password').val() == ''){
        $('#confirmlabel').css('top','440');
        $('#confirmlabel').css('color','grey');
        }
        else{
        $('#confirmlabel').css('color','grey');
        }
    }
$(document).ready(function(){
    $("#ca").click(function(){
        $(this).children("input").toggle();
        firstname();
        lastname();
        email();
        password();
        repassword();
    });
   $("input").click(function(e) {
        e.stopPropagation();
   });
});

    $("#id_first_name").focus(function(){
        lastname();
        email();
        password();
        repassword();
        $('#fnlabel').css('top','-10');
        $('#fnlabel').css('color','4285F4');
        dfname = 1;
    });
    $("#id_email").focus(function(){
        lastname();
        firstname();
        password();
        repassword();
        $('#emlabel').css('top','274');
        $('#emlabel').css('color','4285F4');
    });
    $("#id_last_name").focus(function(){
        firstname();
        email();
        password();
        repassword();
        $('#lnlabel').css('top','-10');
        $('#lnlabel').css('color','4285F4');
    });

    $("#id_password").focus(function(){
        email();
        lastname();
        repassword();
        $('#pwlabel').css('top','417');
        $('#pwlabel').css('color','4285F4');
    });

    $("#id_re_password").focus(function(){
        email();
        lastname();
        firstname();
        password();

        $('#confirmlabel').css('top','417');
        $('#confirmlabel').css('color','4285F4');
    });
}
