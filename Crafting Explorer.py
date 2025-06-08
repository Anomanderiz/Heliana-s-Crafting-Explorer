import streamlit as st
import pandas as pd

# Load Excel
excel_file = "Heliana's Recipes.xlsx"
xlsx = pd.ExcelFile(excel_file)

# Load sheets
essences_df = pd.read_excel(xlsx, sheet_name="Essence")
harvest_df = pd.read_excel(xlsx, sheet_name="Harvest Table")
recipes_df = pd.read_excel(xlsx, sheet_name="Recipes")

# --- UI ---
st.set_page_config(page_title="Heliana's Crafting Explorer", layout="wide")
st.title("🌟 Heliana's Crafting Explorer")

# --- Essence Table ---
st.header("Essence Table")
st.dataframe(essences_df, use_container_width=True)

st.markdown("---")

# --- Sidebar search + Reset Filters ---
if "search_text" not in st.session_state:
    st.session_state.search_text = ""
if "creature_type" not in st.session_state:
    st.session_state.creature_type = "(Any)"

# Flag to trigger clearing results
if "clear_triggered" not in st.session_state:
    st.session_state.clear_triggered = False

def reset_and_clear():
    st.session_state.search_text = ""
    st.session_state.creature_type = "(Any)"
    st.session_state.clear_triggered = True

st.sidebar.header("Search Options")
if st.sidebar.button("Reset Filters & Clear Results"):
    reset_and_clear()

# --- Search fields ---
search_text_input = st.sidebar.text_input(
    "Search Magic Item Name (partial match)", value=st.session_state.search_text
)

creature_types = ["(Any)"] + sorted(recipes_df["Creature Type"].dropna().unique().tolist())
creature_type_select = st.sidebar.selectbox(
    "Filter by Creature Type (optional)", creature_types, index=creature_types.index(st.session_state.creature_type)
)

# Update session state with current widget values
st.session_state.search_text = search_text_input
st.session_state.creature_type = creature_type_select

search_text = st.session_state.search_text
creature_type = st.session_state.creature_type

# --- Display Results ---
if st.session_state.clear_triggered:
    st.session_state.clear_triggered = False
    st.info("Results cleared. Enter new search criteria.")

elif search_text.strip() != "":
    st.subheader(f"🏰 Magic Items matching '{search_text}'")

    # Filter recipes by Name
    recipes_filtered = recipes_df[recipes_df["Name"].str.contains(search_text, case=False, na=False)]

    # Further filter by Creature Type if selected
    if creature_type != "(Any)":
        recipes_filtered = recipes_filtered[recipes_filtered["Creature Type"].str.contains(creature_type, case=False, na=False)]

    # Show Recipes
    if not recipes_filtered.empty:
        st.dataframe(recipes_filtered, use_container_width=True)
    else:
        st.info("No matching Magic Items found.")

elif creature_type != "(Any)":
    # If no text but Creature Type selected, show full Harvest + Recipes for that Creature Type
    st.subheader(f"🦖 Harvest Table for '{creature_type}'")
    harvest_filtered = harvest_df[harvest_df["Creature Type"].str.contains(creature_type, case=False, na=False)]
    st.dataframe(harvest_filtered, use_container_width=True)

    st.subheader(f"🏰 Magic Items using '{creature_type}' Parts")
    recipes_filtered = recipes_df[recipes_df["Creature Type"].str.contains(creature_type, case=False, na=False)]
    st.dataframe(recipes_filtered, use_container_width=True)
else:
    st.info("Enter text to search for Magic Items, or select a Creature Type.")

# Footer
st.markdown("---")
st.caption("Built with 🚀 by your assistant")
