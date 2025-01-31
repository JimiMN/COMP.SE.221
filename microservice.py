from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# OpenWeatherMap API endpoint and key
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = "your_openweathermap_api_key"  # Replace with your actual API key

@app.get("/weather/{city_name}")
async def get_weather(city_name: str):
    """Fetch weather data for a given city"""
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric',  # Returns temperature in Celsius
        'lang': 'en',       # Language of the weather description
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(WEATHER_API_URL, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"HTTP error: {exc.response.text}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error while fetching weather data: {str(exc)}")
        
        weather_data = response.json()

        # Check if the response is successful
        if weather_data.get("cod") != 200:
            raise HTTPException(status_code=400, detail="City not found or invalid data")
        
        # Extract the required weather information
        main_weather = weather_data.get("weather", [{}])[0].get("description", "No description available")
        temperature = weather_data.get("main", {}).get("temp", "No temperature data")
        humidity = weather_data.get("main", {}).get("humidity", "No humidity data")

        # Return a structured response
        return {
            "city": city_name,
            "temperature": f"{temperature} °C",
            "weather": main_weather.capitalize(),
            "humidity": f"{humidity} %",
        }
