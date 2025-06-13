# Import required packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# App Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Establish Snowflake connection and session
cnx = st.connection("snowflake")
session = get_active_session()

# Load fruit options from Snowflake
fruit_df = session.table("smoothis.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in fruit_df.collect()]

# Input: Name of the smoothie
smoothie_name = st.text_input("Name your smoothie")
if smoothie_name:
    st.write("The name of your smoothie will be:", smoothie_name)

# Multi-select for ingredients (max 5)
selected_fruits = st.multiselect(
    "Choose up to 5 ingredients",
    fruit_list,
    max_selections=5
)

# Order Submission Section
if selected_fruits and smoothie_name:
    ingredients_string = ', '.join(selected_fruits)

    insert_query = f"""
        INSERT INTO smoothis.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{smoothie_name}')
    """

    st.code(insert_query, language="sql")

    if st.button("Submit Order"):
        session.sql(insert_query).collect()
        st.success("Your Smoothie is ordered! 🥤", icon="✅")

elif not smoothie_name and selected_fruits:
    st.warning("Please enter a name for your smoothie.")
