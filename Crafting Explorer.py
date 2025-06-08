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
st.title("\ud83c\udf1f Heliana's Crafting Explorer")

# --- Essence Table ---
st.header("Essence Table")
st.dataframe(essences_df, use_container_width=True)

st.markdown("---")

# --- Sidebar search + Reset Filters ---
if "search_text" not in st.session_state:
    st.session_state.search_text = ""
if "creature_type" not in st.session_state:
    st.session_state.creature_type = "(Any)"
if "clear_results" not in st.session_state:
    st.session_state.clear_results = False

def reset_filters():
    st.session_state.search_text = ""
    st.session_state.creature_type = "(Any)"

def clear_results():
    st.session_state.clear_results = True

st.sidebar.header("Search Options")
st.sidebar.button("Reset Filters", on_click=reset_filters)
st.sidebar.button("Clear Results", on_click=clear_results)

# --- Search fields ---
st.session_state.search_text = st.sidebar.text_input(
    "Search Magic Item Name (partial match)", st.session_state.search_text
)

creature_types = ["(Any)"] + sorted(recipes_df["Creature Type"].dropna().unique().tolist())
st.session_state.creature_type = st.sidebar.selectbox(
    "Filter by Creature Type (optional)", creature_types, index=creature_types.index(st.session_state.creature_type)
)

search_text = st.session_state.search_text
creature_type = st.session_state.creature_type

# --- Display Results ---
if st.session_state.clear_results:
    st.session_state.clear_results = False
    st.info("Results cleared. Enter new search criteria.")

elif search_text.strip() != "":
    st.subheader(f"\ud83c\udff0 Magic Items matching '{search_text}'")

    # Filter recipes by Name
    recipes_filtered = recipes_df[recipes_df["Name"].str.contains(search_text, case=False, na=False)]

    # Further filter by Creature Type if selected
    if creature_type != "(Any)":
        recipes_filtered = recipes_filtered[recipes_filtered["Creature Type"].str.contains(creature_type, case=False, na=False)]

    # Show Recipes
    if not recipes_filtered.empty:
        with st.expander("Show Magic Item Recipes", expanded=True):
            st.dataframe(recipes_filtered, use_container_width=True)

        # Show components needed
        components_needed = recipes_filtered["Component"].dropna().unique().tolist()

        st.subheader("Monsters that provide required Components")
        with st.expander("Show Harvest Table Results", expanded=True):
            harvest_filtered = harvest_df[harvest_df["Component"].isin(components_needed)]

            if creature_type != "(Any)":
                harvest_filtered = harvest_filtered[harvest_filtered["Creature Type"].str.contains(creature_type, case=False, na=False)]

            st.dataframe(harvest_filtered, use_container_width=True)
    else:
        st.info("No matching Magic Items found.")

elif creature_type != "(Any)":
    # If no text but Creature Type selected, show full Harvest + Recipes for that Creature Type
    st.subheader(f"\ud83e\udd96 Harvest Table for '{creature_type}'")
    with st.expander("Show Harvest Table Results", expanded=True):
        harvest_filtered = harvest_df[harvest_df["Creature Type"].str.contains(creature_type, case=False, na=False)]
        st.dataframe(harvest_filtered, use_container_width=True)

    st.subheader(f"\ud83c\udff0 Magic Items using '{creature_type}' Parts")
    with st.expander("Show Magic Item Recipes", expanded=True):
        recipes_filtered = recipes_df[recipes_df["Creature Type"].str.contains(creature_type, case=False, na=False)]
        st.dataframe(recipes_filtered, use_container_width=True)
else:
    st.info("Enter text to search for Magic Items, or select a Creature Type.")

# Footer
st.markdown("---")
st.caption("Built with \ud83d\ude80 by your assistant")
