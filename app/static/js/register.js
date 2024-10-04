document.getElementById('confirmpassword').addEventListener('input', function (){
    const password = document.getElementById('password').value;
    const confirmpassword = document.getElementById('confirmpassword').value;

    if(password === confirmpassword){
        document.getElementById('password').classList.add('match');
        document.getElementById('confirmpassword').classList.add('match')
    }else{
        document.getElementById('password').classList.remove('match');
        document.getElementById('confirm-password').classList.remove('match');
    }
});