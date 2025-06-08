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

# --- Search fields ---
if st.session_state.reset_triggered:
    search_text = ""
    creature_type = "(Any)"
    st.session_state.reset_triggered = False
else:
    search_text = st.sidebar.text_input("Search Magic Item Name (partial match)", "")
    creature_types = ["(Any)"] + sorted(recipes_df["Creature Type"].dropna().unique().tolist())
    creature_type = st.sidebar.selectbox("Filter by Creature Type (optional)", creature_types)

# --- Display Results ---
if search_text.strip() != "":
    st.subheader(f"🏰 Magic Items matching '{search_text}'")
    
    # Check if "Name" column exists, if not try "Item Name" 
    name_column = "Name" if "Name" in recipes_df.columns else "Item Name"
    
    # Filter recipes by Name
    recipes_filtered = recipes_df[recipes_df[name_column].str.contains(search_text, case=False, na=False)]
    
    # Further filter by Creature Type if selected
    if creature_type != "(Any)":
        recipes_filtered = recipes_filtered[recipes_filtered["Creature Type"].str.contains(creature_type, case=False, na=False)]
    
    # Show Recipes
    if not recipes_filtered.empty:
        with st.expander("Show Magic Item Recipes", expanded=True):
            st.dataframe(recipes_filtered, use_container_width=True)
        
        # Show components needed
        components_needed = recipes_filtered["Component"].dropna().unique().tolist()
        
        if components_needed:
            st.subheader("Monsters that provide required Components")
            with st.expander("Show Harvest Table Results", expanded=True):
                harvest_filtered = harvest_df[harvest_df["Component"].isin(components_needed)]
                
                if creature_type != "(Any)":
                    harvest_filtered = harvest_filtered[harvest_filtered["Creature Type"].str.contains(creature_type, case=False, na=False)]
                
                if not harvest_filtered.empty:
                    st.dataframe(harvest_filtered, use_container_width=True)
                else:
                    st.info("No monsters found providing the required components.")
    else:
        st.info("No matching Magic Items found.")

elif creature_type != "(Any)":
    # If no text but Creature Type selected, show full Harvest + Recipes for that Creature Type
    st.subheader(f"🦖 Harvest Table for '{creature_type}'")
    with st.expander("Show Harvest Table Results", expanded=True):
        harvest_filtered = harvest_df[harvest_df["Creature Type"].str.contains(creature_type, case=False, na=False)]
        
        if not harvest_filtered.empty:
            st.dataframe(harvest_filtered, use_container_width=True)
        else:
            st.info("No harvest data found for this creature type.")
    
    st.subheader(f"🏰 Magic Items using '{creature_type}' Parts")
    with st.expander("Show Magic Item Recipes", expanded=True):
        recipes_filtered = recipes_df[recipes_df["Creature Type"].str.contains(creature_type, case=False, na=False)]
        
        if not recipes_filtered.empty:
            st.dataframe(recipes_filtered, use_container_width=True)
        else:
            st.info("No recipes found for this creature type.")

else:
    st.info("Enter text to search for Magic Items, or select a Creature Type.")

# Footer
st.markdown("---")
st.caption("Built with 🚀 by your assistant")
