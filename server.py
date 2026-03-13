import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

# 1. Page Configuration
st.set_page_config(page_title="Dr. Greenthumb", page_icon="🌱")

# 2. EMERGENCY RESET (In case you get stuck on 'undefined')
if st.sidebar.button("Reset to Home"):
    st.query_params.clear()
    st.rerun()

st.title("🌱 Dr. Greenthumb Garden Mapper")
st.write("Click on a row in your photo to 'plant' a crop!")

# 3. Create a Plant Menu
plant_choice = st.selectbox("What are you planting today?", 
                            ["🍅 Tomato", "🥕 Carrot", "🌻 Sunflower", "🥬 Kale", "🫑 Pepper"])

# 4. Memory: This keeps track of where you clicked
if "garden_inventory" not in st.session_state:
    st.session_state.garden_inventory = []

# 5. The Interactive Map
# IMPORTANT: Make sure you have an image file named 'garden.jpg' in your GitHub folder
# If your image has a different name, change 'garden.jpg' below to match it.
try:
    coords = streamlit_image_coordinates("garden.jpg", key="garden_map")

    if coords:
        # Save the click location and the plant type
        new_plant = {"x": coords["x"], "y": coords["y"], "name": plant_choice}
        st.session_state.garden_inventory.append(new_plant)
        st.success(f"Planted {plant_choice}!")

except FileNotFoundError:
    st.error("Missing Photo! Please upload a file named 'garden.jpg' to your GitHub.")

# 6. Show your list of planted rows
if st.session_state.garden_inventory:
    st.divider()
    st.subheader("Your Garden Layout")
    for item in st.session_state.garden_inventory:
        st.write(f"✅ {item['name']} at coordinates: {item['x']}, {item['y']}")

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import PIL.Image

# 1. Professional Layout
st.set_page_config(page_title="Dr. Greenthumb Planner", layout="wide")

# 2. Emergency Reset (in case you get stuck)
if st.sidebar.button("Reset App"):
    st.query_params.clear()
    st.rerun()

st.title("🌱 Dr. Greenthumb: Interactive Garden Planner")
st.write("Click your photo below to 'plant' your selected crop.")

# 3. Memory for your plants
if "garden_inventory" not in st.session_state:
    st.session_state.garden_inventory = []

# 4. Plant Selection Menu
with st.sidebar:
    st.header("Seed Packet")
    plant_choice = st.radio(
        "Select a crop:",
        ["🍅 Tomato", "🥕 Carrot", "🌻 Sunflower", "🥬 Kale", "🫑 Pepper"]
    )
    if st.button("🗑️ Clear Garden"):
        st.session_state.garden_inventory = []
        st.rerun()

# 5. The Interactive Photo
try:
    # This looks for your garden photo
    img = PIL.Image.open("garden.jpg")
    coords = streamlit_image_coordinates(img, key="garden_map")

    if coords:
        # Save the location when you click
        new_plant = {"x": coords["x"], "y": coords["y"], "name": plant_choice}
        st.session_state.garden_inventory.append(new_plant)
        st.toast(f"Planted {plant_choice}!")

except FileNotFoundError:
    st.error("⚠️ Photo Missing! Please upload your photo to GitHub and name it 'garden.jpg'.")

# 6. Show what you've planted
if st.session_state.garden_inventory:
    st.divider()
    st.subheader("📋 Your Planted Rows")
    cols = st.columns(3)
    for idx, item in enumerate(st.session_state.garden_inventory):
        cols[idx % 3].write(f"**{item['name']}** at {item['x']}, {item['y']}")
