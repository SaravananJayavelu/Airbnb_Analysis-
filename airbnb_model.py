# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
df=pd.read_csv(r"C:\GUVI\Code\Project\.venv\Project_4 Airbnb Analysis\final_airbnb.csv")

# Set page config for the web app
st.set_page_config(page_title='Airbnb Analysis', 
    page_icon=':bar_chart:', 
    layout='wide')
st.title('Airbnb Analysis')


# Sidebar for filters
with st.sidebar:
    st.code('FILTERS')
    country=st.selectbox('Country',options=df['country'].unique())
    room_type=st.selectbox('Room Type',options=df['room_type'].unique())
    rating=st.slider('Ratings Range', 0,100,(0,100))
    city=st.selectbox('City',options=df.query(f"country=='{country}'")['suburb'].unique())
    price=st.slider('Price Range', 0,48842,(0,48842))

# Map for listings
st.map(df.query(f"suburb=='{city}' and room_type=='{room_type}' and review_scores>={rating[0]} and review_scores<={rating[1]} and country=='{country}' and price>={price[0]} and price<={price[1]}")[['latitude','longitude']].dropna(how="any"), zoom=5)

# Visualisations
outdf=df.query(f"suburb=='{city}' and room_type=='{room_type}' and review_scores>={rating[0]} and review_scores<={rating[1]} and country=='{country}' and price>={price[0]} and price<={price[1]}")
listdf=(outdf[['name','guests_included']].sort_values(by=['guests_included'],ascending=[False]).dropna(how="any")).head(10)
fig1 = px.histogram(listdf,y="name", x="guests_included", title = ' Most visited listings', orientation='h')
st.plotly_chart(fig1)
viscol1,viscol2=st.columns(2)

with viscol1:
    roomdf=df.query(f"suburb=='{city}'and review_scores>={rating[0]} and review_scores<={rating[1]} and country=='{country}' and price>={price[0]} and price<={price[1]}")
    figroom=px.histogram(roomdf, x="room_type",title='Roomtypes')
    st.plotly_chart(figroom)

    figcancel=px.bar(outdf, x="cancellation_policy",title='Cancellation Policy')
    st.plotly_chart(figcancel)

    figaccom=px.histogram(outdf, x="accommodates",title='Accommodates')
    st.plotly_chart(figaccom)

with viscol2:
    fig = px.scatter(outdf,x="bed_type", y ="review_scores", title = 'Most Loved Bedtypes', color="bed_type")
    st.plotly_chart(fig)

    piefig=px.pie(outdf, names="bedrooms",title='Bedrooms Available')
    st.plotly_chart(piefig)

    hostdf=outdf[['host_name','host_response_rate','host_response_time','host_total_listings_count']].dropna(how="any")
    hostfig=px.scatter(hostdf,x="host_response_time", y ="host_name", title = 'Host Response Time', color="host_response_time")
    st.plotly_chart(hostfig)

# Dataframes
col6,col7=st.columns(2)
with col6:
    st.write('Number of listings',len(outdf))
    st.write(outdf[['name','review_scores']].rename(columns={'name':'Name','review_scores':'Rating'}).sort_values('Rating',ascending=False).reset_index(drop=True))
with col7:
    hostdf=outdf[['host_name','host_response_rate','host_response_time','host_total_listings_count']].dropna(how="any")
    st.write('Number of Hosts',len(hostdf['host_name'].unique()))
    st.write(hostdf.rename(columns={'host_name':'Name','host_response_rate':'Response Rate','host_response_time':'Response Time','host_total_listings_count':'Listings Count'}).sort_values(by=['Listings Count'],ascending=[False]).reset_index(drop=True))