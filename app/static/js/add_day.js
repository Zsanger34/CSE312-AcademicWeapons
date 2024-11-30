
document.addEventListener('DOMContentLoaded', () => {
    
    const addDayButton = document.querySelector('#add_day_button');
    const gobackbutton = document.querySelector('#go_back');
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
    
            const add_exercise = document.createElement('div');
            add_exercise.className = 'add_exercise';

            const title_day =  document.createElement('h3');
            title_day.textContent = 'Create an Exercise';
            title_day.className = 'title_day';
    
            const exerciseInput = document.createElement('input');
            exerciseInput.type = 'text';
            exerciseInput.placeholder = `Add Exercise for ${day[1]}`;
            exerciseInput.className = 'exercise-input';
            exerciseInput.maxLength = 50;
            exerciseInput.oninput = function () {this.value = this.value.replace(/[^a-zA-Z ()-]/g, '');};

            const rowvalue = document.createElement('div');
            rowvalue.className = 'row_value';

            const weightcontainer = createInputContainer('lbs');
            const repscontainer = createInputContainer('reps');
            const setscontainer = createInputContainer('sets');
            
            rowvalue.appendChild(weightcontainer);
            rowvalue.appendChild(setscontainer);
            rowvalue.appendChild(repscontainer);

            const exerciseList = document.createElement('div');
            exerciseList.className = 'exercise-list';
    
            //used for startup
            workouts[day[1]].forEach(exercise => {
                const exerciseDiv = startup(dayBox, exercise, day[1]);
                exerciseList.appendChild(exerciseDiv);
            });
    
            const addButton = document.createElement('button');
            addButton.type = 'button';
            addButton.textContent = '+';
            addButton.className = 'exercise-button';
            addButton.onclick = async () => {
                const exerciseName = exerciseInput.value;
                const weight = weightcontainer.querySelector('input').value;
                const reps = repscontainer.querySelector('input').value;
                const sets = setscontainer.querySelector('input').value;
    
                const response = await fetch('/add_day', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({action: 'add', day: day[1], exerciseName, weight, reps, sets}),
                });
                const result = await response.json();
    
                if (response.ok) {
                    workouts[day[1]] = result.updated_list[day[1]]; 
                    exerciseList.innerHTML = ''; 
                    workouts[day[1]].forEach(exercise => {
                        const exerciseDiv = startup(dayBox, exercise, day[1]);
                        exerciseList.appendChild(exerciseDiv);
                    });
    
                    exerciseInput.value = '';
                    weightcontainer.querySelector('input').value = '';
                    repscontainer.querySelector('input').value = '';
                    setscontainer.querySelector('input').value = '';
                } else {
                    showErrorModal(result.error);
                }
            };
            
            add_exercise.appendChild(title_day)
            add_exercise.appendChild(exerciseInput);
            add_exercise.appendChild(rowvalue);
            add_exercise.appendChild(addButton);
    
            dayBox.appendChild(dayHeader);
            dayBox.appendChild(dayTitle);
            dayBox.appendChild(exerciseList);
            dayBox.appendChild(add_exercise);
            daysContainer.appendChild(dayBox);
        });
    }
    fetchDays();

    function createInputContainer(unit) {
        const container = document.createElement('div');
        container.className = `input-${unit}`;
        const input = document.createElement('input');
        input.type = 'number';
        input.className = 'input-field';
        input.min = '0.00';
        const unitSpan = document.createElement('span');
        unitSpan.textContent = unit;
        unitSpan.className = 'unit-span';
        container.appendChild(input);
        container.appendChild(unitSpan);
        return container;
    }
    
    let requestQueue = Promise.resolve();
    async function removeExercise(dayBox, exerciseName, day) {
        requestQueue = requestQueue.then(async () => {
            const response = await fetch('/add_day', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({action: 'remove', day, exerciseName}),
            });
            const result = await response.json();

            if (response.ok) {
                workouts[day] = result.updated_list[day];
                const exerciseList = dayBox.querySelector('.exercise-list');
                exerciseList.innerHTML = '';

                workouts[day].forEach(exercise => {
                    const exerciseDiv = startup(dayBox, exercise, day);
                    exerciseList.appendChild(exerciseDiv);
                });
            } else {
                showErrorModal(result.error);
            }
        });
    }

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

        //call a function to delete
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'x';
        deleteButton.className = 'delete-button';
        deleteButton.onclick = () => {
            removeExercise(dayBox, name, day);
        };

        exerciseDiv.appendChild(exerciseTitle);
        exerciseDiv.appendChild(exerciserow);
        exerciseDiv.appendChild(deleteButton);
        return exerciseDiv;
    }

    function showErrorModal(errorMessage) {
        const errorModal = document.getElementById('error-modal');
        const errorMessageElement = document.getElementById('error-message');
        errorMessageElement.innerHTML = errorMessage;
        errorModal.style.display = 'flex';
        const okButton = document.getElementById('error-ok-button');
        okButton.onclick = () => {
            errorModal.style.display = 'none';
        };
    };

    //submission
    addDayButton.addEventListener('click', () => {
        window.location.href = '/';
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.value = '';
        });
    });
    gobackbutton.addEventListener('click', () => {
        window.location.href = '/add_week';
    });
    document.getElementById("logout").addEventListener("click", function() {
        window.location.href = "/logout";
    });
});