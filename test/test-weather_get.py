from datetime import datetime

import python_weather
import asyncio


async def get_weather(location, date_str):
    # Create a new client
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # Fetch the weather for the location
        weather = await client.get(location)
        for daily in weather:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if daily.date == target_date:
                return {'condition': weather.description, 'temperature': f"{weather.temperature}°F",
                        'precipitation': weather.precipitation, 'wind': weather.wind_speed,
                        "UV": weather.ultraviolet, 'humidity': weather.humidity, 'location': location}
            else:
                return f"No weather data found for {date_str} in {location}"
        # Check if the requested date is in the forecast


# Example usage
if __name__ == "__main__":
    location = "Mashhad"
    date_str = "2024-10-03"

    # Run the async function
    print(asyncio.run(get_weather(location, date_str)))
