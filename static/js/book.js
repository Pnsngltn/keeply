const userId = {{ user_id }};
let selectedService = null;
let selectedDate = null;
let selectedSlot = null;

// Step 1: Load services
fetch(`/api/services/${userId}`)
    .then(res => res.json())
    .then(services => {
        const container = document.getElementById("services-container");
        services.forEach(s => {
            const btn = document.createElement("button");
            btn.innerText = `${s.name} - ${s.price}€`;
            btn.onclick = () => selectService(s.id);
            container.appendChild(btn);
        });
    });

function selectService(serviceId) {
    selectedService = serviceId;
    document.getElementById("step-service").style.display = "none";
    loadDates();
}

// Step 2: Load dates
function loadDates() {
    fetch(`/api/dates/${userId}`)
        .then(res => res.json())
        .then(dates => {
            const container = document.getElementById("dates-container");
            container.innerHTML = "";
            dates.forEach(d => {
                const btn = document.createElement("button");
                btn.innerText = d;
                btn.onclick = () => selectDate(d);
                container.appendChild(btn);
            });
            document.getElementById("step-date").style.display = "block";
        });
}

function selectDate(date) {
    selectedDate = date;
    document.getElementById("step-date").style.display = "none";
    loadTimeslots();
}

// Step 3: Load timeslots
function loadTimeslots() {
    fetch(`/api/timeslots/${userId}/${selectedDate}`)
      .then(res => res.json())
      .then(slots => {
          const container = document.getElementById("slots-container");
          container.innerHTML = "";
          slots.forEach(s => {
              const btn = document.createElement("button");
              btn.innerText = `${s.time_start} - ${s.time_end}`;
              btn.onclick = () => selectSlot(s.id);
              container.appendChild(btn);
          });
          document.getElementById("step-time").style.display = "block";
      });
}

function selectSlot(slotId) {
    selectedSlot = slotId;
    document.getElementById("step-time").style.display = "none";
    document.getElementById("step-client").style.display = "block";
}

// Step 4: Submit client info
document.getElementById("client-form").onsubmit = function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const data = {
        user_id: userId,
        service_id: selectedService,
        slot_id: selectedSlot,
        name: formData.get("name"),
        email: formData.get("email"),
        phone: formData.get("phone")
    };
    fetch("/api/book", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(resp => {
        if(resp.success){
            document.getElementById("step-client").style.display = "none";
            document.getElementById("confirmation").style.display = "block";
        }
    });
}
