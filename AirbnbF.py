import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from bson.decimal128 import Decimal128
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import json
from collections import Counter
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(page_title="Airbnb Data Analytics",
    page_icon=":house:",
    layout="wide")

# Title and description
st.title('Airbnb Data Analytics and Visuvalization for Trends and Insights')

with open('D:/Guvi_Data_Science/MDT33/Capstone_Project/Airbnb_Project_Orientation_Recordings/sample_airbnb.json', 'r') as file:
    data = json.load(file)

Airbnb_data = []

for i in data:
    Airbnb_data.append({
        'ID': i['_id'],
        'Name': i['name'],
        'Description': i['description'],
        'Country': i['address']['country'],
        'Country_code': i['address']['country_code'],
        'Longitude': i['address']['location']['coordinates'][0],
        'Latitude': i['address']['location']['coordinates'][1],
        'Price': i['price'],
        'Cleaning Fees': i.get('cleaning_fee', 0),
        'Security_deposit': i.get('security_deposit'),
        'Amenities': i['amenities'],
        'Property_Type': i['property_type'],
        'Room_Type': i['room_type'],
        'Bed_type': i['bed_type'],
        'Accomodates': i['accommodates'],
        'Bedroom Count': i.get('bedrooms', 0),
        'Total Beds': i.get('beds', 0),
        'House_rules': i.get('house_rules'),
        'Listing URL': i['listing_url'],
        'Availability_365': i['availability']['availability_365'],
        'Availability_90': i['availability']['availability_90'],
        'Availability_60': i['availability']['availability_60'],
        'Availability_30': i['availability']['availability_30'],
        'Minimum_Nights': i['minimum_nights'],
        'Maximum_Nights': i['maximum_nights'],
        'Cancellation_policy': i['cancellation_policy'],
        'Host ID': i['host']['host_id'],
        'Host Name': i['host']['host_name'],
        'Host Location': i['host']['host_location'],       
        'Number of Reviews': i['number_of_reviews'],
        'Neighbourhood':i['host']['host_neighbourhood'],
        'Review_count': i['review_scores'].get('review_scores_rating'),
        'Review_score': i['review_scores'].get('review_scores_value')
    })

adf = pd.DataFrame(Airbnb_data)
duplicate_rows = adf[adf.duplicated(subset=['ID'])]  
adf.reset_index(drop=True,inplace=True)

# Convert 'Price' column to float
adf['Price'] = adf['Price'].astype(str).astype(float)

# Convert 'Security_deposit' column to float, handling NaN values
adf['Security_deposit'] = adf['Security_deposit'][~adf['Security_deposit'].isna()].astype(str).astype(float)

# Convert 'Cleaning_fee' column to float, handling NaN values
adf['Cleaning Fees'] = adf['Cleaning Fees'][~adf['Cleaning Fees'].isna()].astype(str).astype(float)

# Convert 'Review_scores' column to nullable integers
adf['Review_score'] = adf['Review_score'].astype('Int64')

# Fill missing values in 'Total_bedrooms' with the mode
adf['Bedroom Count'] = adf['Bedroom Count'].fillna(adf['Bedroom Count'].mode()[0])

# Fill missing values in 'Total_beds' with the median due to outliers
adf['Total Beds'] = adf['Total Beds'].fillna(adf['Total Beds'].median())

# Fill missing values in 'Security_deposit' with the median
adf['Security_deposit'] = adf['Security_deposit'].fillna(adf['Security_deposit'].median())

# Fill missing values in 'Cleaning_fee' with the median
adf['Cleaning Fees'] = adf['Cleaning Fees'].fillna(adf['Cleaning Fees'].median())

# Fill missing values in 'Review_scores' with the median
adf['Review_score'] = adf['Review_score'].fillna(adf['Review_score'].median())

# Fill missing values in 'Review_scores' with the median
adf['Review_count'] = adf['Review_count'].fillna(adf['Review_count'].median())

# Filling Empty values in Description and House rules columns
adf['Description'] = adf['Description'].replace(to_replace='',value='No Description Provided')
adf['House_rules'] = adf['House_rules'].replace(to_replace='',value='No House rules Provided')
adf['Amenities'] = adf['Amenities'].replace(to_replace='',value='Not Available')

csv_file_path = 'Airbnb_D1.csv'
adf.to_csv(csv_file_path, index=False)

