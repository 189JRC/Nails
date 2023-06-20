//Delete appointment 
function deleteVacantAppointment(e) {
    e.preventDefault();
    id = e.target.id
    const url = `delete_apt/${id}`
    fetch(url)
        .then(response => {
            if (!response.ok) {
                alert("Error finding path, unable to delete appointment");
            } else {
                // remove post from index page and shift other posts by deleting <br>
                console.log(`Appointment ${id} deleted successfully`)
                window.location.reload();
            }
        });
}

//Deletes past appointment and creates record with earnings data.
function makeRecord(event, id) {
    event.preventDefault();

    const form = document.getElementById("formHook");
    const formData = new FormData(form);
    let uid = document.getElementById("modalTitle").data;

    const url = `/api/create_record/${uid}`
    console.log(uid)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector("#formHook").firstElementChild.value, // Include the CSRF token in the request headers
        },
        body: JSON.stringify(Object.fromEntries(formData)),
    })
        .then(response => {
            if (!response.ok) {
                console.log("Error finding path");
            } else {
                console.log(`Acknowledged ${uid}`)
                window.location.reload();
            }
        });

}

//Allows future, non-booked appointment to be deleted.
function cancelAppointment(event) {
    event.preventDefault();
    let id = document.getElementById("modalTitle").data;
    console.log(id)
    // fetch call to delete appointment
    const url = `delete_apt/${id}`

    fetch(url)
        .then(response => {
            if (!response.ok) {
                alert("Error finding path, unable to delete appointment");
            } else {
                // remove post from index page and shift other posts by deleting <br>
                console.log(`Appointment ${id} deleted successfully`)
                window.location.reload();
            }
        });
}

//Launches modal window for cancellation of future, booked appointment.
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('cancelAppointmentModal');

    modal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Identify appointment data from the selected button
        let timeDateId = button.getAttribute('data-bs-whatever'); // = `${apt.time}, ${apt.dom}, ${apt.id}`
        const uid = timeDateId.split(", ")[2];
        modal.querySelector("#modalTitle").textContent = `Cancel Appointment: ${uid}`; // Set title for the modal window with dtg // give modal the appointment id
        modal.querySelector("#modalTitle").data = uid; // give appointment id to modal window
    });
});

//Launches modal window for acknowledgement of past, booked appointment.
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('acknowledgeModal');

    modal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const uid = button.getAttribute('data-bs-whatever').split(", ")[2];// `${apt.time}, ${apt.dom}, ${apt.id}`
        modal.querySelector("#modalTitle").textContent = `Acknowledge Appointment: ${uid}`;
        const modalTitleElement = document.getElementById('modalTitle');
        modalTitleElement.data = uid;
    });
});

// Populates page with rows for dates. Appends rows with child rows for appointments

function renderDates(data) {
    const appointmentsHook = document.getElementById("appointmentsHook");

    data.forEach(function (item) {
        renderDateElement(item, appointmentsHook);
    });
}

function create(element, ...args) {
    const el = document.createElement(element);
    const [className, innerHTML, ...attributes] = args;

    if (className) {
        el.setAttribute("class", className);
    }

    if (innerHTML) {
        el.innerHTML = innerHTML;
    }

    if (attributes && attributes.length > 0) {
        for (const attribute of attributes) {
            const [attrName, attrValue] = attribute;
            el.setAttribute(attrName, attrValue);
        }
    }

    return el;
}

function renderDateElement(item, appointmentsHook) {
    //Use date to form row for attach appointments to
    const dateDivElement = create("div", "dateDiv", item.date, "id", item.date, "class", "appointment-dates");
    const hr = create("hr");
    const hr2 = create("hr");
    dateDivElement.prepend(hr2);
    dateDivElement.appendChild(hr);
    appointmentsHook.appendChild(dateDivElement);

    //Create row with elements for titles for appointment data
    const appointmentTitleRow = create("div", "row appointment-title-row");
    appointmentTitleRow.append(create("span", "col-3", "<strong>Time</strong>"));//appointmentTitleRow.append(timeHeader)
    appointmentTitleRow.append(create("span", "col-3", "<strong>Type</strong>"));
    appointmentTitleRow.append(create("span", "col-3", "<strong>Customer</strong>"));
    appointmentTitleRow.append(create("span", "col-3", "<strong>Edit</strong>"));
    dateDivElement.append(appointmentTitleRow)
    dateDivElement.append(create("br"))

    //From the list of appointment objects create rows with apt data, append each to title row
    const appointments = item.appointments;
    appointments.forEach(function (appointment) {
        const appointmentDataRow = createAppointmentRow(appointment);
        dateDivElement.append(appointmentDataRow);
    });
}

function createAppointmentRow(appointment) {
    //Create html elements and set default attributes
    const appointmentDataRow = create("row", "row appointment-data-row");
    const timeInfo = create("span", "col-3", appointment.time.slice(0, 5));
    const typeInfo = create("span", "col-3", appointment.type);
    const CustomerNumberInfo = create("span", "col-3");
    const deleteInfo = create("button");

    deleteInfo.id = `${appointment.id}`;
    deleteInfo.setAttribute("data-bs-whatever", `${appointment.time}, ${appointment.dom}, ${appointment.id}`);
    deleteInfo.innerHTML = "&#10006;";
    CustomerNumberInfo.innerHTML = 'None';
    deleteInfo.setAttribute("class", "col-1 btn btn-warning mx-auto");

    //Override default attributes depending on if apt is booked and if apt is in future
    if (appointment.customer) {
        deleteInfo.setAttribute("data-bs-toggle", "modal");
        CustomerNumberInfo.innerHTML = `${appointment.customer.name}, ${appointment.customer.number}`;
        deleteInfo.setAttribute("value", `${appointment.id}`);
    }

    if (appointment.future === false) {
        deleteInfo.innerHTML = "&#10003;";
        deleteInfo.setAttribute("class", "col-1 btn btn-success mx-auto");
        appointmentDataRow.setAttribute("class", "row expired-appointment");
    }

    if (appointment.future === false && !appointment.customer) {
        deleteInfo.addEventListener("click", function (event) {
            deleteVacantAppointment(event);
        });
    }


    if (appointment.future === true && appointment.customer) {
        deleteInfo.setAttribute("data-bs-target", "#cancelAppointmentModal");
    }

    if (appointment.future === false && appointment.customer) {
        deleteInfo.setAttribute("data-bs-target", "#acknowledgeModal");
    }

    if (appointment.future === true && !appointment.customer) {
        deleteInfo.addEventListener("click", function (event) {
            deleteVacantAppointment(event);
        });
    }

    appointmentDataRow.append(timeInfo);
    appointmentDataRow.append(typeInfo);
    appointmentDataRow.append(CustomerNumberInfo);
    appointmentDataRow.append(deleteInfo);

    return appointmentDataRow;
}

//get appointments past and future
const endpoint = "/api/appointments/management"
function getAppointments() {
    fetch(endpoint)
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network Error')
            }
            return response.json();
        })
        .then((data) => {
            renderDates(data);
        })
        .catch((error) => {
            console.error("There was a problem fetching appointments data:", error)
        }
        )
};

document.addEventListener('DOMContentLoaded', getAppointments);
