# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("Name on your Smoothie will be:", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients!', my_dataframe, max_selections=5)
    

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    INGREDIENTS_STRING = ''

    for fruit_chosen in ingredients_list:
        INGREDIENTS_STRING += fruit_chosen + ', '

    st.write(INGREDIENTS_STRING)

    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
                values ('""" + name_on_order + """' , '""" + INGREDIENTS_STRING + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order!')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")
        