choropleth_data = adf[['Country', 'Latitude', 'Longitude']]
choropleth_data = choropleth_data.copy()
choropleth_data.dropna(subset=['Country', 'Latitude', 'Longitude'], inplace=True)
property_counts = choropleth_data['Country'].value_counts().reset_index(name='Count')
property_counts.columns = ['Country', 'Count']

with st.sidebar:
    
    image_path = "C:/Users/Admin/Downloads/ABNB-4aaade0f.png"
    image_path1="C:/Users/Admin/Pictures/Screenshots/Power BI-Airbnb.png"
    image_path2="C:/Users/Admin/Pictures/Screenshots/2.png"
    pdf_path="D:/Guvi_Data_Science/MDT33/Capstone_Project/Airbnb_Project_Orientation_Recordings/Airbnb_Power BI.pdf"
    # Display the image
    st.image(image_path, use_column_width=True)
    st.download_button(label="Download data as csv",
                        data=open(csv_file_path, 'rb').read(),
                        file_name='Airbnb_D1.csv',
                        mime='text/csv')
    # Add a download button for PDF file
    pdf_data = open(pdf_path, 'rb').read()
    st.download_button(label="Download PowerBI pdf report",
                   data=pdf_data,
                   file_name='Airbnb_Power_BI_1.pdf',
                   mime='application/pdf')

    selected=option_menu(menu_title="Airbnb  Analytics",
                    options=["ANALYSIS","INSIGHTS"],
                    default_index=0,
                    menu_icon='cast',
                    orientation = 'vertical')
    st.image(image_path1, use_column_width=True)
    st.image(image_path2, use_column_width=True)
    
fig = px.scatter_geo(property_counts, 
                     locations="Country",
                    hover_name="Country", 
                    locationmode='country names',
                    projection="equirectangular",
                    title="AIRBNB ACROSS THE WORLD",
                    size="Count",  # Size markers by count of properties
                    labels={'Count': 'Number of Properties'})

# Customize the layout
fig.update_layout(
    title={
        'text': "AIRBNB ACROSS THE WORLD",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 24,
            'color': 'Yellow'
        }
    },
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="lightgreen",
        landcolor="black",
        projection_type="natural earth",
        bgcolor='black'),
    plot_bgcolor='lightgrey',  # Set the background color of the plotting area
    paper_bgcolor='black',  # Set the background color of the entire canvas
    margin={"r":0,"t":40,"l":0,"b":0})

# Customize marker properties
fig.update_traces(marker=dict(
        line=dict(width=1, color='DarkSlateGrey'),
        symbol='diamond',
        sizemode='area',
        color='lightblue'),
    selector=dict(mode='markers'))

st.plotly_chart(fig,use_container_width=True)

