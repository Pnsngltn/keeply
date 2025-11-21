document.addEventListener("DOMContentLoaded", () => {
  const startInput = document.getElementById("time_start");
  const endInput = document.getElementById("time_end");
  const durationSelect = document.getElementById("duration");
  const periodDisplay = document.getElementById("period-display");
  const previewTableBody = document.querySelector("#preview-table tbody");

  const timeToMinutes = (t) => {
    const [h, m] = t.split(":").map(Number);
    return h * 60 + m;
  };

  const minutesToTime = (minutes) => {
    const h = Math.floor(minutes / 60) % 24;
    const m = minutes % 60;
    return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}`;
  };

  const updateInterval = () => {
    const start = startInput.value;
    const end = endInput.value;

    if (!start || !end) {
      periodDisplay.textContent = "-";
      durationSelect.disabled = true;
      previewTableBody.innerHTML = "";
      return;
    }

    let startMin = timeToMinutes(start);
    let endMin = timeToMinutes(end);

    // Handle wrap-around (e.g., end < start means next day)
    if (endMin <= startMin) endMin += 24 * 60;

    const totalMinutes = endMin - startMin;
    const totalHours = totalMinutes / 60;

    // Update period display
    periodDisplay.textContent = `${totalHours.toFixed(2)} hours (${totalMinutes} minutes)`;
    if (totalHours > 8) periodDisplay.style.color = "red";
    else if (totalHours > 4) periodDisplay.style.color = "orange";
    else periodDisplay.style.color = "green";

    // Populate duration select
    durationSelect.disabled = false;
    durationSelect.innerHTML = `<option value="">Select valid duration</option>`;
    const validDurations = [];
    for (let d = 5; d <= totalMinutes; d += 5) {
      if (totalMinutes % d === 0) validDurations.push(d);
    }

    if (validDurations.length === 0) {
      durationSelect.disabled = true;
      const opt = document.createElement("option");
      opt.textContent = "No valid durations";
      opt.disabled = true;
      durationSelect.appendChild(opt);
      previewTableBody.innerHTML = "";
      return;
    }

    validDurations.forEach((d) => {
      const opt = document.createElement("option");
      opt.value = d;
      opt.textContent = `${d} minutes`;
      durationSelect.appendChild(opt);
    });

    // Update preview table with first valid duration
    if (validDurations.length > 0) updatePreview(validDurations[0], startMin, totalMinutes);
  };

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

  // Update preview when duration changes
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
});
