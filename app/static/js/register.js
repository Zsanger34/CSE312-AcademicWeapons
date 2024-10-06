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
document.getElementById('password').addEventListener('input', function() {
    const password = this.value;
    
    // Check password rules
    const lengthRule = document.getElementById('length');
    const uppercaseRule = document.getElementById('uppercase');
    const lowercaseRule = document.getElementById('lowercase');
    const numberRule = document.getElementById('number');
    const specialRule = document.getElementById('special');

    // Rule: At least 10 characters
    if (password.length >= 10) {
        lengthRule.classList.add('valid');
    } else {
        lengthRule.classList.remove('valid');
    }

    // Rule: One uppercase letter
    if (/[A-Z]/.test(password)) {
        uppercaseRule.classList.add('valid');
    } else {
        uppercaseRule.classList.remove('valid');
    }

    // Rule: One lowercase letter
    if (/[a-z]/.test(password)) {
        lowercaseRule.classList.add('valid');
    } else {
        lowercaseRule.classList.remove('valid');
    }

    // Rule: One number
    if (/\d/.test(password)) {
        numberRule.classList.add('valid');
    } else {
        numberRule.classList.remove('valid');
    }

    // Rule: One special character
    if (/[!@#$%^&*]/.test(password)) {
        specialRule.classList.add('valid');
    } else {
        specialRule.classList.remove('valid');
    }
});
//sending the data to flask and then flask sends a message back
document.addEventListener('DOMContentLoaded', () => {
    //declare our variables (form, seewehn )
    const form = document.querySelector('.registrationForm');
    const submitButton = document.getElementById('create');
    const errorMessage = document.getElementById('errormessage');

    submitButton.addEventListener('click', async(event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const confirmpassword = document.getElementById('confirmpassword').value;

        //clear the messages
        errorMessage.innerHTML = '';

        //get the data from the form and send it to registration
       
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
                confirmpassword: confirmpassword
            }),
        });

        const result = await response.json();

        if (response.ok) {
            //there is no error and redirect them to the homepage
            window.location.href = '/';
        } else {
            //display the error messages
            let messages = [];
            for (let key in result) {
                if (result.hasOwnProperty(key)) {
                    messages.push(result[key]);
                }
            }
            errorMessage.innerHTML = `<ul><li>${messages.join('</li><li>')}</li></ul>`;
        }
        

    });//end of button submit
});
