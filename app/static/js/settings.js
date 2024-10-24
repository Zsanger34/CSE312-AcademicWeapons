//This function is for being able to create the drop down menu
function toggleDropdown(dropDownFormID){
    const dropDownForm = document.getElementById(dropDownFormID);
    if (dropDownForm.style.display == "block"){
        dropDownForm.style.display = "none";
    }else{
        dropDownForm.style.display = "block";
    }
}




async function NewUserNameForm(){
    const oldUsername = document.getElementById("oldUserName").value;
    const newUserName = document.getElementById("newUserName").value;
    const errorMessage = document.getElementById("changeUserNameErrorMessage");

    errorMessage.innerHTML = "";

    const response = await fetch('/settings/changeUserName', {
        method: 'POST',             
        headers: {'Content-Type': 'application/json', },
        body: JSON.stringify({oldUsername: oldUsername,newUserName: newUserName}),
    });

    //check the results
    const results = await response.json()
    if(response.ok){

    }else{
        //handle any errors here
    }

}


async function newPasswordForm(){
    const confirmOldPassword = document.getElementById("confirmOldPassword").value;
    const newPassword = document.getElementById("newPassword").value;
    const confirmNewPassword = document.getElementById("confirmNewPassword").value;
    const errorMessage = document.getElementById("changePasswordErrorMessage");

    errorMessage.innerHTML = "";

    const response = await fetch('/seetings/changePassword', {
        method: 'POST',
        headers: {},
        body: JSON.stringify({confirmOldPassword: confirmOldPassword, newPassword: newPassword, confirmNewPassword: confirmNewPassword }),
    });

    //check the results
    const results = await response.json()

    if(response.ok){

    }else{
        //handle any errors here
    }


}