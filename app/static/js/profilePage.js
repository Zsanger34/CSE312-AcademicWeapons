function showErrorMessage(errorMessage){
    const errorHTML = document.getElementById('error-message');
    errorHTML.textContent = errorMessage;
    errorHTML.style.display = 'flex';

    setTimeout(() => {
        errorHTML.classList.add('fade-out-message');
        setTimeout(() => {
            errorHTML.style.display = 'none';
            errorHTML.classList.remove('fade-out-message');
        }, 1000); 
        errorHTML.textContent = '';
    }, 3000);
}


function showGoodMessage(goodMessage){
    const goodHTML = document.getElementById('good-message');
    goodHTML.textContent = goodMessage;
    goodHTML.style.display = 'flex';

    setTimeout(() => {
        goodHTML.classList.add('fade-out-message');
        setTimeout(() => {
            goodHTML.style.display = 'none';
            goodHTML.classList.remove('fade-out-message');
        }, 1000); 
        goodHTML.textContent = '';
    }, 3000);
}


async function followUser(){
    const user = document.getElementById('userName').textContent
    const formData = new FormData();
    formData.append('chosenUser', user);
    try{

        const response = await fetch('/profile/followUser', {
            method: 'POST',
            body: formData,

        });

        verifyFollowed = await response.json();
        if (response.ok){
            //user was followed, change it so that it now displays to unfollow the user
            let goodMessage = verifyFollowed['goodMessage'];
            showGoodMessage(goodMessage);

        }else{
            //display error message saying following user failed for some reason
            let error = verifyFollowed['errorMessage'];
            showErrorMessage(error);
        }
    }catch (error){
        console.error('Error:', error);
    }

}


document.getElementById("logout").addEventListener("click", function() {
    window.location.href = "/logout";
});