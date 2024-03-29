#https://n3eta-first-streamlit-app-streamlit-app-reon2f.streamlit.app/
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
   
streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 and Oatmeal')
streamlit.text('🥗 kale and Spinach Smoothie')
streamlit.text('🐔 Hard Boiled Free-Range Eggs')
streamlit.text('🥑🍞 Avocado Toast')
              
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#create a function
def get_fruityvice_data(fruit_choice_from_function):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice_from_function)
     #take the json version of the response and normalize it
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     #output it in the screen as a table
     return fruityvice_normalized


#section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("select a fruit to get info")
   else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)

except URLError as e:
      streamlit.error()
      
streamlit.write('You have entered ', fruit_choice)


streamlit.header("View Our Fruit List - Add Your Favorites")

#get the list of fruits from snowflake table
def get_fruit_load_list():
   my_cur = my_cnx.cursor()
   my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
   return my_cur.fetchall()
   
if streamlit.button('Get Fruit Load List'):   
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)
   
   
#insert fruit enetred by user into snowflake table
def insert_row_snowflake(new_fruit):
   my_cur = my_cnx.cursor()
   my_cur.execute("insert into FRUIT_LOAD_LIST values ('" + new_fruit +"')")
   return "Thanks for adding " + new_fruit
   

your_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to your List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function = insert_row_snowflake(your_fruit)
      my_cnx.close()
      streamlit.text(back_from_function)

#don't run anything past this
#streamlit.stop()  

