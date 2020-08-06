			var ogfirstnamevalue = "First Name";
			var oglastnamevalue = "Last Name";

			var ogemailvalue = 'Email Address';
			var ogpasswordvalue = 'Password';
			var ogpasswordcheckvalue = 'Password Check';
			function checkEmailEmpty(){
				let email = $("#id_email").val();
				if(email == ''){
					$("#id_email").val(ogemailvalue);
				}
			}
			function checkPasswordEmpty(){
				let pw = $("#id_password").val();
				if(pw == ''){
					$("#id_password").val(ogpasswordvalue);
				}
			}

			function checkPasswordCheckEmpty(){
				let pwcheck = $("#id_re_password").val();
				if (pwcheck == ''){
					$("#id_re_password").val(ogpasswordcheckvalue);
				}
			}

			function checkFirstNameEmpty(){
				let firstname = $("#id_first_name").val();
				if (firstname == ''){
					$("#id_first_name").val(ogfirstnamevalue);
				}
			}
			function checkLastNameEmpty(){
				let lastname = $("#id_last_name").val();
				if (lastname == ''){
					$("#id_last_name").val(oglastnamevalue);
				}
			}

			function checkLastNameSmallEmpty(){
				let lastname = $(".inputsmallscreenlastname").val();
				if (lastname == ''){
					$(".inputsmallscreenlastname").val(oglastnamevalue);
				}
			}

			function checkPasswordCheckSmallEmpty(){
				let pw = $(".inputsmallscreenpassword").val();
				if (pw == ''){
					$(".inputsmallscreenpassword").val(ogpasswordcheckvalue);
				}
			}

			const clearEmail = () => {
				let email = $("#id_email").val();
				if(email == ogemailvalue){
					$("#id_email").val('');

				}
			};

			const clearPassword = () => {
				let pw = $("#id_password").val();
				if(pw == ogpasswordvalue){
					$("#id_password").val('');
				}
			};

			const clearPasswordCheck = () => {
				let pw = $("#id_re_password").val();
				if(pw == ogpasswordcheckvalue){
					$("#id_re_password").val('');
				}
			};

			const clearFirstName = () => {
				let firstname = $("#id_first_name").val();
				if(firstname == ogfirstnamevalue){
					$("#id_first_name").val('');
				}
			};

			const clearLastName = () => {
				let ln = $("#id_last_name").val();
				if(ln == oglastnamevalue){
					$("#id_last_name").val('');
				}
			};

			const clearLastNameSmall = () => {
				let ln = $(".inputsmallscreenlastname").val();
				if(ln == oglastnamevalue){
					$(".inputsmallscreenlastname").val('');
				}
			};


			const clearPasswordCheckSmall = () => {
				let ln = $(".inputsmallscreenpassword").val();
				if(ln == ogpasswordcheckvalue){
					$(".inputsmallscreenpassword").val('');
				}
			};

			function outlineGrey(that){
				$(that).css({
					"border":"1px solid grey",
					"color":"grey"
				});
			}

			function outLineRed(that){
				$(that).css({
					"border":"1px solid red",
					"color":"red"
				});
			}

			function changePasswordToText(){
				let pw = $("#id_password").val();
				if(!pw){
					$("#id_password").get(0).type = 'text';
				}
			}

			function changePasswordCheckToText(){
				let pw = $("#id_re_password").val();
				if(!pw){
					$("#id_re_password").get(0).type = 'text';
				}
			}
			

			$("#loginwrap").click(function(event){
				window.location.href = '/users/login';

			});
			$('#submit').click(function(event){
    			event.stopPropagation();
			});
			$("#register").click(function(event){
				//check that email and pw are not empty
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();
				checkLastNameSmallEmpty();
				checkPasswordCheckSmallEmpty();

				let email = $("#id_email").val();
				let pw = $("#id_password").val();
				let pwcheck = $("#id_re_password").val();
				let pwchecksmall = $(".inputsmallscreenpassword").val();
				let firstname = $("#id_first_name").val();
				let lastname = $("#id_last_name").val();
				let lastnamesmall = $(".inputsmallscreenlastname").val();

				


				//user submitted form without supplying an email
				if(email == ogemailvalue){

					outLineRed($("#id_email"));
					
				}
				//user submitted form without supplying a pw
				if(pw == ogpasswordvalue){
						outLineRed($("#id_password"));
				
				}


				if(firstname == ogfirstnamevalue){
					outLineRed($("#id_first_name"));
				}

				if(lastname == oglastnamevalue){
					outLineRed($("#id_last_name"));
				}

				if(pwcheck == ogpasswordcheckvalue){
					outLineRed($("#id_re_password"));
				}

				if(lastnamesmall == oglastnamevalue){
					outLineRed($(".inputsmallscreenlastname"));
				}

				if(pwchecksmall == ogpasswordcheckvalue){
					outLineRed($(".inputsmallscreenpassword"));
				}
				//user entered email and pw 
				//login
				if(email && pw && lastnamesmall && lastname && firstname && email != ogemailvalue && pw != ogpasswordvalue && firstname != ogfirstnamevalue && lastname != oglastnamevalue && pwcheck != ogpasswordcheckvalue){
					//handle login
					alert(email);
				}


			});


			$(".registerwrapper").click(function(event){
				event.preventDefault();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();
				checkLastNameSmallEmpty();
				checkPasswordCheckSmallEmpty();
			});

			$(".registerright").click(function(event){
				event.preventDefault();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();
				checkLastNameSmallEmpty();
				checkPasswordCheckSmallEmpty();
			});
			$("#email").focus(function(event){
				changePasswordToText();
				changePasswordCheckToText();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();
				checkLastNameSmallEmpty();
				checkPasswordCheckSmallEmpty();

				
				outlineGrey(this);
			});

			$("#id_email").click(function(e){
				e.stopPropagation();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();
				clearEmail();
				outlineGrey(this);
			});


			$("#id_password").focus(function(event){
				$(this).get(0).type = 'password';
				$(this).css("padding-left","10px");
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();
				checkLastNameSmallEmpty();
				checkPasswordCheckSmallEmpty();

				clearPassword();
				outlineGrey(this);

			});

			$("#id_password").click(function(event){
				event.stopPropagation();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();

				clearPassword();
				outlineGrey(this);
			});

			$("#id_re_password").focus(function(event){
				$(this).get(0).type = 'password';
				$(this).css("padding-left","10px");
				checkPasswordEmpty();
				checkEmailEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();
				checkLastNameSmallEmpty();

				clearPasswordCheck();
				outlineGrey(this);

			});

			$("#id_re_password").click(function(event){
				event.stopPropagation();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();


				
				clearPasswordCheck();
				outlineGrey(this);
			});

			$("#id_first_name").focus(function(event){
				changePasswordToText();
				changePasswordCheckToText();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkLastNameEmpty();
				checkPasswordCheckSmallEmpty();

				checkFirstNameEmpty();
				checkLastNameSmallEmpty();
				clearFirstName();
				outlineGrey(this);

			});

			$("#id_first_name").click(function(event){
				event.stopPropagation();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkLastNameEmpty();

			
				clearFirstName();
				outlineGrey(this);
			});


			$("#id_last_name").focus(function(event){
				changePasswordToText();
				changePasswordCheckToText();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				

		

				clearLastName();
				outlineGrey(this);

			});

			$("#id_last_name").click(function(event){
				event.stopPropagation();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
			
				clearLastName();
				outlineGrey(this);
			});

			$(".inputsmallscreenlastname").click(function(event){
				event.stopPropagation();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				checkPasswordCheckSmallEmpty();
				checkPasswordCheckSmallEmpty();
				clearLastNameSmall();
				outlineGrey(this);
			
			});

			$(".inputsmallscreenpassword").click(function(event){
				event.stopPropagation();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();

				clearPasswordCheckSmall();
				outlineGrey(this);
			
			})


$( document ).ready(function() {
     checkEmailEmpty();
	 checkPasswordEmpty();
	 checkPasswordCheckEmpty();
	 checkFirstNameEmpty();
	 checkLastNameEmpty();
	 checkLastNameSmallEmpty();
	 checkPasswordCheckSmallEmpty()

});