from datetime import datetime

import python_weather
import asyncio

from src.ExtensionBase import ExtensionBase


class WeatherExtension(ExtensionBase):

    def matches(self, query: str) -> bool:
        ans = self.llm.start_conversation(
            f"Is this query: ```{query}``` asking about weather or related things like should "
            f"i wear a jacket or not that can be answerd by using weather channel.\ "
            f"just return true or false not anything else", False)
        # check ans[0] is true or false case-insensitive
        return ans[0].lower() == 'true'

    def process(self, query: str) -> str:
        location = \
            self.llm.start_conversation(f"From this query: ```{query}``` extract the location just return location "
                                        f"nothing else", False)[0]
        # get the current time in this format "2024-05-01"
        time_str = datetime.now().strftime("%Y-%m-%d")
        time = self.llm.start_conversation(f"You are a date extractor, From this query: ```{query}``` return the date, "
                                           f"base on current time of {time_str} in this format `yyyy-mm-dd` "
                                           f" *only return the result nothing else* "
                                           , False)[0]

        a = asyncio.run(get_weather(location, time))
        return f"the user asked {query}, answer him base on this data `{a}`"


async def get_weather(location, date_str):
    # Create a new client
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # Fetch the weather for the location
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        weather = await client.get(location)
        for daily in weather:
            if daily.date == target_date:
                return {'high': f"{daily.highest_temperature}°F",
                        'low': f"{daily.lowest_temperature}°F",
                        "sun_light": f"{daily.sunlight} Hours", 'rain': f"{daily.snowfall} Inch",
                        'location': location}

        return f"No weather data found for {date_str} in {location}"
        # Check if the requested date is in the forecast
