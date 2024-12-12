""""
Name: Daniil Brudnyy
Class: CS230-4
Data: Nuclear Explosions
Link:
"""

import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
import pandas as pd
from PIL import Image
#Import necessary packages

file_path = "C:\\Users\\conta\\Downloads\\nuclear_explosions.csv" #update for program use on different device
df_nuclear = pd.read_csv(file_path) #reads data file and creates dataframe

page = st.tabs(["Home", "Data", "Statistical Data Values", "Data Properties", "Country Charts", "More Charts and PivotTable", "Map"]) #Creates tabs for different information
with page[0] :
    #Home page
    st.title("Home")
    st.write("Welcome to an analysis of nuclear explosions in the world.")
    st.write("By Daniil Brudnyy")
    #Uploads downloaded image(see attached submission for image) and change path for different user
    image_file = Image.open("C:\\Users\\conta\\Downloads\\nuclear_blast.jpg")
    #Sets image size and caption
    st.image(image_file, width = 850, caption = "Nuclear Blast Mushroom Cloud")
with page[1] :
    #Page with dataframe
    st.title("Data")
    st.write("This is a table of nuclear explosions in the world.")
    st.write(df_nuclear)
with page[2] :
    #Statistical values of dataframe including count, mean, and value ranges
    st.title("Table of Statistical Values for Data")
    st.write("This is a table of the values from the nuclear explosions in the world.")
    #Uses .describe() to create a table of statistical data
    st.write(df_nuclear.describe())
with page[3] :
    st.title("Data Properties")
    selected_prop = st.radio("Please select the category of a data property you would like to view", ["", "Unique Warhead Names", "Deployment by Country", "Deployment by Year"])
    if selected_prop == "Unique Warhead Names" :
        # Removes any empty data values
        data = df_nuclear["Data.Name"].dropna()
        # [DA1] uses lambda to remove any names that are not given, defined as Nan in the data
        clean_data = data.apply(lambda x: x if x != "Nan" else None)
        clean_data = clean_data.dropna()
        #Write the names
        st.write(clean_data)
        #[PY5] write unique values into a dictionary
        clean_dict = {}
        for name in clean_data :
            if name not in clean_dict.values() :
                clean_dict[name] = name
        # [ST1] Allow user to check if the weapon exists or not with text input
        search_name = st.text_input("Please enter the name of a warhead").lower()
        #Filters data to check if warhead was deployed by name, allows for lowercase values
        if search_name.title() in clean_dict :
            st.write(f"{search_name} was deployed")
        else :
            st.write(f"{search_name} was not deployed. Please check your spelling or enter a different warhead name")
    elif selected_prop == "Deployment by Country" :
        selected_type = st.radio("Please select what you would like to view", ["", "Number of Warheads Each Country Deployed", "Country With Most Deployments", "Country With Least Deployments"])
        if selected_type == "Number of Warheads Each Country Deployed" :
            # [PY4] List comprehension to get list of countries that deployed warheads
            countries = [country for country in set(df_nuclear["WEAPON SOURCE COUNTRY"])]
            # [ST2] Streamlit widget for a dropdown selection
            country = st.selectbox("Please select a country", countries)
            # Gets the specified country from value_counts using .get
            st.write(f"{country} deployed {df_nuclear["WEAPON SOURCE COUNTRY"].value_counts().get(country, 0)} nuclear warheads")
        elif selected_type == "Country With Most Deployments" :
            # [DA9] Adds a new column to the dataframe by grouping the countries and getting the number of occurrences of each country
            df_nuclear["Country.Count"] = df_nuclear.groupby("WEAPON SOURCE COUNTRY")["WEAPON SOURCE COUNTRY"].transform("count")
            # [DA3] Gets the largest(maximum) value of the new dataframe column to get the highest number of warheads deployed by a country
            max_country_deployments = df_nuclear["Country.Count"].max()
            # Uses a filter to determine the country that deployed the most warheads
            max_country = df_nuclear.loc[df_nuclear["Country.Count"] == max_country_deployments, "WEAPON SOURCE COUNTRY"].iloc[0]
            # Writes the country that deployed the most warheads along with the amount of warheads it deployed
            st.write(f"{max_country} deployed the most nuclear warheads with {max_country_deployments} warheads deployed")
        elif selected_type == "Country With Least Deployments" :
            # Also adds a new column to dataframe
            df_nuclear["Country.Count"] = df_nuclear.groupby("WEAPON SOURCE COUNTRY")["WEAPON SOURCE COUNTRY"].transform("count")
            # Gets smallest (minimum) value from column
            min_country_deployments = df_nuclear["Country.Count"].min()
            # Also uses filter to determine country with the least amount of deployments
            min_country = df_nuclear.loc[df_nuclear["Country.Count"] == min_country_deployments, "WEAPON SOURCE COUNTRY"].iloc[0]
            # Writes country that deployed the least amount of warheads
            st.write(f"{min_country} deployed the least nuclear warheads with {min_country_deployments} warheads deployed")
    elif selected_prop == "Deployment by Year" :
        # Gets the earliest and latest year of nuclear deployments from dataframe
        min_year = df_nuclear["Date.Year"].min()
        max_year = df_nuclear["Date.Year"].max()
        # [ST3] Streamlit slider widget to select the year
        selected_year = st.slider("Please select the year you would like to view deployment data for", min_year, max_year)
        # Uses .get to get the amount of times a value (selected_year) occurred in a dataframe column
        year_deployment_n = df_nuclear["Date.Year"].value_counts().get(selected_year, 0)
        # Writes how many warheads were deployed in the selected year
        st.write(f"{year_deployment_n} nuclear warheads were deployed in {selected_year}")
