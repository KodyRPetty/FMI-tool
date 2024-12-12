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

    # Display the likelihood in a colorful box
    if likelihood == "FMI LOW likelihood":
        st.markdown(f"<div style='background-color:green;color:white;padding:10px;border-radius:5px;text-align:center;'>{likelihood}</div>", unsafe_allow_html=True)
    elif likelihood == "FMI MEDIUM likelihood":
        st.markdown(f"<div style='background-color:orange;color:white;padding:10px;border-radius:5px;text-align:center;'>{likelihood}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color:red;color:white;padding:10px;border-radius:5px;text-align:center;'>{likelihood}</div>", unsafe_allow_html=True)

    # Create a bar chart showing the number of users with each column count
    fig, ax = plt.subplots()
    sns.barplot(x=user_columns_above_3.value_counts().index, y=user_columns_above_3.value_counts())
    ax.set_xlabel("Number of Columns > 3")
    ax.set_ylabel("Number of Users")
    st.pyplot(fig)

# Streamlit app
st.title("Twitter Data Analysis")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(uploaded_file)
    analyze_twitter_users(df)