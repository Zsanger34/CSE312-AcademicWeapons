document.addEventListener('DOMContentLoaded', function() {
    const bio = document.getElementById('bio');

    bio.addEventListener('input', function(event){
        const currentBio = event.target.value;
        const errorMessage = document.getElementById('editModalErrorMessage');
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
    const goodMessage = document.getElementById('editModelGoodMessage');
    modal.style.display = 'none';
    bio.value = '';
    profileImage.value = '';
    goodMessage.textContent = '';
}


async function submitChanges(event){
    event.preventDefault();
    const profileImage = document.getElementById('profileImage').files[0];
    const bio = document.getElementById('bio').value;
    const goodMessage = document.getElementById('editModelGoodMessage');
    const errorMessage = document.getElementById('.errorMessage');

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
            document.getElementById('user-bio').textContent = data["newBio"];
            goodMessage.textContent = 'Succesfully changed Bio';
        }else if ("pictureChanged" in data){
            // Handle picture change
            var newProfilePic = document.getElementById('profile-picture');
            newProfilePic.src = data["newPictureURL"];
            goodMessage.textContent = 'Succesfully changed Profile Picture';
        }else{
            // Handle picture change and bio change
            document.getElementById('user-bio').textContent = data["newBio"];
            var newProfilePic = document.getElementById('profile-picture');
            newProfilePic.src = data["newPictureURL"];
            goodMessage.textContent = 'Succesfully changed Bio and profile Picture';

        }

    } else if (response.status === 400) {
        errorMessage.textContent = data['errorMessage'];
    } else {
        console.error('Unexpected error', await response.text());
    }


}