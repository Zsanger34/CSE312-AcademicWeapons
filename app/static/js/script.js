document.addEventListener('DOMContentLoaded', function() {
    // Add subtle hover effect on header
    const header = document.querySelector('header h1');
    header.addEventListener('mouseover', () => {
        header.style.color = '#34495E';
    });
    header.addEventListener('mouseout', () => {
        header.style.color = '#4A90E2';
    });
});

//this logs out the user and clears the cookie and then redirecting them to a new page
document.addEventListener('DOMContentLoaded', () => {
    const logout = document.getElementById('logout');
    logout.addEventListener('click', async(event) => { 
        //when logout is clicked we will send a post request to the backend to clear the cookies

        //create the json response to send
        const response = await fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({action: "clear_cookies"}),
        });

        //wait for the response
        const result = await response.json();

        if (response.ok) {
            //after we get the response back from the backend go to login
            window.location.href = '/login';
        }
    }); //end log out event
});
