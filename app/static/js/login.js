//sending the data to flask and then flask sends a message back
document.addEventListener('DOMContentLoaded', () => {
    //declare our variables (form, seewehn )
    const form = document.querySelector('.registrationForm');
    const submitButton = document.getElementById('login');
    const errorMessage = document.getElementById('errormessage');

    submitButton.addEventListener('click', async(event) => {
        event.preventDefault();

        //getting the data from the form
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        //clear the messages
        errorMessage.innerHTML = '';

        //sending the data to the backend
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
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