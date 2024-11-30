document.addEventListener("DOMContentLoaded", () => {
    const addDayButton = document.getElementById("add_day_button");
    const showDaydiv = document.querySelector(".day-list");
    const daySelect = document.getElementById("day-select");
    const dayTitle = document.getElementById("title");
    const form = document.getElementById("create_routine");

    let routineData = workout_days; 

    //this waits for the input and does not allow users to do anything here
    dayTitle.addEventListener("input", () => {
        dayTitle.value = dayTitle.value.replace(/[^a-zA-Z ()-]/g, '');
    });

    const renderDayCard = (day, title) => {
        const dayCard = document.createElement("li");
        dayCard.className = "day-card";
        dayCard.innerHTML = `
            <h3>${day}</h3>
            <p>${title}</p>
            <button type="button" class="delete-day-button">x</button>
        `;
        dayCard.querySelector(".delete-day-button").addEventListener("click", () => {
            removeDay(day);
        });
        showDaydiv.appendChild(dayCard);
    };//end render card

    
    const removeDay = async (day) => {
        const response = await fetch('/add_week', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: 'remove', day}),
        });
        const result = await response.json()
        if(response.ok){
            routineData = result.updated_list;
            showDaydiv.innerHTML = "";
            routineData.forEach(({day, title}) => renderDayCard(day, title));
        }else{
            showErrorModal(result.error);
        }
    }

    const addDay = async () => {
        //(check if on the server if they have duplicates)
        const day = daySelect.value;
        const title = dayTitle.value;
        if (!day || !title.trim()) {
            alert("Please select a day and enter a title.");
            return;
        }
        const response = await fetch('/add_week', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({action: 'add', day, title}),
        });
        const result = await response.json();

        if(response.ok){
            routineData = result.updated_list;
            showDaydiv.innerHTML = "";
            routineData.forEach(({day, title}) => renderDayCard(day, title));
            
            dayTitle.value = "";
            daySelect.innerHTML = `
                <option value="" disabled selected>Choose a Day</option>
                <option value="Monday">Monday</option>
                <option value="Tuesday">Tuesday</option>
                <option value="Wednesday">Wednesday</option>
                <option value="Thursday">Thursday</option>
                <option value="Friday">Friday</option>
                <option value="Saturday">Saturday</option>
                <option value="Sunday">Sunday</option>
            `;
        }else{
            showErrorModal(result.error);
        }
    };//end of day
    addDayButton.addEventListener("click", addDay);

    //on startup
    const startup = () => {
        if (routineData.length > 0) {
            routineData.forEach(({day, title}) => {
                renderDayCard(day, title);
            });
        }
    };
    startup();

    //this does not submit the data when enter is pressed
    document.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            const activeElement = document.activeElement;
            if (activeElement === daySelect || activeElement === dayTitle) {
                e.preventDefault();
                addDay();
            }
        }
    });

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

    //moves to the next page
    form.addEventListener("click", () => {
        window.location.href = '/add_day';
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.value = '';
        });
    });
    document.getElementById("logout").addEventListener("click", function() {
        window.location.href = "/logout";
    });
});//end of the dom

