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

async function unFollowUser(){
    const user = document.getElementById('userName').textContent
    const formData = new FormData();
    formData.append('chosenUser', user);
    try{
        const response = await fetch('/profile/unFollowUser', {
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


document.addEventListener('DOMContentLoaded', () => {
    
    let workouts = routineData

    async function fetchDays() {
        const daysContainer = document.getElementById('days-container');
        dayData.forEach(day => {
            workouts[day[1]] = workouts[day[1]] || [];
    
            const dayBox = document.createElement('div');
            dayBox.className = 'day-box';
    
            const dayHeader = document.createElement('h3');
            dayHeader.textContent = day[1];
    
            const dayTitle = document.createElement('h4');
            dayTitle.textContent = day[2];

            const exerciseList = document.createElement('div');
            exerciseList.className = 'exercise-list';
    
            //used for startup
            workouts[day[1]].forEach(exercise => {
                const exerciseDiv = startup(dayBox, exercise, day[1]);
                exerciseList.appendChild(exerciseDiv);
            });
    
            dayBox.appendChild(dayHeader);
            dayBox.appendChild(dayTitle);
            dayBox.appendChild(exerciseList);
            daysContainer.appendChild(dayBox);
        });
    }
    fetchDays();

    function startup(dayBox, exercise, day) {
        //get the values
        const { name, weight, reps, sets } = exercise;
        console.log(exercise)

        //create the workout box
        const exerciseDiv = document.createElement('div');
        exerciseDiv.className = 'exercise';
        const exerciseTitle = document.createElement('p');
        exerciseTitle.textContent = name;
        exerciseTitle.className = 'exercise_title'

        const exerciserow = document.createElement('div');
        exerciserow.className = 'exercise_row';

        const exerciseweight = document.createElement('p');
        const weight_name = `${weight} lbs`
        exerciseweight.textContent = weight_name;
        
        const exercisesets = document.createElement('p');
        const sets_name = `${sets} sets`
        exercisesets.textContent = sets_name;

        const exercisereps = document.createElement('p');
        const reps_name = `${reps} reps`
        exercisereps.textContent = reps_name;

        exerciserow.appendChild(exerciseweight)
        exerciserow.appendChild(exercisesets)
        exerciserow.appendChild(exercisereps)

        exerciseDiv.appendChild(exerciseTitle);
        exerciseDiv.appendChild(exerciserow);
        return exerciseDiv;
    }
});