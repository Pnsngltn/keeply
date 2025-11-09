// Handle appointment status updates
async function updateAppointmentStatus(appointmentId, newStatus) {
    try {
        const response = await fetch('/api/appointment/status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                appointment_id: appointmentId,
                status: newStatus
            })
        });
        
        if (response.ok) {
            // Reload page to refresh appointment lists
            window.location.reload();
        } else {
            alert('Failed to update appointment status');
        }
    } catch (error) {
        console.error('Error updating appointment:', error);
        alert('Error updating appointment status');
    }
}

// Event handler setup
document.addEventListener('DOMContentLoaded', function() {
    // Handle confirm button clicks
    document.querySelectorAll('.btn-confirm').forEach(button => {
        button.addEventListener('click', () => {
            updateAppointmentStatus(button.dataset.appointmentId, 'confirmed');
        });
    });

    // Handle cancel button clicks
    document.querySelectorAll('.btn-cancel').forEach(button => {
        button.addEventListener('click', () => {
            if (confirm('Are you sure you want to cancel this appointment?')) {
                updateAppointmentStatus(button.dataset.appointmentId, 'cancelled');
            }
        });
    });

    // Handle finish button clicks
    document.querySelectorAll('.btn-finish').forEach(button => {
        button.addEventListener('click', () => {
            updateAppointmentStatus(button.dataset.appointmentId, 'finished');
        });
    });
});