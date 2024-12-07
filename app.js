document.getElementById("searchButton").addEventListener("click", fetchWeatherByCity);
document.getElementById("useCurrentLocation").addEventListener("click", fetchWeatherByLocation);
document.getElementById("voiceSearch").addEventListener("click", startVoiceSearch);

const weatherDisplay = document.getElementById("weatherDisplay");
const loadingSpinner = document.getElementById("loadingSpinner");

// Fetch weather by city
async function fetchWeatherByCity() {
  const city = document.getElementById("cityInput").value.trim();

  if (!city) {
    alert("Please enter a city name!");
    return;
  }

  await fetchWeather(`/weather?city=${encodeURIComponent(city)}`);
}

// Fetch weather by geolocation
async function fetchWeatherByLocation() {
  if (!navigator.geolocation) {
    alert("Geolocation is not supported by your browser.");
    return;
  }

  navigator.geolocation.getCurrentPosition(async (position) => {
    const { latitude, longitude } = position.coords;
    await fetchWeather(`/weather?lat=${latitude}&lon=${longitude}`);
  });
}

// Fetch and display weather
async function fetchWeather(url) {
  weatherDisplay.innerHTML = "";
  loadingSpinner.style.display = "block";

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

    const data = await response.json();
    loadingSpinner.style.display = "none";

    if (data.error) {
      weatherDisplay.innerHTML = `<p>${data.error}</p>`;
    } else {
      displayWeather(data);
    }
  } catch (error) {
    loadingSpinner.style.display = "none";
    console.error("Error fetching weather data:", error);
    weatherDisplay.innerHTML = `<p>Error fetching weather data. Please try again later.</p>`;
  }
}

// Display weather data
function displayWeather(data) {
  const { name, main, weather, sys } = data;
  const iconUrl = `http://openweathermap.org/img/wn/${weather[0].icon}@2x.png`;
  const sunrise = new Date(sys.sunrise * 1000).toLocaleTimeString();
  const sunset = new Date(sys.sunset * 1000).toLocaleTimeString();

  weatherDisplay.innerHTML = `
    <h2>Weather in ${name}</h2>
    <img src="${iconUrl}" alt="${weather[0].description}" />
    <p><strong>Temperature:</strong> ${main.temp}°C</p>
    <p><strong>Condition:</strong> ${weather[0].description}</p>
    <p><strong>Humidity:</strong> ${main.humidity}%</p>
    <p><strong>Sunrise:</strong> ${sunrise}</p>
    <p><strong>Sunset:</strong> ${sunset}</p>
  `;

  updateBackground(weather[0].description);
}

// Update background based on weather condition
function updateBackground(condition) {
  const body = document.body;
  if (condition.includes("rain")) {
    body.style.background = "url('rainy.jpg') no-repeat center center/cover";
  } else if (condition.includes("clear")) {
    body.style.background = "url('sunny.jpg') no-repeat center center/cover";
  } else if (condition.includes("cloud")) {
    body.style.background = "url('cloudy.jpg') no-repeat center center/cover";
  } else {
    body.style.background = "linear-gradient(to bottom, #87CEEB, #ffffff)";
  }
}

// Voice search
function startVoiceSearch() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.start();

  recognition.onresult = (event) => {
    const city = event.results[0][0].transcript;
    document.getElementById("cityInput").value = city;
    fetchWeatherByCity();
  };

  recognition.onerror = (event) => {
    alert("Voice recognition error: " + event.error);
  };
}
document.getElementById("searchButton").addEventListener("click", async () => {
  const city = document.getElementById("cityInput").value.trim();
  const weatherDisplay = document.getElementById("weatherDisplay");
  const loadingSpinner = document.getElementById("loadingSpinner");

  if (!city) {
    alert("Please enter a city name!");
    return;
  }

  weatherDisplay.innerHTML = "";
  loadingSpinner.style.display = "block";

  try {
    const response = await fetch(`/weather?city=${encodeURIComponent(city)}`);
    const data = await response.json();
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
    loadingSpinner.style.display = "none";
    weatherDisplay.innerHTML = `<p>Unable to fetch weather data. Please try again.</p>`;
    console.error("Error:", error);
  }
});
