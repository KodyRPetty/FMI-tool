import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_twitter_users(df):
    # Count the number of columns with values greater than 3 for each Twitter user
    user_columns_above_3 = df.loc[:, 'Ukranazis':'Other (MH17 Or Skripal Or Crocus)'].gt(3).sum(axis=1)

    # Count the number of Twitter users with at least 3 columns above 3
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
        st.markdown(f"<div style='background-color:green;color:white;padding:10px;border-radius:5px;text-align:center;'>{likelihood} ({num_users_above_3} Twitter Users)</div>", unsafe_allow_html=True)
    elif likelihood == "FMI MEDIUM likelihood":
        st.markdown(f"<div style='background-color:orange;color:white;padding:10px;border-radius:5px;text-align:center;'>{likelihood} ({num_users_above_3} Twitter Users)</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color:red;color:white;padding:10px;border-radius:5px;text-align:center;'>{likelihood} ({num_users_above_3} Twitter Users)</div>", unsafe_allow_html=True)

    # Create a bar chart showing the top 20 Twitter users by number of columns above 3
    top_users = user_columns_above_3.sort_values(ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=top_users.index, y=top_users.values, ax=ax)
    ax.set_xlabel("Twitter User")
    ax.set_ylabel("Number of Columns > 3")
    ax.set_title("Top 20 Twitter Users by Columns Above 3")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)

# Streamlit app
st.title("Twitter Data Analysis")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(uploaded_file)
    analyze_twitter_users(df)