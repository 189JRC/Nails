// on page load populate it with appts from api
document.addEventListener('DOMContentLoaded', () => {
    getAppointments("all");
    getAppointments("my");
});

//getAppointments(all) to get all apt items, getAppointments(my) to get user's prebooked appointments
// Lay out the appointments reading them from the api/appointments endpoint

function getAppointments(page) {
    //getAppointments(all) to get all apt items, getAppointments(my) to get user's prebooked appointments
    let endpoint = "";
    let renderFunction = "";

    if (page === "all") {
        //console.log("making fetch call for all appointments")
        endpoint = "/api/appointments/view";
        renderFunction = renderAppointmentsPage
    } else if (page === "my") {
        //console.log("making fetch call for my appointments")
        const customer_id = getId("customer-greeting").getAttribute("data")
        endpoint = `/api/my_appointments/${customer_id}`;
        renderFunction = renderMyAppointments
    }

    fetch(endpoint)
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network error');
            }
            return response.json();
        })
        .then((data) => {
            // Process the appointments data and render it on the page
            renderFunction(data)
        })
        .catch((error) => {
            //console.error('There was a problem fetching appointments data:', error);
        });

}

function create(element) {
    return document.createElement(element)
}

function getId(id) {
    return document.getElementById(id)
}

//Render appointments to DOM for booking page
//Create a new div for each date
//Add a button for each appointment object, with relevant attributes
//Button class indicates its status
function renderAppointmentsPage(data) {
    const aptsHook = getId("appointmentsHook");
    const aptsObject = Object.entries(data);

    for (const [date, aptsArray] of aptsObject) {

        const dateDiv = create("div");
        const hr = create("hr");
        const hr2 = create("hr");

        dateDiv.innerHTML = date;
        dateDiv.prepend(hr2);
        dateDiv.appendChild(hr);
        aptsHook.appendChild(dateDiv);

        for (const [index, aptObj] of Object.entries(aptsArray)) {
            const aptSelectBtn = document.createElement("button");
            if (aptObj.booked === false) {
                aptSelectBtn.setAttribute("class", "newbutton mb-1");
                aptSelectBtn.setAttribute("id", `btn-${aptObj.id}`);
                aptSelectBtn.setAttribute("data-bs-toggle", "modal");
                aptSelectBtn.setAttribute("data-bs-target", "#modal");
                aptSelectBtn.setAttribute(
                    "data-bs-whatever",
                    `${aptObj.time}, ${date}, ${aptObj.id}`
                );
                aptSelectBtn.setAttribute("value", `${aptObj.id}`);
                // Append the button to the dateDiv, not directly to appointmentsHook

            } else if (aptObj.booked === true) {
                aptSelectBtn.setAttribute("class", "newbutton2 mb-1");
            };

            dateDiv.append(aptSelectBtn);
            aptSelectBtn.textContent = `${aptObj.time}`;
        };
    };
};

//Render appointments to DOM for my appointments page
function renderMyAppointments(data) {

    //Booking confirmation message appears on successful booking
    //DO SAME FOR CANCELLATION - USE SAME FUNCTION
    const noAppointmentsMsg = getId("noAppointmentsMsg")
    noAppointmentsMsg.style.display = 'none';

    const myAptsHook = getId("myAptsHook")
    const appointmentsObjectsArray = Object.entries(data);
    const parentElement = getId("myAptsHook");

    while (parentElement.firstChild) {
        parentElement.firstChild.remove();
    }

    for (const [index, aptObj] of appointmentsObjectsArray) {
        const aptDetails = `${aptObj.type} at ${aptObj.formatted_time} on ${aptObj.formatted_date}`;
        const row = create("p");
        row.innerHTML = aptDetails;
        row.style
        const priceTimeRow = create("p");
        priceTimeRow.innerHTML = aptObj.price_time;
        row.append(priceTimeRow);
        const hr = create("hr");
        const br = create("br");
        const br2 = create("br");
        const button = create("button");
        button.setAttribute("class", "newbutton2");
        button.setAttribute("id", "cancelApt");
        button.setAttribute("data", `${aptObj.id}`);
        button.innerHTML = "Request Cancellation";
        //row.append(br);
        //row.append(br2);
        row.append(button);
        row.append(hr);
        myAptsHook.append(row);

        //add functionality to buttons after their creation
        cancellationTrigger();

    }
}

function cancellationTrigger() {
    const cancellationBtns = document.querySelectorAll("#cancelApt");

    cancellationBtns.forEach(btn => {
        btn.addEventListener("click", showCancellationAlert);
    })
}

function showAlert() {
    const customAlert = getId("customAlert");
    const customAlertMessage = getId("customAlertMessage");
    const customAlertButton = getId("customAlertButton");

    customAlertMessage.textContent = "Appointment booked successfully";
    customAlert.style.display = "block";

    customAlertButton.addEventListener("click", hideAlert);

    function hideAlert() {
        customAlert.style.display = "none";
        customAlertButton.removeEventListener("click", hideAlert);
    }
}

function showCancellationAlert(event) {
    event.preventDefault();
    const aptId = event.target.getAttribute("data")
    const customerId = getId("customer-greeting").getAttribute("data")

    const ids = `${aptId}:${customerId}`
    const customAlert = getId("cancellationAlert");
    customAlert.style.display = "block";

    const customAlertMessage = getId("cancellationAlertMessage");
    const problem = getId("cancellationAlertButton");
    problem.setAttribute("data", ids)

    customAlertMessage.textContent = "Are you sure you want to cancel apppointment ?";
    problem.textContent = "Yes please!";


    problem.addEventListener("click", function (event) {
        cancelApt(event);
        customAlert.style.display = "none";
    });

    problem.addEventListener("click", hideAlert);
    function hideAlert() {
        customAlert.style.display = "none";
        problem.removeEventListener("click", hideAlert);
    }

}


