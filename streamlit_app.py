import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# -----------------------------
# Page Config & Title
# -----------------------------
st.set_page_config(page_title="Smoothie Customizer", page_icon=":cup_with_straw:")
st.title(":cup_with_straw: Customise Your Smoothie!")
st.write("Choose exactly 5 fruits for your custom smoothie!")

# -----------------------------
# Snowflake Session Setup
# -----------------------------
@st.cache_resource
def init_connection():
    return Session.builder.configs({
        'account': 'OLRKCFA-SGB76613',
        'user': 'CHANDANA',
        'password': 'Chandanaresmed@10',  # ❗Password included here (not safe for production)
        'warehouse': 'COMPUTE_WH',
        'database': 'SMOOTHIS',
        'schema': 'PUBLIC'
    }).create()

session = init_connection()

# -----------------------------
# Load Fruit Options
# -----------------------------
fruit_df = session.table("smoothis.public.fruit_options").select(col('FRUIT_NAME'))
fruit_list = [row['FRUIT_NAME'] for row in fruit_df.collect()]

# -----------------------------
# User Input
# -----------------------------
name_on_order = st.text_input("Name on Smoothie:")
ingredients_selected = st.multiselect("Choose up to 5 ingredients", fruit_list, max_selections=5)

# -----------------------------
# Submit Order
# -----------------------------
if ingredients_selected and st.button("Submit Order"):
    if len(ingredients_selected) != 5:
        st.error("Please select exactly 5 ingredients.", icon="❌")
    elif not name_on_order.strip():
        st.error("Please enter your name for the smoothie order.", icon="❌")
    else:
        ingredients_string = ' '.join(ingredients_selected)
        insert_query = f"""
            INSERT INTO smoothis.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(insert_query).collect()
        st.success(f"✅ {name_on_order}'s Smoothie has been ordered!")
