import streamlit as st
import pandas as pd
from PIL import Image

# Load Excel
excel_file = "Heliana's Recipes.xlsx"
xlsx = pd.ExcelFile(excel_file)

# Load sheets
essences_df = pd.read_excel(xlsx, sheet_name="Essence")
harvest_df = pd.read_excel(xlsx, sheet_name="Harvest Table")
recipes_df = pd.read_excel(xlsx, sheet_name="Recipes")

# --- UI ---
st.set_page_config(page_title="Heliana's Crafting Explorer", layout="wide")

# Load Heliana image
heliana_image = Image.open(".streamlit/heliana_logo.png")

# Display as splash / logo
st.image(heliana_image, width=150)
st.title("Heliana's Crafting Explorer")

# --- Essence Table ---
st.header("Essence Table")
st.dataframe(essences_df, use_container_width=True)

st.markdown("---")

# --- Sidebar search + Reset Filters ---
if "search_text" not in st.session_state:
    st.session_state.search_text = ""
if "creature_type" not in st.session_state:
    st.session_state.creature_type = "(Any)"
if "show_harvest" not in st.session_state:
    st.session_state.show_harvest = False
if "clear_triggered" not in st.session_state:
    st.session_state.clear_triggered = False

# Reset button callback
def reset_and_clear():
    st.session_state.search_text = ""
    st.session_state.creature_type = "(Any)"
    st.session_state.show_harvest = False  # <-- safe here
    st.session_state.clear_triggered = True

# --- Sidebar UI ---
with st.sidebar:
    show_harvest = st.checkbox("Show Harvest Table", key="show_harvest")

    search_text = st.text_input(
        "Search Magic Item Name (partial match)", key="search_text"
    )

    creature_types = ["(Any)"] + sorted(recipes_df["Creature Type"].dropna().unique().tolist())
    creature_type = st.selectbox(
        "Filter by Creature Type (optional)",
        creature_types,
        index=creature_types.index(st.session_state.creature_type),
        key="creature_type"
    )

    st.button("🔄 Reset Filters", on_click=reset_and_clear)

# --- Display Results ---

if st.session_state.clear_triggered:
    st.session_state.clear_triggered = False
    st.subheader("🏰 All Magic Items")
    st.dataframe(recipes_df, use_container_width=True)

elif st.session_state.show_harvest:
    # Show Harvest Table
    st.subheader("🦖 Harvest Table")
    harvest_filtered = harvest_df.copy()
    if creature_type != "(Any)":
        harvest_filtered = harvest_filtered[harvest_filtered["Creature Type"].str.contains(creature_type, case=False, na=False)]
        st.subheader(f"🦖 Harvest Table for '{creature_type}'")
    st.dataframe(harvest_filtered, use_container_width=True)

else:
    # Show Magic Items mode
    if search_text.strip() != "":
        st.subheader(f"🏰 Magic Items matching '{search_text}'")

        recipes_filtered = recipes_df[recipes_df["Name"].str.contains(search_text, case=False, na=False)]

        if creature_type != "(Any)":
            recipes_filtered = recipes_filtered[recipes_filtered["Creature Type"].str.contains(creature_type, case=False, na=False)]

        if not recipes_filtered.empty:
            st.dataframe(recipes_filtered, use_container_width=True)
        else:
            st.info("No matching Magic Items found.")

    elif creature_type != "(Any)":
        st.subheader(f"🏰 Magic Items using '{creature_type}' Parts")
        recipes_filtered = recipes_df[recipes_df["Creature Type"].str.contains(creature_type, case=False, na=False)]
        st.dataframe(recipes_filtered, use_container_width=True)

    else:
        st.subheader("🏰 All Magic Items")
        st.dataframe(recipes_df, use_container_width=True)

# Footer
st.markdown("---")
