const apiKey = "2c7e9efe37df2463ce611b1d76ad37f1";

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            obtenerClima(lat, lon);
        },
        (error) => {
            document.getElementById("estado").innerText =
                "No se pudo obtener la ubicación. Asegúrate de permitir el acceso a la ubicación.";
        }
    );
} else {
    document.getElementById("estado").innerText =
        "Geolocalización no soportada en este navegador.";
}


function obtenerClima(lat, lon) {
    const url = `https://api.openweathermap.org/data/3.0/onecall?lat=${lat}&lon=${lon}&exclude=minutely,hourly&units=metric&lang=es&appid=${apiKey}`;

    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            document.getElementById("estado").innerText = `Zona: ${data.timezone}`;
            const climaHTML = `
                <p>Temperatura: ${data.current.temp}°C</p>
                <p>Descripción: ${data.current.weather[0].description}</p>
                <p>Humedad: ${data.current.humidity}%</p>
            `;
            document.getElementById("clima").innerHTML = climaHTML;
        })
        .catch((error) => {
            document.getElementById("estado").innerText =
                "Hubo un error al obtener el clima.";
        });
}
