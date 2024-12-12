import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def analyze_twitter_users(df):
    # Get the list of column names
    columns = df.columns.tolist()

    # Identify the columns that should be used for the analysis
    analysis_columns = [col for col in columns if col not in ['username']]

    # Convert the analysis columns to numeric data types
    for col in analysis_columns:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            # If the column cannot be converted to float, skip it
            analysis_columns.remove(col)
            print(f"Skipping column '{col}' due to non-numeric data.")

    # Count the number of columns with values greater than 3 for each Social Media user
    user_columns_above_3 = df[analysis_columns].gt(3).sum(axis=1)

    # Count the number of Social Media users with at least 3 columns above 3
    num_users_above_3 = (user_columns_above_3 >= 3).sum()

    # Determine the likelihood based on the number of users
    if num_users_above_3 < 3:
        likelihood = "FMI LOW likelihood"
    elif num_users_above_3 < 10:
        likelihood = "FMI MEDIUM likelihood"
    else:
        likelihood = "FMI HIGH likelihood"

    # Display the likelihood in a colorful box with the number of users
    if likelihood == "FMI LOW likelihood":
        st.markdown(f"<div style='background-color:green;color:white;padding:10px;border-radius:5px;text-align:center;'>{likelihood} ({num_users_above_3} Social Media Users)</div>", unsafe_allow_html=True)
    elif likelihood == "FMI MEDIUM likelihood":
        st.markdown(f"<div style='background-color:orange;color:white;padding:10px;border-radius:5px;text-align:center;'>{likelihood} ({num_users_above_3} Social Media Users)</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color:red;color:white;padding:10px;border-radius:5px;text-align:center;'>{likelihood} ({num_users_above_3} Social Media Users)</div>", unsafe_allow_html=True)

    # Create a bar chart showing the top 5 Social Media users by number of columns above 3
    top_users = user_columns_above_3.sort_values(ascending=False).head(5)

    fig, ax = plt.subplots(figsize=(24, 12))
    ax.bar(range(len(top_users)), top_users.values, color='black')
    ax.set_xlabel("Social Media User", fontsize=16)
    ax.set_ylabel("Number of FMI-related indicators", fontsize=16)
    ax.set_title("Top 5 FMI-spreading Social Media Users", fontsize=20)

    # Set the x-axis tick labels
    top_user_names = df.iloc[top_users.index, 0].tolist()
    ax.set_xticks(range(len(top_user_names)))
    ax.set_xticklabels(top_user_names, rotation=90, fontsize=14)

    # Adjust the y-axis limits to ensure all bars are visible
    if np.isfinite(top_users.max()):
        ax.set_ylim(bottom=0, top=top_users.max() + 1)

    st.pyplot(fig)

    # Create a stacked bar chart for the social media user with the highest total sum of columns
    top_user_total_sum = df[analysis_columns].sum(axis=1).sort_values(ascending=False).index[0]
    top_user_name = df.iloc[top_user_total_sum, 0]
    top_user = df[analysis_columns].iloc[top_user_total_sum]

    fig, ax = plt.subplots(figsize=(24, 12))
    ax.bar(0, top_user.sum(), color=[f'C{i}' for i in range(len(analysis_columns))])
    bottom = 0
    for i, value in enumerate(top_user):
        ax.bar(0, value, bottom=bottom, color=f'C{i}', width=0.8)
        bottom += value
    ax.set_xlabel("Social Media User", fontsize=16)
    ax.set_ylabel("Total # of FMI indicators", fontsize=16)
    ax.set_title(f"The FMI-y of them all: {top_user_name}", fontsize=20)
    ax.set_xticks([0])
    ax.set_xticklabels([top_user_name], fontsize=14)

    # Add a legend
    legend_elements = [plt.Rectangle((0, 0), 1, 1, color=f'C{i}', label=col) for i, col in enumerate(analysis_columns)]
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14)

    st.pyplot(fig)

# Streamlit app
st.title("Social Media Data Analysis")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(uploaded_file)
    analyze_twitter_users(df)