		var ogemailvalue = 'Enter Email Address....';
			var ogpasswordvalue = 'Password';
			function checkEmailEmpty(){
				let email = $(".loginemail").val();
				if(email == ''){
					$(".loginemail").val(ogemailvalue);
				}
			}
			function checkPasswordEmpty(){
				let pw = $("#pw").val();
				if(pw == ''){
					$("#pw").val(ogpasswordvalue);
				}
			}

			const clearEmail = () => {
				let email = $(".loginemail").val();
				if(email == ogemailvalue){
					$(".loginemail").val('');

				}
			};

			const clearPassword = () => {
				let pw = $("#pw").val();
				if(pw == ogpasswordvalue){
					$("#pw").val('');
				}
			};

			function outlineGrey(that){
				$(that).css({
					"border":"1px solid grey",
					"color":"grey"
				});
			}
			
			$(".loginbtn").click(function(event){
				//check that email and pw are not empty
				checkPasswordEmpty();
				checkEmailEmpty();

				let email = $(".loginemail").val();
				let pw = $("#pw").val();

				console.log('email: ',email);
				console.log('pw: ',pw);

				//user submitted form without supplying an email
				if(email == ogemailvalue){

					$(".loginemail").css({
						"border":"1px solid red",
						"color":"red"
					});
					
				}
				//user submitted form without supplying a pw
				 if(pw == ogpasswordvalue){
			
					$("#pw").css({
						"border":"1px solid red",
						"color":"red"
					});
				}
				//user entered email and pw 
				//login
				if(email && pw && email != ogemailvalue && pw != ogpasswordvalue){
					//handle login
					alert(email);
				}


			});

			$("#createwrap").click(function(e){
				window.location.href = 'register.html';
			});

			$(".loginwrapper").click(function(e){
				e.preventDefault();
				checkPasswordEmpty();
				checkEmailEmpty();
			});
			$(".wrapper").click(function(e){
				e.preventDefault();
				checkPasswordEmpty();
				checkEmailEmpty();
			});
			$(".loginemail").focus(function(event){
				checkPasswordEmpty();
				clearEmail();
				outlineGrey(this);
			});

			$(".loginemail").click(function(event){
				event.stopPropagation();
				checkPasswordEmpty();
				clearEmail();
				outlineGrey(this);
			});


			$("#pw").focus(function(event){
				checkEmailEmpty();
				clearPassword();
				outlineGrey(this);

			});

			$("#pw").click(function(event){
				event.stopPropagation();
				checkEmailEmpty();
				clearPassword();
				outlineGrey(this);
			});