if selected == "ANALYSIS":   
    
    tab1, tab2 = st.tabs(["Room Type Analysis", "Price Analysis"])

    with tab1:
    
        col1,col2,col3=st.columns(3)
        with col1:
                selected_country = st.selectbox('Select Country', adf['Country'].unique())
        with col2:
                selected_PROPERTY_TYPE = st.selectbox('Select Property Type', adf['Property_Type'].unique())
        with col3:            
            selected_availability= st.selectbox('Number of days',["30","60","90","365"])
        
        filtered_df = adf[
                (adf['Country'] == selected_country) &
            (adf['Property_Type'] == selected_PROPERTY_TYPE) &
            ((adf['Availability_30'] >= int(selected_availability)) |
            (adf['Availability_60'] >= int(selected_availability)) |
            (adf['Availability_90'] >= int(selected_availability)) |
            (adf['Availability_365'] >= int(selected_availability)))]
        
        # Select specific columns
        selected_columns = ['Name', 'Property_Type', 'Room_Type', 'Price', 'Cleaning Fees', 'Security_deposit', 
                        'Bedroom Count', 'Total Beds','Cancellation_policy','Review_score', 'Neighbourhood', 'Number of Reviews']
        result_df = filtered_df[selected_columns]

        def plot_price_distribution(df):
        # Aggregate data by Room Type
            aggregated_data = df.groupby('Room_Type')['Price'].mean().reset_index()
            fig = px.bar(aggregated_data, x='Room_Type', y='Price', title='Average Price Distribution by Property_Type', 
                         text='Price' )
            fig.update_traces(
            textposition='outside',  # Positions the labels outside the bars
            texttemplate='%{text:.2f}'  # Format the labels to show 2 decimal places
            )
            st.plotly_chart(fig)

        def plot_room_type_pie_chart(df):
            room_type_counts = df['Room_Type'].value_counts().reset_index()
            room_type_counts.columns = ['Room_Type', 'Count']
            fig = px.pie(room_type_counts, names='Room_Type', values='Count', 
                    title='Proportion of Properties by Room Type', hole=0.3)
            st.plotly_chart(fig)

        def count_amenities(df, amenities_list):
            amenities_count = {amenity: 0 for amenity in amenities_list}
            for index, row in df.iterrows():
                for amenity in amenities_list:
                    if amenity in row['Amenities']:
                        amenities_count[amenity] += 1
            return amenities_count


        def plot_Review(df):
        # Aggregate data by Room Type
            aggregated_data = df.groupby('Room_Type')['Review_score'].mean().reset_index()
            fig = px.line(aggregated_data, x='Room_Type', y='Review_score', title='Average Review_score Distribution by Room_Type', 
                         text='Review_score', markers=True)
            fig.update_traces(
            textposition='top center',  # Positions the labels outside the bars
            texttemplate='%{text:.2f}'  # Format the labels to show 2 decimal places
            )
            st.plotly_chart(fig)

        with st.expander("Filtered Dataframe"):
            st.dataframe(result_df)

        col1,col2 = st.columns(2)

        with col1:
            plot_room_type_pie_chart(result_df)
        with col2:    
            plot_price_distribution(result_df)
        plot_Review(result_df)

    with tab2:
    
        col1,col2,col3,col4,col5=st.columns(5)
        
        with col1:
            selected_country = st.selectbox('Select Country', adf['Country'].unique(),key="Select Country2")
        
        with col2:
            selected_PROPERTY_TYPE = st.selectbox('Select Property Type', adf['Property_Type'].unique(),key="Select Property Type1")
        
        with col3:            
            selected_availability= st.selectbox('Number of days',["30","60","90","365"],key='Number of days1')
        
        with col4:            
            selected_Room_Type= st.selectbox('Select Room Type', adf['Room_Type'].unique())
        
        with col5: 
            selected_Amenities = st.multiselect('Select Amenities',('24-hour check-in', 'TV', 'Air conditioning', 'Beach view',
                                                                  'Bicycle','Family/kid friendly','Free parking on premises',
                                                                  'Kitchen','Pets allowed','Swimming pool', 'Wifi', 'Iron','Laptop friendly workspace') )
        filtered_df = adf[
            (adf['Country'] == selected_country) &
            (adf['Property_Type'] == selected_PROPERTY_TYPE) &
            (adf['Room_Type'] == selected_Room_Type) &
            ((adf['Availability_30'] >= int(selected_availability)) |
             (adf['Availability_60'] >= int(selected_availability)) |
             (adf['Availability_90'] >= int(selected_availability)) |
             (adf['Availability_365'] >= int(selected_availability)))
        ]
        if selected_Amenities:
            filtered_df = filtered_df[filtered_df['Amenities'].apply(lambda x: all(item in x for item in selected_Amenities))]


        selected_columns = ['Name', 'Price', 'Cleaning Fees', 'Security_deposit', 
                        'Bedroom Count', 'Total Beds','Cancellation_policy','Review_score', 'Amenities','Neighbourhood', 'Minimum_Nights',
                          'Maximum_Nights','Number of Reviews']
        result1_df = filtered_df[selected_columns]
        result1_df = result1_df.sort_values(by='Review_score', ascending=False)
              
        with st.expander("Filtered Dataframe"):
            st.dataframe(result_df)

# Select top 10 properties
        top_properties = result1_df.head(10)

        fig3 = px.bar(top_properties, 
                  x='Name', 
                  y=['Price', 'Cleaning Fees', 'Security_deposit'], 
                  title='Price, Cleaning Fees, and Security Deposit by Property Name',
                  labels={'value': 'Amount ($)', 'Name': 'Property Name'},
                  barmode='group')
    
        fig3.update_layout(
        xaxis_title='Property Name',
        legend_title_text='Type',
        xaxis={'categoryorder':'total descending'}
        )

        st.plotly_chart(fig3, use_container_width=True)
        amenities_list = ['24-hour check-in', 'TV', 'Air conditioning', 'Beach view',
                            'Bicycle','Family/kid friendly','Free parking on premises',
                             'Kitchen','Pets allowed','Swimming pool', 'Wifi', 'Iron','Laptop friendly workspace']

        amenities_count = count_amenities(adf, amenities_list)
    
        amenities_df = pd.DataFrame(list(amenities_count.items()), columns=['Amenity', 'Count'])
        amenities_df = amenities_df.sort_values(by='Count', ascending=False)

        fig2 = px.bar(amenities_df, x='Amenity', y='Count', title='Most Common Amenities',
                  labels={'Amenity': 'Amenity', 'Count': 'Number of Properties'},
                  color='Amenity')
    
        st.plotly_chart(fig2, use_container_width=True)

        