with page[4] :
    st.title("Country Charts")
    selected_chart = st.radio("Please select the type of chart you would like to view", ["", "Pie Chart", "Bar Chart"])
    if selected_chart == "Pie Chart" :
        st.write("This is a pie chart of nuclear explosions in the world.")
        df_nuclear_countries = df_nuclear["WEAPON SOURCE COUNTRY"].value_counts()
        ax1 = plt.subplot()
        df_nuclear_countries.plot(kind="pie", autopct = "%.1f%%", startangle = 90)
        ax1.set_title("Pie Chart of Number of Explosions by Country")
        st.pyplot()
    elif selected_chart == "Bar Chart" :
        st.write("This is a bar chart of nuclear explosions in the world.")
        df_nuclear_countries = df_nuclear["WEAPON SOURCE COUNTRY"].value_counts()
        ax1 = plt.subplot()
        df_nuclear_countries.plot(kind="bar", ax = ax1, color = "red")
        ax1.set_xlabel("Country")
        ax1.set_ylabel("Number of Explosions")
        ax1.set_title("Bar Chart of Number of Explosions by Country")
        st.pyplot()
with page[5] :
    st.title("More Charts and PivotTable")
    selected_chart = st.radio("Please select the chart you would like to view", ["", "Line Chart of Years", "Bar Graph of Warhead Deployment Types", "PivotTable"])
    if selected_chart == "Line Chart of Years" :
        st.write("This is a line chart of the years of nuclear explosions in the world.")
        df_nuclear_years = df_nuclear["Date.Year"].value_counts().sort_index(ascending = True)
        ax1 = plt.subplot()
        df_nuclear_years.plot(kind="line", ax = ax1, color = "purple")
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Number of Explosions")
        ax1.set_title("Line Chart of Number of Explosions by Year")
        st.pyplot()
    elif selected_chart == "Bar Graph of Warhead Deployment Types" :
        st.write("A bar graph of the warhead deployment types of nuclear explosions in the world.")
        df_nuclear_warhead_deployment_types = df_nuclear["Data.Type"].value_counts()
        ax1 = plt.subplot()
        df_nuclear_warhead_deployment_types.plot(kind="bar", ax = ax1, color = "green")
        ax1.set_xlabel("Warhead Deployment Type")
        ax1.set_ylabel("Number of Explosions")
        ax1.set_title("Bar Graph of Number of Explosions by Warhead Deployment Type")
        st.pyplot()
    elif selected_chart == "PivotTable" :
        st.write("A PivotTable of nuclear warhead detonation locations by country.")
        df_nuclear_warhead_deployment_types = df_nuclear.pivot_table(index = "Data.Type", columns = "WEAPON SOURCE COUNTRY", values = "Date.Year", aggfunc = "count")
        st.write(df_nuclear_warhead_deployment_types)
