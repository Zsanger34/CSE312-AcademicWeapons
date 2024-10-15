//This function is for being able to create the drop down menu
function toggleDropdown(dropDownFormID){
    const dropDownForm = document.getElementById(dropDownFormID);
    if (dropDownForm.style.display == "block"){
        dropDownForm.style.display = "none";
    }else{
        dropDownForm.style.display = "block";
    }
}




function NewUserNameForm(){

}


function newPasswordForm(){
    const confirmOldPassword = document.getElementById("confirmOldPassword").value
    const newPassword = document.getElementById("newPassword").value
    const confirmNewPassword = document.getElementById("confirmNewPassword").value
}