if selected == "INSIGHTS":   
    
    selected_country = st.selectbox('Select Country', adf['Country'].unique(), key="Select Country1")
    filtered_df = adf[adf['Country'] == selected_country]
    filtered_df = filtered_df.sort_values(by='Review_score', ascending=False)

# Select top 10 properties
    top_properties = filtered_df.head(10)

    # Dual-axis line chart for Review Score and Price
    st.markdown(f"### Review Score and Price for Top 10 Properties in {selected_country}")

    fig = go.Figure()

    colors = ['rgba(255, 71, 80, 0.6)', 'rgba(128, 0, 128, 0.6)', 'rgba(0, 128, 128, 0.6)', 'rgba(255, 0, 0, 0.6)',
          'rgba(0, 255, 0, 0.6)', 'rgba(0, 0, 255, 0.6)', 'rgba(255, 255, 0, 0.6)', 'rgba(255, 165, 0, 0.6)',
          'rgba(75, 0, 130, 0.6)', 'rgba(255, 192, 203, 0.6)']

    # Add line for Review Score
    fig.add_trace(go.Bar(
    x=top_properties['Name'], 
    y=top_properties['Price'], 
    name='Price', 
    yaxis='y1',
    marker=dict(color='rgba(58, 71, 80, 0.6)'),
    marker_color=colors,
    hovertemplate='Price: $%{y}<extra></extra>'))

    # Add line for Price
    fig.add_trace(go.Scatter(
    x=top_properties['Name'], 
    y=top_properties['Review_score'], 
    mode='lines+markers', 
    name='Review Score', 
    yaxis='y2',
    line=dict(color='red', width=2),
    marker=dict(color='red', size=8),
    hovertemplate='Review Score: %{y}<extra></extra>'))
    # Create secondary y-axis
    # Create dual y-axis
    fig.update_layout(
    title=f'Review Score and Price for Top 10 Properties in {selected_country}',
    xaxis_title='Property Name',
    yaxis=dict(
        title='Price ($)',
        titlefont=dict(color='rgba(58, 71, 80, 0.6)'),
        tickfont=dict(color='rgba(58, 71, 80, 0.6)'),
    ),
    yaxis2=dict(
        title='Review Score',
        titlefont=dict(color='red'),
        tickfont=dict(color='red'),
        overlaying='y',
        side='right'
    ),
    legend=dict(
        x=0.1,
        y=1.1,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("### Insights for Total Beds, Bedrooms, and Accommodates")
    
    fig1 = px.scatter(top_properties, 
                      x='Name', 
                      y='Bedroom Count', 
                      size='Accomodates', 
                      color='Total Beds', 
                      title='Scatter plot of Total Beds vs. Bedrooms',
                      labels={'Total Beds': 'Total Beds', 'Bedroom Count': 'Bedrooms', 'Accomodates': 'Accommodates'},
                      hover_data=['Name', 'Price'])
    
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### Minimum and Maximum Nights by Property")

    # Melt the DataFrame for plotting
    min_max_nights_df = top_properties.melt(id_vars=['Name'], value_vars=['Minimum_Nights', 'Maximum_Nights'], 
                                            var_name='Night Type', value_name='Nights')

    fig_min_max_nights = px.bar(
        min_max_nights_df,
        x='Nights',
        y='Name',
        color='Night Type',
        orientation='h',
        title='Minimum and Maximum Nights by Property',
        labels={'Nights': 'Number of Nights', 'Name': 'Property Name'},
        barmode='group',
        color_discrete_map={'Minimum_nights': '##ADD8E6', 'Maximum_nights': '#90EE90'}  # Custom colors
        )

    fig_min_max_nights.update_layout(
        xaxis_title='Number of Nights',
        yaxis_title='Property Name',
        legend_title_text='Type of Nights',
        xaxis={'categoryorder': 'total descending'}
    )

    st.plotly_chart(fig_min_max_nights, use_container_width=True)