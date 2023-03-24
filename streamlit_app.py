import streamlit as sl
import pandas as pd

sl.title('My Parents New Healthy Diner')
   
sl.header('Breakfast Favorites')

sl.text('🥣 Omega 3 and Oatmeal')
sl.text('🥗 kale and Spinach Smoothie')
sl.text('🐔 Hard Boiled Free-Range Eggs')
sl.text('🥑🍞 Avocado Toast')
              
sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
