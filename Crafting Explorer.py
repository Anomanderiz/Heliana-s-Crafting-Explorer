import streamlit as st
import pandas as pd
from PIL import Image

# --- Constants ---
EXCEL_FILE = "Heliana's Recipes.xlsx"

# --- Data Loading with Caching ---
@st.cache_data
def load_data(excel_path):
    """
    Loads data from the specified Excel file.
    Using st.cache_data ensures this expensive operation runs only once.
    """
    try:
        xlsx = pd.ExcelFile(excel_path)
        essences_df = pd.read_excel(xlsx, sheet_name="Essence")
        harvest_df = pd.read_excel(xlsx, sheet_name="Harvest Table")
        recipes_df = pd.read_excel(xlsx, sheet_name="Recipes")
        return essences_df, harvest_df, recipes_df
    except FileNotFoundError:
        st.error(f"Fatal Error: The data file '{excel_path}' was not found. Please ensure it is in the correct directory.")
        return None, None, None

# Load dataframes
essences_df, harvest_df, recipes_df = load_data(EXCEL_FILE)

# Exit gracefully if data loading failed
if essences_df is None:
    st.stop()

# --- UI Configuration ---
st.set_page_config(page_title="Heliana's Crafting Explorer", layout="wide")

# --- Session State Initialization ---
# Initialize session state keys in one block for clarity if they don't exist.
if "search_text" not in st.session_state:
    st.session_state.search_text = ""
if "creature_type" not in st.session_state:
    st.session_state.creature_type = "(Any)"
if "show_harvest" not in st.session_state:
    st.session_state.show_harvest = False

# --- Sidebar ---
with st.sidebar:
    try:
        heliana_image = Image.open(".streamlit/heliana_logo.png")
        st.image(heliana_image, width=150)
    except FileNotFoundError:
        st.warning("Logo image not found.")

    st.title("Filters")
    
    # Callback to reset filter inputs
    def reset_filters():
        st.session_state.search_text = ""
        st.session_state.creature_type = "(Any)"
        # Note: Resetting show_harvest is optional. You might want it to persist.
        # st.session_state.show_harvest = False

    st.checkbox("Show Harvest Table", key="show_harvest")

    st.text_input(
        "Search Magic Item Name",
        key="search_text",
        placeholder="e.g., Flame Tongue",
    )

    creature_types = ["(Any)"] + sorted(recipes_df["Creature Type"].dropna().unique().tolist())
    st.selectbox(
        "Filter by Creature Type",
        creature_types,
        key="creature_type"
    )

    st.button("🔄 Reset Filters", on_click=reset_filters, use_container_width=True)

# --- Main Page Display ---
st.title("Heliana's Crafting Explorer")

st.header("Essence Table")
st.dataframe(essences_df, use_container_width=True, hide_index=True)
st.markdown("---")

# Determine which primary table to show
if st.session_state.show_harvest:
    # --- Display Harvest Table ---
    title = "🦖 Harvest Table"
    filtered_df = harvest_df.copy()

    # Apply creature type filter if selected
    if st.session_state.creature_type != "(Any)":
        creature_filter = st.session_state.creature_type
        filtered_df = filtered_df[filtered_df["Creature Type"].str.contains(creature_filter, case=False, na=False)]
        title += f" for '{creature_filter}'"

    st.header(title)
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

else:
    # --- Display Magic Items (Recipes) Table ---
    title_parts = ["🏰 All Magic Items"]
    filtered_df = recipes_df.copy()

    # Sequentially apply filters
    if st.session_state.search_text:
        search_term = st.session_state.search_text.strip()
        filtered_df = filtered_df[filtered_df["Name"].str.contains(search_term, case=False, na=False)]
        title_parts = [f"🏰 Magic Items matching '{search_term}'"] # Override default title

    if st.session_state.creature_type != "(Any)":
        creature_filter = st.session_state.creature_type
        filtered_df = filtered_df[filtered_df["Creature Type"].str.contains(creature_filter, case=False, na=False)]
        # Append to the title if it wasn't already overridden by a search
        if not st.session_state.search_text:
             title_parts = [f"🏰 Magic Items using '{creature_filter}' Parts"]

    st.header(" ".join(title_parts))

    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
        st.info("No matching magic items found for the selected criteria.")

# --- Footer ---
st.markdown("---")

