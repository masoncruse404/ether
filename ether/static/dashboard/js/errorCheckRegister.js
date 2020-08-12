			var ogfirstnamevalue = "First Name";
			var oglastnamevalue = "Last Name";

			var ogemailvalue = 'Email Address';
			var ogpasswordvalue = 'Password';
			var ogpasswordcheckvalue = 'Password Check';
			function checkEmailEmpty(){
				let email = $("#email").val();
				if(email == ''){
					$("#email").val(ogemailvalue);
				}
			}
			function checkPasswordEmpty(){
				let pw = $("#password").val();
				if(pw == ''){
					$("#password").val(ogpasswordvalue);
				}
			}

			function checkPasswordCheckEmpty(){
				let pwcheck = $("#passwordcheck").val();
				if (pwcheck == ''){
					$("#passwordcheck").val(ogpasswordcheckvalue);
				}
			}

			function checkFirstNameEmpty(){
				let firstname = $("#firstname").val();
				if (firstname == ''){
					$("#firstname").val(ogfirstnamevalue);
				}
			}
			function checkLastNameEmpty(){
				let lastname = $("#lastname").val();
				if (lastname == ''){
					$("#lastname").val(oglastnamevalue);
				}
			}

			function checkLastNameSmallEmpty(){
				let lastname = $("#inputsmallscreenlastname").val();
				if (lastname == ''){
					$("#inputsmallscreenlastname").val(oglastnamevalue);
				}
			}

			function checkPasswordCheckSmallEmpty(){
				let pw = $("#inputsmallscreenpassword").val();
				if (pw == ''){
					$("#inputsmallscreenpassword").val(ogpasswordcheckvalue);
				}
			}

			const clearEmail = () => {
				let email = $("#email").val();
				if(email == ogemailvalue){
					$("#email").val('');

				}
			};

			const clearPassword = () => {
				let pw = $("#password").val();
				if(pw == ogpasswordvalue){
					$("#password").val('');
				}
			};

			const clearPasswordCheck = () => {
				let pw = $("#passwordcheck").val();
				if(pw == ogpasswordcheckvalue){
					$("#passwordcheck").val('');
				}
			};

			const clearFirstName = () => {
				let firstname = $("#firstname").val();
				if(firstname == ogfirstnamevalue){
					$("#firstname").val('');
				}
			};

			const clearLastName = () => {
				let ln = $("#lastname").val();
				if(ln == oglastnamevalue){
					$("#lastname").val('');
				}
			};

			const clearLastNameSmall = () => {
				let ln = $("#inputsmallscreenlastname").val();
				if(ln == oglastnamevalue){
					$("#inputsmallscreenlastname").val('');
				}
			};


			const clearPasswordCheckSmall = () => {
				let ln = $("#inputsmallscreenpassword").val();
				if(ln == ogpasswordcheckvalue){
					$("#inputsmallscreenpassword").val('');
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
				let pw = $("#password").val();
				if(!pw){
					$("#password").get(0).type = 'text';
				}
			}

			function changePasswordCheckToText(){
				let pw = $("#passwordcheck").val();
				if(!pw){
					$("#passwordcheck").get(0).type = 'text';
				}
			}
			

			$("#loginwrap").click(function(event){
				window.location.href = 'login.html';

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

				let email = $("#email").val();
				let pw = $("#password").val();
				let pwcheck = $("#passwordcheck").val();
				let pwchecksmall = $("#inputsmallscreenpassword").val();
				let firstname = $("#firstname").val();
				let lastname = $("#lastname").val();
				let lastnamesmall = $("#inputsmallscreenlastname").val();

				console.log('email: ',email);
				console.log('pw: ',pw);

				//user submitted form without supplying an email
				if(email == ogemailvalue){

					outLineRed($("#email"));
					
				}
				//user submitted form without supplying a pw
				if(pw == ogpasswordvalue){
						outLineRed($("#password"));
				
				}


				if(firstname == ogfirstnamevalue){
					outLineRed($("#firstname"));
				}

				if(lastname == oglastnamevalue){
					outLineRed($("#lastname"));
				}

				if(pwcheck == ogpasswordcheckvalue){
					outLineRed($("#passwordcheck"));
				}

				if(lastnamesmall == oglastnamevalue){
					outLineRed($("#inputsmallscreenlastname"));
				}

				if(pwchecksmall == ogpasswordcheckvalue){
					outLineRed($("#inputsmallscreenpassword"));
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

			$("#email").click(function(e){
				e.stopPropagation();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();
				clearEmail();
				outlineGrey(this);
			});


			$("#password").focus(function(event){
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

			$("#password").click(function(event){
				event.stopPropagation();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();

				clearPassword();
				outlineGrey(this);
			});

			$("#passwordcheck").focus(function(event){
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

			$("#passwordcheck").click(function(event){
				event.stopPropagation();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkFirstNameEmpty();
				checkLastNameEmpty();


				
				clearPasswordCheck();
				outlineGrey(this);
			});

			$("#firstname").focus(function(event){
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

			$("#firstname").click(function(event){
				event.stopPropagation();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkLastNameEmpty();

			
				clearFirstName();
				outlineGrey(this);
			});


			$("#lastname").focus(function(event){
				changePasswordToText();
				changePasswordCheckToText();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
				

		

				clearLastName();
				outlineGrey(this);

			});

			$("#lastname").click(function(event){
				event.stopPropagation();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();
			
				clearLastName();
				outlineGrey(this);
			});

			$("#inputsmallscreenlastname").click(function(event){
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

			$("#inputsmallscreenpassword").click(function(event){
				event.stopPropagation();
				checkPasswordEmpty();
				checkEmailEmpty();
				checkPasswordCheckEmpty();
				checkFirstNameEmpty();

				clearPasswordCheckSmall();
				outlineGrey(this);
			
			})


