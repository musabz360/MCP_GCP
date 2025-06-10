def getliveTemp(latitude, longitude):
    """
    Get comprehensive weather data for a given latitude and longitude.
    """
    import requests

    # Define the API endpoint and parameters    
    api_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature", 
            "is_day", "precipitation", "rain", "showers", "snowfall", 
            "weather_code", "cloud_cover", "pressure_msl", "surface_pressure",
            "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m",
            "cape", "freezing_level_height"
        ],
        "hourly": [
            "temperature_2m", "relative_humidity_2m", "dew_point_2m",
            "apparent_temperature", "precipitation_probability",
            "precipitation", "rain", "showers", "snowfall", "snow_depth",
            "weather_code", "cloud_cover", "cloud_cover_low",
            "cloud_cover_mid", "cloud_cover_high", "visibility",
            "evapotranspiration", "wind_speed_10m", "wind_direction_10m",
            "wind_gusts_10m", "uv_index", "uv_index_clear_sky",
            "is_day", "cape", "surface_pressure", "pressure_msl"
        ],
        "daily": [
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "apparent_temperature_max", "apparent_temperature_min",
            "sunrise", "sunset", "daylight_duration", "sunshine_duration",
            "uv_index_max", "uv_index_clear_sky_max",
            "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum",
            "precipitation_hours", "precipitation_probability_max",
            "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant",
            "shortwave_radiation_sum", "et0_fao_evapotranspiration"
        ],
        "timezone": "auto",
        "forecast_days": 7,
        "past_days": 1  # Include yesterday's data
    }

    # Make the API request
    response = requests.get(api_url, params=params)
    
    # Check if request was successful
    if response.status_code != 200:
        print(f"Error: API request failed with status code {response.status_code}")
        return None
      # Parse the JSON response
    data = response.json()
    
    # Format the data into a clean structure
    formatted_data = {
        'current': data['current'],
        'hourly': {},
        'daily': {}
    }
    
    # Format hourly data for today
    current_date = data['hourly']['time'][0].split('T')[0]
    today_hourly = {}
    for i, time in enumerate(data['hourly']['time']):
        if current_date in time:
            hour = time.split('T')[1]
            hour_data = {}
            for key in data['hourly'].keys():
                if key != 'time':
                    hour_data[key] = data['hourly'][key][i]
            today_hourly[hour] = hour_data
    formatted_data['hourly'] = today_hourly
    
    # Format daily data
    daily_forecast = {}
    for i, date in enumerate(data['daily']['time']):
        day_data = {}
        for key in data['daily'].keys():
            if key != 'time':
                day_data[key] = data['daily'][key][i]
        daily_forecast[date] = day_data
    formatted_data['daily'] = daily_forecast
    return formatted_data



