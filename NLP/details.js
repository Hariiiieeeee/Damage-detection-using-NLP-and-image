document.getElementById('get-location').addEventListener('click', function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            document.getElementById('incident-location').value = `Latitude: ${lat}, Longitude: ${lon}`;
        }, function(error) {
            alert('Unable to retrieve your location due to ' + error.message);
        });
    } else {
        alert('Geolocation is not supported by this browser.');
    }
});

document.getElementById('accident-caused-by').addEventListener('change', function() {
    const thirdPartyDetails = document.getElementById('third-party-details');
    const firDocument = document.getElementById('fir-document');
    if (this.value === 'driver') {
        thirdPartyDetails.style.display = 'block';
        document.getElementById('third-party-name').required = true;
        document.getElementById('third-party-contact').required = true;
        firDocument.required = true;
    } else {
        thirdPartyDetails.style.display = 'none';
        document.getElementById('third-party-name').required = false;
        document.getElementById('third-party-contact').required = false;
        firDocument.required = false;
    }
});

document.getElementById('claim-form').addEventListener('submit', function(event) {
    event.preventDefault(); 
    window.location.href = 'cam.html';
});