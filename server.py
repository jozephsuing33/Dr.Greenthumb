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

# 4. Control Board + Plant Selection Menu
DEFAULT_SUPPLIES = [
    {"name": "Potting Soil", "status": "Supplies"},
    {"name": "Tomato Fertilizer", "status": "Low"},
    {"name": "Watering Wand", "status": "Replace"},
    {"name": "Mulch Bags", "status": "Supplies"},
    {"name": "Seed Starter Mix", "status": "Low"},
]

if "supplies" not in st.session_state:
    st.session_state.supplies = list(DEFAULT_SUPPLIES)

SUPPLY_STATUSES = ["Low", "Replace", "Supplies"]

with st.sidebar:
    st.header("🎛️ Control Board")
    st.caption("Track what is Low / Replace / Supplies")

    new_supply = st.text_input("Add a supply", placeholder="e.g. Compost")
    new_status = st.selectbox("Status", SUPPLY_STATUSES, index=2)
    if st.button("➕ Add to Control Board") and new_supply.strip():
        st.session_state.supplies.append(
            {"name": new_supply.strip(), "status": new_status}
        )
        st.rerun()

    st.divider()
    st.subheader("Update status")
    for i, item in enumerate(st.session_state.supplies):
        updated = st.selectbox(
            item["name"],
            SUPPLY_STATUSES,
            index=SUPPLY_STATUSES.index(item["status"]),
            key=f"supply_status_{i}",
        )
        if updated != item["status"]:
            st.session_state.supplies[i]["status"] = updated

    if st.button("♻️ Reset Supplies"):
        st.session_state.supplies = list(DEFAULT_SUPPLIES)
        st.rerun()

    st.divider()
    st.header("Seed Packet")
    plant_choice = st.radio(
        "Select a crop:",
        ["🍅 Tomato", "🥕 Carrot", "🌻 Sunflower", "🥬 Kale", "🫑 Pepper"]
    )
    if st.button("🗑️ Clear Garden"):
        st.session_state.garden_inventory = []
        st.rerun()

# 5. Control Board overview on the main page
st.subheader("🎛️ Control Board — Low / Replace / Supplies")
low_col, replace_col, supplies_col = st.columns(3)

with low_col:
    st.markdown("### 🔴 Low")
    low_items = [s for s in st.session_state.supplies if s["status"] == "Low"]
    if low_items:
        for s in low_items:
            st.write(f"• {s['name']}")
    else:
        st.caption("Nothing low right now")

with replace_col:
    st.markdown("### 🟠 Replace")
    replace_items = [s for s in st.session_state.supplies if s["status"] == "Replace"]
    if replace_items:
        for s in replace_items:
            st.write(f"• {s['name']}")
    else:
        st.caption("Nothing to replace")

with supplies_col:
    st.markdown("### 🟢 Supplies")
    ok_items = [s for s in st.session_state.supplies if s["status"] == "Supplies"]
    if ok_items:
        for s in ok_items:
            st.write(f"• {s['name']}")
    else:
        st.caption("No items in stock")

st.divider()

# 6. The Interactive Photo
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

# 7. Show what you've planted
if st.session_state.garden_inventory:
    st.divider()
    st.subheader("📋 Your Planted Rows")
    cols = st.columns(3)
    for idx, item in enumerate(st.session_state.garden_inventory):
        cols[idx % 3].write(f"**{item['name']}** at {item['x']}, {item['y']}")
