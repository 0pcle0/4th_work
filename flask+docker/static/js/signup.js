	function checkform() {

		var name = document.getElementById("name");
		var username = document.getElementById("username");
		var pw = document.getElementById("password");
		var pw2 = document.getElementById("password2");
		var tel = document.getElementById("tel");
		var age =  document.getElementById("age");

		if(username.value==""){
 		alert("아이디를 입력하세요.");
 		username.focus();

		} else if(name.value==""){
		alert("이름을 입력하세요.");
		name.focus();

		} else if(tel.value==""){
		alert("전화번호를 입력하세요.");
		tel.focus();
 		

		} else if(pw.value==""){
 		alert("비밀번호를 입력하세요.");
 		pw.focus();
 		

		} else if(pw2.value==""){
 		alert("비밀번호를 재입력하세요.");
 		pw2.focus();
 		

		} else if(age.value==""){
 		alert("나이를 입력하세요.");
 		age.focus();
 		

		} else if(pw.value!=pw2.value){
		alert("비밀번호가 일치하지 않습니다.");
		pw2.focus();
		

		} else if(age.value > 105){
		alert("나이를 제대로 입력해주세요.");
		age.focus();
		
		
		} else if(age.value < 15){
		alert("15세 미만은 가입할 수 없습니다.");
		age.focus();
		

		} else {
		alert("회원가입이 완료되었습니다.");
		submit( );
		}

	}
