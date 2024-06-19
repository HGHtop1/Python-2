import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt 
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
st.set_page_config(page_title="BUSINESS IT | PYTHON 2", layout="wide")
st.title('BUSINESS IT | PYTHON 2')
st.subheader("BBA - BFA 2024")
st.title('📊 Student Performance Dashboard')
st.write("Welcome to our database. Here you will find all the necessary information you will need to study about student performance. Hopefully, our data will help you understand what we are doing here as data analysts.")

with st.expander("Group Information"):
    st.markdown(
        """
        1. Ngo Tuan Kiet - 10623025

        2. Hang Gia Han - 10623011

        3. Nguyen Hai Trieu - 10623046

        4. Tran Anh Khoa - 10623021

        5. Nguyen Khanh Ngan - 10623064
        """
    )

# Load the data
data = pd.read_csv(r'C:\Users\Admin\Downloads\streamlit\StudentsPerformance.csv')

# Sidebar for user inputs
st.sidebar.title("Filter Options")

# Filter options
gender_options = ['All'] + data['gender'].unique().tolist()
gender = st.sidebar.selectbox("Select Gender", gender_options)

race_options = ['All'] + data['race/ethnicity'].unique().tolist()
race = st.sidebar.selectbox("Select Race/Ethnicity", race_options)

parental_education_options = ['All'] + data['parental level of education'].unique().tolist()
parental_education = st.sidebar.selectbox("Select Parental Level of Education", parental_education_options)

lunch_options = ['All'] + data['lunch'].unique().tolist()
lunch = st.sidebar.selectbox("Select Lunch Type", lunch_options)

# Score selection options
score_options = ['math score', 'reading score', 'writing score']
selected_scores = st.sidebar.multiselect("Select Scores to Include in Correlation Matrix", score_options, default=score_options)

# Filter the dataset based on user selection
filtered_data = data.copy()
if gender != 'All':
    filtered_data = filtered_data[filtered_data['gender'] == gender]
if race != 'All':
    filtered_data = filtered_data[filtered_data['race/ethnicity'] == race]
if parental_education != 'All':
    filtered_data = filtered_data[filtered_data['parental level of education'] == parental_education]
if lunch != 'All':
    filtered_data = filtered_data[filtered_data['lunch'] == lunch]

# Calculate descriptive statistics
st.subheader("Descriptive Statistics")
st.write(filtered_data.describe())

# Show data table
st.subheader("Data Table")
st.dataframe(filtered_data)

# Create tabs for navigation
tab1, tab2 = st.tabs(["General relation", "Others"])

with tab1:
    st.subheader("Scatter Plot with Regression Line")
    scatter_x = st.selectbox("Select X-axis for Scatter Plot", score_options)
    scatter_y = st.selectbox("Select Y-axis for Scatter Plot", score_options, index=1)
    fig = px.scatter(filtered_data, x=scatter_x, y=scatter_y, color='gender', trendline="ols",
title=f'Scatter Plot of {scatter_x.capitalize()} vs {scatter_y.capitalize()}')
    st.plotly_chart(fig, use_container_width=True)

    # Correlation matrix heatmap
    if len(selected_scores) >= 2:
        st.subheader("Correlation Matrix Heatmap")
        cor_scores = filtered_data[selected_scores].corr()

        # Use Plotly to create the heatmap
        fig = go.Figure(data=go.Heatmap(
            z=cor_scores.values,
            x=cor_scores.columns,
            y=cor_scores.columns,
            colorscale='Viridis',
            zmin=0.8,
            zmax=1,
            text=cor_scores.values,
            hoverinfo='text'
        ))

        fig.update_layout(
            title='Correlation Matrix for Selected Scores',
            xaxis_nticks=36,
            yaxis_nticks=36
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Distribution of Scores by Category")
    category = st.selectbox("Select Category for Distribution Plot", ['gender', 'race/ethnicity', 'lunch'])
    fig = px.histogram(filtered_data, x=category, color='gender', barmode='group',
                    title=f'Distribution of Scores by {category.capitalize()}')
    st.plotly_chart(fig, use_container_width=True)
    # Insights section
    st.subheader("Insights")
    st.markdown("""
        - **Correlation Insights**: The heatmap shows the correlation between different exam scores. Use it to understand how different scores relate to each other.
        - **Scatter Plot Analysis**: The scatter plot with a regression line helps to visualize relationships between different scores.
        - **Distribution Analysis**: The distribution plot shows how scores are distributed across different categories.
    """)




with tab2:
    st.title('Interactive Subject-wise Scores Visualization')

    # Preprocess the data
    df = data[['math score', 'reading score', 'writing score']]
    df = df.melt(var_name='subjects', value_name='scores')

    # Group and count the data
    df_counts = df.groupby(['scores', 'subjects']).size().reset_index(name='count')

    # Add user input features
    st.header('User Input Features')
    selected_subjects = st.multiselect(
        'Select Subjects to Display',
        options=df['subjects'].unique(),
        default=df['subjects'].unique()
    )

    # Filter data based on user input
    filtered_df_counts = df_counts[df_counts['subjects'].isin(selected_subjects)]

    # Create the scatter plot 
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter_plot = px.scatter(filtered_df_counts,
        x='count', y='scores', color='subjects', title='Subject-wise Scores'
    )
    scatter_plot.update_traces(marker=dict(size=20, opacity=0.6))
    scatter_plot.update_layout(
        width=900,
        height=500,
        title_font_size=24,
        title_x=0.5,
        xaxis=dict(
            title='Count',
            title_font=dict(size=26),
            tickfont=dict(size=16)
        ),
        yaxis=dict(
title='Scores',
            title_font=dict(size=26),
            tickfont=dict(size=16)
        ),
        legend_title=dict(font=dict(size=16)),
        legend=dict(
            title_font_size=20,
            font=dict(size=16)
        )
    )

    st.plotly_chart(scatter_plot)
    st.title('Preparation Distribution Based on Genders')

    # Data frame
    df_melted = pd.melt(data, id_vars='gender', value_vars=['test preparation course'], var_name='course', value_name='status')

    # Radio buttons to select gender
    selected_gender = st.radio(
        'Select Gender to Display',
        options=list(data['gender'].unique()) + ['Both'],  # Add 'Both' option
        index=len(data['gender'].unique())  # Select 'Both' by default
    )

    # Filter data based on selected gender(s)
    if selected_gender == 'Both':
        filtered_data = df_melted  # Show data for both genders
    else:
        filtered_data = df_melted[df_melted['gender'] == selected_gender]

    # Create the pie charts using Plotly Express with facet_col
    fig = px.pie(filtered_data, names='status', color='status', 
                facet_col='gender', facet_col_wrap=2, # Wrap to 2 columns
                title='Preparation Distribution Based on Genders',
                color_discrete_sequence=px.colors.qualitative.Pastel)

    # Update layout 
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title_font_size=26, 
        title_x=0.5, 
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Arial", size=16),
        legend_title=dict(font=dict(size=20)),
        legend=dict(
            title_font_size=20,
            font=dict(size=16)
        ),
        plot_bgcolor='#f0f0f0'
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)
# Add footer
st.markdown("""
    <style>
        footer {visibility: visible;}
        .reportview-container .main footer {visibility: visible;}
        .reportview-container .main footer:after {
        content:'Created with ❤️ by our group';
        visibility: visible;
        display: block;
        position: relative;
        color: black;
        padding: 5px;
        top: 2px;
        }
    </style>
""", unsafe_allow_html=True)
