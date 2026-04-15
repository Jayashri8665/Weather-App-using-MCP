import streamlit as st
import asyncio
from fastmcp import Client

# Async function to call MCP
async def fetch_weather(city):
    async with Client("wttrserver.py") as client:
        result = await client.call_tool(
            "get_weather",
            {"city": city}
        )
        return result

# Wrapper to run async in Streamlit
def get_weather(city):
    return asyncio.run(fetch_weather(city))

# Streamlit UI
st.set_page_config(page_title="Weather MCP App", page_icon="🌦️")

st.title("🌦️ Weather App using MCP")
st.write("Get real-time weather using your MCP tool")

# Input
city = st.text_input("Enter City Name", "London")

# Button
if st.button("Get Weather"):
    with st.spinner("Fetching weather..."):
        try:
            result = get_weather(city)

            st.success("Weather fetched successfully!")

            # ✅ Extract clean data
            data = result.structured_content

            # ✅ Display nicely
            st.subheader("🌤️ Weather Details")

            col1, col2, col3 = st.columns(3)

            col1.metric("🌡️ Temp (°C)", data['temperature_C'])
            col2.metric("💧 Humidity", data['humidity'])
            col3.metric("☀️ Weather", data['weather'])

            st.write(f"📍 City: {data['city']}")

        except Exception as e:
            st.error(f"Error: {e}")