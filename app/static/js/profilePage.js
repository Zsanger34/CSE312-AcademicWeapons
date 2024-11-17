document.addEventListener("DOMContentLoaded", function() {
    
});




async function followUser(){
    try{

        const response = await fetch('/followUser', {

        })
    }catch (error){
        console.error('Error:', error);
    }

}


async function editPage(){
    try{
        const response = await fetch('/verifyUser', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }

        });

        const data = await response.json();

        if (data.verified  == false){
            alert('User verification failed.');
        }else{
            alert("you can edit page now");
        }

    }catch (error){
        console.error('Error:', error);
        alert('An error occurred during verification. Please try again later.');
    }

}

document.getElementById("logout").addEventListener("click", function() {
    window.location.href = "/logout";
});