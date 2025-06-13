# Import packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# App Title
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Snowflake session and table query
session = get_active_session()
fruit_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# User input for smoothie order
name_on_order = st.text_input("Name on Smoothie:")
fruit_list = [row['FRUIT_NAME'] for row in fruit_df.collect()]  # Convert Snowpark DataFrame to list
ingredients_selected = st.multiselect(
    "Choose up to 5 ingredients",
    fruit_list,
    max_selections=5
)

# Submit Order Logic
if ingredients_selected:
    ingredients_string = ' '.join(ingredients_selected)
    insert_query = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        if len(ingredients_selected) == 5:
            session.sql(insert_query).collect()
            st.success(f"{name_on_order}'s Smoothie is ordered!", icon="✅")
        else:
            st.error("Add exactly 5 items to the smoothie", icon="❌")
