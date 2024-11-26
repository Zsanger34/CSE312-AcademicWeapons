document.addEventListener("DOMContentLoaded", () => {   
    const addDayButton = document.getElementById("add_day_button");
    const showDaydiv = document.querySelector(".day-list");
    const daySelect = document.getElementById("day-select");
    const dayTitle = document.getElementById("title");
    const form = document.querySelector("form.create");

    let routineData = [];

    // Add day functionality
    const addDay = () => {
        if (!daySelect.value || !dayTitle.value.trim()) {

            //display an error message
            alert("Please select a day and enter a title.");
            return;
        }

        const day = daySelect.value;
        const title = dayTitle.value;

        if (routineData.some(d => d.day === day)) {

            //display an error message
            alert("This day is already added.");
            return;
        }

        routineData.push({ day, title });
        const dayCard = document.createElement("li");
        dayCard.className = "day-card";
        dayCard.innerHTML = `
            <h3>${day}</h3>
            <p>${title}</p>
            <button type="button" class="delete-day-button">Delete</button>
        `;

        // Delete Button Functionality
        dayCard.querySelector(".delete-day-button").addEventListener("click", () => {
            showDaydiv.removeChild(dayCard);
            routineData = routineData.filter(d => d.day !== day);
        });

        showDaydiv.appendChild(dayCard);

        // Clear inputs
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
    };
    addDayButton.addEventListener("click", addDay);
    document.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            const activeElement = document.activeElement;
            if (activeElement === daySelect || activeElement === dayTitle) {
                e.preventDefault();
                addDay();
            }
        }
    });

    // Async function to send routineData to the backend
    const submitRoutine = async () => {
        const response = await fetch('/add_week', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(routineData),
        });

        const data = await response.json();

        if (response.ok) {
            console.log('we ar good')
        }
        // Reset form and clear routineData
        form.reset();
        showDaydiv.innerHTML = "";
        routineData = [];
    };
    
    //submit and reset form
    form.addEventListener("submit", (e) => {
        e.preventDefault(); 
        submitRoutine();
    });
});