with page[6] :
    st.title("Nuclear Explosions")
    st.write("This is a map of nuclear explosions in the world.")
    st.write("Select a map from the sidebar to view a map of nuclear explosions")
    df_nuclear.rename(columns={"Location.Cordinates.Latitude": "latitude", "Location.Cordinates.Longitude": "longitude"}, inplace=True)
    selected_map = st.radio("Please select the map of explosions you would like to view", ["", "Simple", "Scatter", "Custom Icon"])
    if selected_map == "Simple":
        st.title('Simple Map')
        # Basic map with nuclear explosion data
        st.map(df_nuclear)

    elif selected_map == "Scatter":
        st.title("Scatterplot Map")

        # Create a view of the map
        view_state = pdk.ViewState(
            latitude=df_nuclear["latitude"].mean(),
            longitude=df_nuclear["longitude"].mean(),
            zoom=3,
            pitch=0
        )

        # Create a scatterplot layer
        scatter_layer = pdk.Layer(
            type = "ScatterplotLayer",
            data = df_nuclear,
            get_position = "[longitude, latitude]",
            get_radius = 50000,
            get_color = [255, 0, 0],
            pickable = True
        )

        # Tooltip to display relevant information
        tool_tip = {
            "html": "Explosion Name:<br/><b>{Data.Name}</b><br/>Country: <b>{WEAPON SOURCE COUNTRY}</b>",
            "style": {
                "backgroundColor": "black",
                "color": "white"
            }
        }

        # Create the map
        scatter_map = pdk.Deck(
            map_style = "mapbox://styles/mapbox/outdoors-v12" ,
            initial_view_state = view_state,
            layers = [scatter_layer],
            tooltip = tool_tip
        )

        st.pydeck_chart(scatter_map)

    elif selected_map == "Custom Icon" :
        st.title("Icon Map")

        ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/2/2d/Nuclear_ico.png"

        df_nuclear["Date"] = df_nuclear["Date.Month"].astype(str) + "/" + df_nuclear["Date.Day"].astype(str) + "/" + df_nuclear["Date.Year"].astype(str)


        icon_data = {
            "url": ICON_URL,
            "width": 25,
            "height": 25,
            "anchorY": 1
        }

        df_nuclear["icon_data"] = None
        for i in df_nuclear.index :
            df_nuclear.at[i, "icon_data"] = icon_data

        icon_layer = pdk.Layer(
            type="IconLayer",
            data=df_nuclear,
            get_icon="icon_data",
            get_position='[longitude, latitude]',
            get_size=50,
            pickable=True
        )

        view_state = pdk.ViewState(
            latitude=df_nuclear["latitude"].mean(),
            longitude=df_nuclear["longitude"].mean(),
            zoom=3,
            pitch=0
        )

        tool_tip = {
            "html": "<b>Explosion Name:</b> {Data.Name}<br/><b> Country: </b>{WEAPON SOURCE COUNTRY}<br/> <b>Date:</b> {Date}",
            "style": {
                "backgroundColor": "blue",
                "color": "white"
            }
        }

        icon_map = pdk.Deck(
            map_style='mapbox://styles/mapbox/navigation-day-v1',
            layers=[icon_layer],
            initial_view_state=view_state,
            tooltip=tool_tip
        )

        st.pydeck_chart(icon_map)




"https://upload.wikimedia.org/wikipedia/commons/c/c3/Nuclear_Explosion.svg"