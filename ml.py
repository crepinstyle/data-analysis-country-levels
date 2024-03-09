import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    st.title("Maternal and Infant Health Analysis")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        df = process_uploaded_file(uploaded_file)
        st.dataframe(df)

        analysis_level = st.sidebar.selectbox('Select Analysis Level', ['Province', 'District', 'sector', 'Health center'])
        selected_location = None

        if analysis_level == 'Province':
            selected_location = province_analysis(df)
        elif analysis_level == 'District':
            selected_location = district_analysis(df)
        elif analysis_level == 'sector':
            selected_location = sector_analysis(df)
        elif analysis_level == 'Health center':
            selected_location = health_center_analysis(df)

        perform_user_analysis(df, analysis_level, selected_location)

def process_uploaded_file(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

def province_analysis(df):
    st.title("Province Analysis")
    selected_location = st.sidebar.selectbox('Select Province', df['Province'].unique(), key="province_selectbox")
    distribution_analysis(df, 'Province', selected_location)
    return selected_location

def district_analysis(df):
    provinces_for_district = st.sidebar.multiselect('Select Provinces', df['Province'].unique(), key="district_provinces_multiselect")
    selected_location = st.sidebar.selectbox('Select District', filter_districts_by_province(df, provinces_for_district), key="district_selectbox")
    distribution_analysis(df, 'District', selected_location)
    return selected_location

def sector_analysis(df):
    districts = st.sidebar.multiselect('Select district', df['District'].unique(), key="province_districts_multiselect")
    selected_location = st.sidebar.selectbox('Select sector', filter_sectors_by_districts(df, districts), key="district_selectbox")
    distribution_analysis(df, 'sector', selected_location)
    return selected_location

def health_center_analysis(df):
    sectors_for_health_center = st.sidebar.multiselect('Select Sector', df['sector'].unique(), key='Health_center_sector_multiselect')
    selected_location = st.sidebar.selectbox('Select Health Center', filter_facilities_by_health_center(df, sectors_for_health_center), key='Health_center_selectbox')
    distribution_analysis(df, 'Health center', selected_location)
    return selected_location

def filter_districts_by_province(df, selected_provinces):
    filtered_districts = df[df['Province'].isin(selected_provinces)]['District'].unique()
    return filtered_districts
def filter_sectors_by_districts(df, selected_districts):
    filtered_sectors = df[df['District'].isin(selected_districts)]['sector'].unique()
    return filtered_sectors

def filter_facilities_by_health_center(df, selected_sectors):
    filtered_facilities = df[df['sector'].isin(selected_sectors)]['Health center'].unique()
    return filtered_facilities

def distribution_analysis(df, level, selected_location):
    st.title(f"Distributions of data - {level} Analysis")
    st.sidebar.subheader(f"Distribution of Variable Across {level}s")

    available_locations = df[level].unique()
    selected_locations = st.sidebar.multiselect(f'Select {level}s', available_locations, default=available_locations, key=f"selected_{level.lower()}s_multiselect")

    selected_data = df[df[level].isin(selected_locations)]

    selected_variable = st.sidebar.selectbox('Select Variable for Distribution', df.columns, key="selected_variable_selectbox")
    selected_visualization = st.sidebar.selectbox("Select Visualization Type", ["Bar Plot", "Scatter Plot", "Line Plot", 'Pie Plot'])

    if selected_visualization == "Bar Plot":
        plt.figure(figsize=(10, 6))
        order = (
            selected_data.groupby(level)[selected_variable]
            .mean()
            .sort_values(ascending=False)
            .index
        )
        sns.barplot(data=selected_data, x=level, y=selected_variable, order=order, palette='YlOrRd')
        plt.xlabel(level)
        plt.ylabel(selected_variable)
        plt.title(f'Distribution of {selected_variable} across selected {level}s')
        st.pyplot(plt)

    elif selected_visualization == "Scatter Plot":
        # Add scatter plot code if needed
        pass
    elif selected_visualization == "Line Plot":
        # Add line plot code if needed
        pass
    elif selected_visualization == 'Pie Plot':
        plt.figure(figsize=(10, 6))
        selected_data[selected_variable].value_counts().plot.pie(autopct='%1.1f%%')
        plt.title(f'Pie Plot of {selected_variable} in {selected_location}')
        st.pyplot(plt)

def perform_user_analysis(df, analysis_level, selected_location):
    st.subheader(f"{analysis_level} - {selected_location} Analysis:")

    # Filter data based on selected location (province)
    selected_data = df[df[analysis_level] == selected_location]

    # Allow user to select X and Y variables
    x_variable = st.sidebar.selectbox('Select X Variable', df.columns, key="x_variable_selectbox")
    y_variable = st.sidebar.selectbox('Select Y Variable', df.columns, key="y_variable_selectbox")

    # Sort the data frame by the selected Y variable in descending order
    
    # Sort the data frame by the selected Y variable in ascending order
    selected_data = selected_data.sort_values(by=y_variable, ascending=False)

    # Visualization based on user selection
    st.write(f"Distribution of {y_variable} by {x_variable} in {selected_location}:")
    if selected_data.empty:
        st.warning(f"No data available at {selected_location}.")
    else:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=selected_data, x=x_variable, y=y_variable, order=selected_data[x_variable].unique(),palette='YlOrRd')  # Sort bars based on X variable
        plt.xlabel(x_variable)
        plt.ylabel(y_variable)

        # Update the title dynamically based on the selected location
        if analysis_level == 'Province':
            plt.title(f'Distribution of {y_variable} by {x_variable} in {selected_location} (Province)')
        elif analysis_level == 'District':
            plt.title(f'Distribution of {y_variable} by {x_variable} in {selected_location} (District)')
        elif analysis_level == 'sector':
            plt.title(f'Distribution of {y_variable} by {x_variable} in {selected_location} (Sector)')
        elif analysis_level == 'Health center':
            plt.title(f'Distribution of {y_variable} by {x_variable} in {selected_location} (Health Center)')

        st.pyplot(plt)


if __name__ == "__main__":
    main()
