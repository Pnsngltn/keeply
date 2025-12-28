/**
 * >===< This file contains all Javascript functionality for the Availability Page >===<
 *     I use a lot of Arrow functions here. Buddy Copilot showed me an example of code  
 *    using them when i was trying to figure out how to detect conflicts. It also showed 
 *    me how i could use asynchronous functions so that i could await responses from API 
 *         endpoints in the 'background' without freezing the page for the user.
 *     For Javascript, since it was the language i was less familiar with, i needed quite 
 *    a bit o guidance from AI Chat bots. I didn't copy paste anything straight from the 
 *    response and made sure to thouroughly go through the code line by line with the Bot
 *    so i understand whats happening.
 *
 */

document.addEventListener("DOMContentLoaded", () => {
  
    // Get user input 
    const startInput = document.getElementById("time_start");
    const endInput = document.getElementById("time_end");
    const durationSelect = document.getElementById("duration");

    // Get reference to period-display and tbody elements
    const periodDisplay = document.getElementById("period-display"); 
    const previewTableBody = document.querySelector("#preview-table tbody");

    // Declaring a 'time to minutes past midnight' function to help with calculations
    const timeToMinutes = (t) => {
        const [h, m] = t.split(":").map(Number);
        return h * 60 + m;
    };
    
    // Declaring a function to revert back to 'Time'
    const minutesToTime = (minutes) => {
        const h = Math.floor(minutes / 60) % 24;
        const m = minutes % 60;
        return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}`;
    };

    // >===> Update the list of possible time slot intervals <===<
    const updateInterval = () => {
        const start = startInput.value;
        const end = endInput.value;
	
	// Default values if no start time or end time selected
        if (!start || !end) {
            periodDisplay.textContent = "-";
            durationSelect.disabled = true;    // Disable duration dropdown
            previewTableBody.innerHTML = "";    // Nothing to preview
            return;
        } 
	
	// Translate start and end times into minutes past midnight
        let startMin = timeToMinutes(start);
        let endMin = timeToMinutes(end);

    	// Handle wrap-around (e.g., end < start means next day, so we add 24h worth of minutes)
    	if (endMin <= startMin) endMin += 24 * 60;

	// Keeping track of the total working period to be set
    	const totalMinutes = endMin - startMin;
    	const totalHours = totalMinutes / 60;

    	// Update period display (The idea here is just to give a visual representation of how long the shift will be)
    	periodDisplay.textContent = `${totalHours.toFixed(2)} hours (${totalMinutes} minutes)`;
    	if (totalHours > 8) periodDisplay.style.color = "red";    // Period chosen has more than 8h straight. Not healthy!
    	else if (totalHours > 4) periodDisplay.style.color = "orange";    // Rest after this period
    	else periodDisplay.style.color = "green";    // Short period

    	// Populate duration select
    	durationSelect.disabled = false;    // Enable the element
    	durationSelect.innerHTML = `<option value="">Select valid duration</option>`;    // Just a placeholder option
    	const validDurations = [];
	
	// Find valid slot durations in 5 min increments
    	for (let d = 5; d <= totalMinutes; d += 5) {
      	    if (totalMinutes % d === 0) validDurations.push(d);    // If totalMinutes cleanly divides by d than its valid
    	}

	// Handle cases where there are no valid slot durations
    	if (validDurations.length === 0) {
      	    durationSelect.disabled = true;    // Disable dropdown
            const opt = document.createElement("option");    // Just a placeholder disabled option
      	    opt.textContent = "No valid durations";
      	    opt.disabled = true;
      	    durationSelect.appendChild(opt);
      	    previewTableBody.innerHTML = "";    // No preview to be shown
      	    return;
    	}
	
	// Create an option for each valid duration and append it to the dropdown
    	validDurations.forEach((d) => {
      	    const opt = document.createElement("option");
            opt.value = d;
      	    opt.textContent = `${d} minutes`;
      	    durationSelect.appendChild(opt);
    	});

        // Update preview table with smallest valid duration by default
        if (validDurations.length > 0) updatePreview(validDurations[0], startMin, totalMinutes);
    };

    // >===> Update the preview table <===<
    const updatePreview = (duration, startMin, totalMinutes) => {
        previewTableBody.innerHTML = "";
        let current = startMin;
        let count = 1;
        while (current < startMin + totalMinutes) {
            const end = current + duration;
      	    const row = document.createElement("tr");
      	    const startTime = minutesToTime(current);
      	    const endTime = minutesToTime(end);
      	    row.innerHTML = `<td>${count}</td><td>${startTime}</td><td>${endTime}</td>`;
      	    previewTableBody.appendChild(row);
      	    current = end;
      	    count++;
    	}	
    };

    // >===> Update preview when duration changes <===<
    durationSelect.addEventListener("change", () => {
        const duration = parseInt(durationSelect.value);
        const start = startInput.value;
        const end = endInput.value;

        if (!duration || !start || !end) return;

        let startMin = timeToMinutes(start);
        let endMin = timeToMinutes(end);

        if (endMin <= startMin) endMin += 24 * 60;

        const totalMinutes = endMin - startMin;

        updatePreview(duration, startMin, totalMinutes);
    });

    startInput.addEventListener("change", updateInterval);
    endInput.addEventListener("change", updateInterval);

    // >===> Bulk timeslot deletion <===<
    const deleteBtn = document.getElementById("delete-selected-btn");
    const selectAll = document.getElementById("select-all-slots");

    /** Another nice trick Copilot taught me. Guard clauses.
    * Only if selectAll exists (i.e.: is True) will the Event listener be created
    */
    selectAll && selectAll.addEventListener("change", function (e) {
	document.querySelectorAll(".slot-checkbox").forEach(cb => cb.checked = e.target.checked);
    });
	
    deleteBtn && deleteBtn.addEventListener("click", async function () {
        const checks = Array.from(document.querySelectorAll(".slot-checkbox:checked"));
	if (checks.length === 0) { alert("No timeslots selected"); return; } 
	// This gives the user an option to confirm or cancel the delete request. If cancel, just return
	if (!confirm(`Delete ${checks.length} timeslot(s)? This cannot be undone.`)) return;
	const ids = checks.map(c => c.value);

	try {
	    const csrfMeta = document.querySelector("meta[name='csrf-token']");
	    const CSRF_TOKEN = csrfMeta ? csrfMeta.getAttribute("content") : null;

	    /** Here i needed to make a request to the API endpoint. I had to resort to Copilot
	    * for the syntax. 
	    */
	    const res = await fetch("/api/timeslots/delete", {
		method: "POST", 
		headers: {
		    "Content-Type": "application/json",
		    ...(CSRF_TOKEN ? {"X-CSRFToken": CSRF_TOKEN} : {})
		},
		credentials: "same-origin", 
		body: JSON.stringify({ slot_ids: ids})
	    });
	    const json = await res.json();

	    // res keeps the response from 'await'
	    if (!res.ok) {
		alert(json.error || "Failed to delete timeslots");
		return;
	    }

	    // Reload window to reflect changes
	    window.location.reload();
	} catch (err) {    // Catching all errors TODO: Add more specificity to the error messages
	    console.error(err);
   	    alert("Error deleting timeslots");
        }
    });
});
