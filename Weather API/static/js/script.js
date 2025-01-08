if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            document.getElementById("estado").innerText =
                `Ubicación obtenida correctamente. Latitud: ${lat}, Longitud: ${lon}`;

            // Enviar las coordenadas al servidor
            fetch(`http://127.0.0.1:5000/obtener_clima?lat=${lat}&lon=${lon}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    // Manejar la respuesta del servidor
                })
                .catch(error => console.error('Error:', error));
        },
        (error) => {
            document.getElementById("estado").innerText =
                "No se pudo obtener la ubicación. Asegúrate de permitir el acceso.";
            console.error(error);
        }
    );
} else {
    document.getElementById("estado").innerText =
        "Geolocalización no soportada en este navegador.";
}