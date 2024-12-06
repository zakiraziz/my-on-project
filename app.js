document.getElementById("searchButton").addEventListener("click", async () => {
  const city = document.getElementById("cityInput").value.trim();
  const weatherDisplay = document.getElementById("weatherDisplay");
  const loadingSpinner = document.getElementById("loadingSpinner");

  if (!city) {
    alert("Please enter a city name!");
    return;
  }

  // Show the loading spinner while fetching data
  weatherDisplay.innerHTML = "";
  loadingSpinner.style.display = "block";

  try {
    const response = await fetch(`/weather?city=${encodeURIComponent(city)}`);

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    const data = await response.json();

    // Hide the loading spinner
    loadingSpinner.style.display = "none";

    if (data.error) {
      weatherDisplay.innerHTML = `<p>${data.error}</p>`;
    } else {
      const { name, main, weather } = data;
      weatherDisplay.innerHTML = `
        <h2>Weather in ${name}</h2>
        <p><strong>Temperature:</strong> ${main.temp}°C</p>
        <p><strong>Condition:</strong> ${weather[0].description}</p>
        <p><strong>Humidity:</strong> ${main.humidity}%</p>
      `;
    }
  } catch (error) {
    // Hide the loading spinner
    loadingSpinner.style.display = "none";

    console.error("Error fetching weather data:", error);
    weatherDisplay.innerHTML = `
      <p>Sorry, there was an error fetching the weather data. Please try again later.</p>
    `;
  }
});
