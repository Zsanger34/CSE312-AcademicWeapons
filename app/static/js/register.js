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
            alert(result.message); // Example: Show success message
        } else {
            // Handle error response from Flask
            errorMessage.innerHTML = result.error;
        }
        

    });//end of button submit
});
