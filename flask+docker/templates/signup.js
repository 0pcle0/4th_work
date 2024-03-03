	function checkform() {

		var username = document.getElementById("username");
		var pw = document.getElementById("password");
		var pw2 = document.getElementById("password2");
		var age =  document.getElementById("age");

		if(username.value==""){
 		alert("아이디를 입력하세요.");
 		username.focus();
 		return false;

		} else if(pw.value==""){
 		alert("비밀번호를 입력하세요.");
 		pw.focus();
 		return false;

		} else if(pw2.value==""){
 		alert("비밀번호를 재입력하세요.");
 		pw2.focus();
 		return false;

		} else if(age.value==""){
 		alert("나이를 입력하세요.");
 		age.focus();
 		return false;

		} else if(pw.value!=pw2.value){
		alert("비밀번호가 일치하지 않습니다.");
		pw2.focus();
		return false;

		} else if(age.value > 105){
		alert("나이를 제대로 입력해주세요.");
		age.focus();
		return false;
		
		} else if(age.value < 15){
		alert("15세 미만은 가입할 수 없습니다.");
		age.focus();
		return false;

		} else {
		alert("회원가입이 완료되었습니다.");
		submit( );
		}

	}
