document.addEventListener('DOMContentLoaded', function() {
    const bio = document.getElementById('bio');

    bio.addEventListener('input', function(event){
        const currentBio = event.target.value;
        const errorMessage = document.getElementById('bioError');
        if (currentBio.length > 100){
            bio.value = bio.value.substring(0, 100);
            errorMessage.textContent = "too many characters, limit is 100"
            errorMessage.style.display = 'block';
        }else{
            errorMessage.textContent = ""
            errorMessage.style.display = 'none';
        }
    })
});


function editPage() {
    const modal = document.getElementById('editProfileModal');
    modal.style.display = 'block';
}


function closeEditPage(){
    const modal = document.getElementById('editProfileModal');
    const bio = document.getElementById('bio')
    const profileImage = document.getElementById('profileImage')
    modal.style.display = 'none';
    bio.value = '';
    profileImage.value = '';
}


async function submitChanges(event){
    event.preventDefault();
    const profileImage = document.getElementById('profileImage').files[0];
    const bio = document.getElementById('bio').value;
    const bioError = document.querySelector('.bioError');
    const errorMessage = document.querySelector('.errorMessage');

    const formData = new FormData();
    formData.append('bio', bio);
    if (profileImage) {
        formData.append('profileImage', profileImage);
    }


    const response = await fetch('/profile/profileEdit', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        if ("bioChanged" in data) {
            // Handle bio change 
            document.getElementById('bio').textContent = data["newBio"];
        }else if ("pictureChanged" in data){
            // Handle picture change

        }else{
            // Handle picture change and bio change

        }

    } else if (response.status === 400) {
        console.error('Bad request');
    } else {
        console.error('Unexpected error', await response.text());
    }


}