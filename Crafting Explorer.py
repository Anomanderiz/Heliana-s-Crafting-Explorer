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
if "reset_triggered" not in st.session_state:
    st.session_state.reset_triggered = False

def reset_filters():
    st.session_state.reset_triggered = True

st.sidebar.header("Search Options")
st.sidebar.button("Reset Filters", on_click=reset_filters)

if st.session_state.reset_triggered:
    search_mode = ""
    st.session_state.reset_triggered = False
else:
    search_mode = st.sidebar.selectbox("Search by:", ["Creature Type", "Component", "Magic Item"])

# --- Display Results ---
if search_mode == "Creature Type":
    creature_types = recipes_df["Creature Type"].dropna().unique().tolist()
    creature_type = st.sidebar.selectbox("Select Creature Type", sorted(creature_types))

    st.subheader(f"🦖 Harvest Table for '{creature_type}'")
    with st.expander("Show Harvest Table Results", expanded=True):
        harvest_filtered = harvest_df[harvest_df["Creature Type"].str.contains(creature_type, case=False, na=False)]

        def highlight_rows(row):
            return ["background-color: #ffeaa7" for _ in row]

        st.dataframe(harvest_filtered.style.apply(highlight_rows, axis=1), use_container_width=True)

    st.subheader(f"🏰 Magic Items using '{creature_type}' Parts")
    with st.expander("Show Magic Item Recipes", expanded=True):
        recipes_filtered = recipes_df[recipes_df["Creature Type"].str.contains(creature_type, case=False, na=False)]

        def highlight_rows(row):
            return ["background-color: #ffeaa7" for _ in row]

        st.dataframe(recipes_filtered.style.apply(highlight_rows, axis=1), use_container_width=True)

elif search_mode == "Component":
    components = pd.concat([
        harvest_df["Component"],
        recipes_df["Component"]
    ]).dropna().unique().tolist()

    component = st.sidebar.selectbox("Select Component", sorted(components))

    st.subheader(f"🦖 Monsters providing '{component}'")
    with st.expander("Show Harvest Table Results", expanded=True):
        harvest_filtered = harvest_df[harvest_df["Component"].str.contains(component, case=False, na=False)]

        def highlight_component(cell):
            if component.lower() in str(cell).lower():
                return "background-color: #ffeaa7"
            return ""

        st.dataframe(harvest_filtered.style.applymap(highlight_component, subset=["Component"]), use_container_width=True)

    st.subheader(f"🏰 Magic Items using '{component}'")
    with st.expander("Show Magic Item Recipes", expanded=True):
        recipes_filtered = recipes_df[recipes_df["Component"].str.contains(component, case=False, na=False)]

        st.dataframe(recipes_filtered.style.applymap(highlight_component, subset=["Component"]), use_container_width=True)

elif search_mode == "Magic Item":
    item_names = recipes_df["Item Name"].dropna().unique().tolist()
    item_name = st.sidebar.selectbox("Select Magic Item", sorted(item_names))

    st.subheader(f"🏰 Recipe for '{item_name}'")
    with st.expander("Show Magic Item Recipe", expanded=True):
        recipe_filtered = recipes_df[recipes_df["Item Name"] == item_name]

        def highlight_rows(row):
            return ["background-color: #ffeaa7" for _ in row]

        st.dataframe(recipe_filtered.style.apply(highlight_rows, axis=1), use_container_width=True)

    components_needed = recipe_filtered["Component"].dropna().unique().tolist()

    st.subheader("Monsters that provide required Components")
    with st.expander("Show Harvest Table Results", expanded=True):
        harvest_filtered = harvest_df[harvest_df["Component"].isin(components_needed)]

        def highlight_component(cell):
            if cell in components_needed:
                return "background-color: #ffeaa7"
            return ""

        st.dataframe(harvest_filtered.style.applymap(highlight_component, subset=["Component"]), use_container_width=True)

# Footer
st.markdown("---")
st.caption("Built with 🚀 by your assistant")