//Button triggers for bookings page and my appointments page

document.addEventListener('DOMContentLoaded', () => {
    const bookingsPage = getId("bookings-page");
    const myAptsPage = getId("my-appointments-page");

    bookingsPage.style.display = 'none';
    myAptsPage.style.display = 'block';

    const triggerBookings = getId("trigger-bookings")
    const triggerMyApts = getId("trigger-my-appointments")

    triggerBookings.addEventListener("click", () => {
        bookingsPage.style.display = 'block';
        myAptsPage.style.display = 'none';
    })

    triggerMyApts.addEventListener("click", () => {
        bookingsPage.style.display = 'none';
        getAppointments("my")
        myAptsPage.style.display = 'block';
        //include fetch call to render to DOM
    })
})

// When user selects a vacant appt button - trigger modal window to show form for booking request
// Get relevant data to make the booking: appointment id, customer id
const modal = getId('modal')
modal.addEventListener('show.bs.modal', function (event) {
    //identify appt data from the selected button
    const button = event.relatedTarget;
    //this is a string with format: `${apt.time}, ${apt.dom}, ${apt.id}`
    let dtg = button.getAttribute('data-bs-whatever');
    //get apt id from elsewhere
    const [time, day, date, uid] = dtg.split(', ');
    //#uid is a hidden field initially has no value
    const idDataToSubmit = getId("uid")
    const submitBtnHook = document.querySelector("#submitBtnHook");
    //set title for modal window with dtg
    modal.querySelector("#modalTitle").textContent = `${day}, ${date} ${time}`
    getId("dateStringHolder").setAttribute("data", `${day}, ${date} ${time}`);
    idDataToSubmit.value = uid
    //submitBtnHook.id = uid;
})

//dynamic pricing display for select box
const selectBox = getId('type');
const priceElement = getId('price');

selectBox.addEventListener('change', function () {
    const selectedOption = selectBox.options[selectBox.selectedIndex];
    const price = selectedOption.getAttribute('data-price');
    const time = selectedOption.getAttribute('data-time');

    if (price && time) {
        priceElement.textContent = `Price: ${price}, ${time} hour appointment`;
    } else {
        priceElement.textContent = '';
    }
});

function updateHTMLonSubmission(id, aptDate, aptTime) {

    //Change btn class type on appointments booking page (make it grey)
    let buttonToChange = getId(`btn-${id}`);
    buttonToChange.setAttribute("class", "newbutton2");
    //Switch to my appointments page
    ////trigger render function (with arg specified) to repopulate the page with correct layout
    const bookingsPage = getId("bookings-page");
    const myAptsPage = getId("my-appointments-page");
    bookingsPage.style.display = 'none';
    myAptsPage.style.display = 'block';
    getAppointments("my")
}

function hideModal(appointmentId, data) {
    let modal = getId('modal');
    const aptDate = modal.querySelector("#modalTitle").textContent
    const aptTime = modal.querySelector("#type").value
    let modalInstance = bootstrap.Modal.getInstance(modal); // Get the Bootstrap Modal instance
    // Hide the modal
    if (modalInstance) {
        modalInstance.hide(); // Use the hide() method to hide the modal
    }
    updateHTMLonSubmission(appointmentId, aptDate, aptTime);

}

// On form submission update appointment with customer data // then trigger confirmation window
const form = getId("formHook");

form.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(form);
    const appointmentData = getId('uid');

    var name = getId('name').value;
    var number = getId('number').value;
    var type = getId('type').value;

    if (name === '' || number === '' || type === '0') {
        throw new Error('Please fill in all fields');
    }

    fetch(`api/appointments/${appointmentData.value}/book/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector("#formHook").firstElementChild.value, // Include the CSRF token in the request headers
        },
        body: JSON.stringify(Object.fromEntries(formData)),

    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to update appointment");
            }
            return response.json();
        })
        .then(updatedAppointment => {
            hideModal(appointmentData.value, appointmentData);
            //window.location.reload();
        })
        .catch(error => {
            showAlert
            console.log(error);
        })

    getAppointments("my")
    showAlert()
});

////////////////////////////////////////////////////////////////////
///////////cncellation - my appts

function updateHTMLOnCancellation(event) {
    const val = event.target.getAttribute("data")
    const value = val.split(":")[0]
    document.querySelector("#bookings-page").style.display = 'block';
    const element = document.querySelector(`[data="${value}"]`);
    const aptButton = getId(`btn-${value}`)
    aptButton.setAttribute("class", "newbutton")
    document.querySelector("#bookings-page").style.display = 'none';
    element.parentElement.remove()
    element.remove()
    if (getId("myAptsHook").childElementCount === 0) {
        getId("noAppointmentsMsg").style.display = 'block';
    }
}

function cancelApt(event) {
    event.preventDefault();
    stringIds = event.target.getAttribute("data")
    const [aptId, customerId] = stringIds.split(":").map(Number);

    const payload = {
        customer_id: customerId,
        appointment_id: aptId
    };

    const url = `api/appointments/${aptId}/cancel`;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': event.target.nextElementSibling.value, // Include the CSRF token in the request headers
        },
        body: JSON.stringify(payload),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })

    updateHTMLOnCancellation(event)
}
