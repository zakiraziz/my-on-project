document.getElementById("searchButton").addEventListener("click", () => {
    const city = document.getElementById("cityInput").value;
    if (!city) {
      alert("Please enter a city name!");
      return;
    }
  
    fetch(`/weather?city=${city}`)
      .then((response) => response.json())
      .then((data) => {
        const weatherDisplay = document.getElementById("weatherDisplay");
        if (data.error) {
          weatherDisplay.innerHTML = `<p>${data.error}</p>`;
        } else {
          const { name, main, weather } = data;
          weatherDisplay.innerHTML = `
            <h2>Weather in ${name}</h2>
            <p>Temperature: ${main.temp}°C</p>
            <p>Condition: ${weather[0].description}</p>
            <p>Humidity: ${main.humidity}%</p>
          `;
        }
      })
      .catch((error) => {
        console.error("Error fetching weather data:", error);
      });
  });
  