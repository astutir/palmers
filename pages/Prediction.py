import streamlit as st
import pandas as pd
import time
import numpy as np
from PIL import Image
from datetime import datetime
import pickle
from sklearn.naive_bayes import GaussianNB

 # Function to display the current date and time
def display_date_time():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%d-%m-%Y %H:%M:%S')
    day_name = current_datetime.strftime('%A')

    st.markdown(
        f"""
        <div style="text-align: right; color: #6DB9EF;
            border-radius: 25%; display: inline-block; font-size: medium; text-shadow: 3px red;
            padding: 2%; margin-left: 65%; font-weight: bold; text-decoration: underline;">
            {day_name}, {formatted_datetime}
        </div>
        """, unsafe_allow_html=True
    )

# Function to display parameter input header
def display_parameter_header():
    st.markdown(
        """
        <div style="text-align: center;">
            <h2 style="color: white;
            background-color: #11009E; border-radius: 20%; display: inline-block; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            border-style: groove; border-top: 15px; padding: 2%; margin: 5% 0; border-width: 25px;">
                The Parameter Imputation Window
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to generate styled HTML
def generate_style(column_name, value, background_color):
    return f'''
        <div style="
            background-color: {background_color};
            padding: 5px;
            border-radius: 10px;
            margin: 10% 0;
            text-align: center;
            font-size: 90%;
            font-weight: bold;
            color: blue;
            border: 10px groove #3081D0;
            border-top-style: double;
            border-top-left-radius: 30%;
            border-top-right-radius: 30%;
            box-shadow: 5px 5px 15px blue;
        ">
            {column_name}<br>
            <span style="color: #6DB9EF; font-size: 220%; font-weight: bold; padding-top: 10px;">{value}</span>
        </div>
    '''

# Display snow effect and welcome toast
st.snow()
st.toast('Welcome to this Page!', icon='🎉')

# Display date and time
display_date_time()

# Display input parameter header
display_parameter_header()

# File uploader for CSV file
upload_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
st.sidebar.info('Input this Parameter, please!')

# If file is uploaded
if upload_file is not None:
    inputan = pd.read_csv(upload_file)
    if st.sidebar.button('Submit'):
        st.write(inputan)  # Display the uploaded data
        with st.spinner('Wait for it...'):
            time.sleep(2)
        st.sidebar.success('Prediction is Success!')

else:
    inputan = None

    def input_user():
        island = st.sidebar.selectbox("Island", ("Biscoe", "Dream", "Torgersen"))
        sex = st.sidebar.radio("Sex", ("male", "female"))
        bill_length = st.sidebar.slider("Length of Bill (mm)", 32.1, 59.6, 43.0)
        bill_depth = st.sidebar.slider("Depth of Bill (mm)", 13.1, 21.5, 17.0)
        flipper_length = st.sidebar.slider("Length of Flipper (mm)", 172.0, 231.0, 201.0)
        body_mass = st.sidebar.slider("Body Mass (g)", 2700.0, 6300.0, 4207.0)
        
        data = {
            "island": island,
            "sex": sex,
            "bill_length_mm": bill_length,
            "bill_depth_mm": bill_depth,
            "flipper_length_mm": flipper_length,
            "body_mass_g": body_mass
        }
        fitur = pd.DataFrame(data, index=[0])
        
        tombol = st.sidebar.button('Submit')           
        if tombol:
            progress_text = "Operation in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()
            with st.spinner('Wait for it...'):
                time.sleep(2)
            st.sidebar.success('Prediction is Success!')
            return fitur 
    
    inputan = input_user()

# Load dataset and model
penguin_raw = pd.read_csv("penguins_cleaned.csv")
penguins = penguin_raw.drop(columns=["species"])
df = pd.concat([inputan, penguins], axis=0)

# Encode features
encode = ["sex", "island"]
if upload_file is not None:
    dummy = pd.get_dummies(inputan[["sex", "island"]], prefix=["sex", "island"])
    df = pd.concat([inputan, dummy], axis=1)
    df.drop(["sex", "island"], axis=1, inplace=True)
    df = df.drop(columns=["species"])
else:  
    for col in encode:
        dummy = pd.get_dummies(df[col], prefix=col)
        df = pd.concat([df, dummy], axis=1)
        del df[col]
    df = df[:1]  # Take the first row (input data user)

# Display parameter information
col1, col2 = st.columns(2)

if upload_file is not None:
    col1.markdown(generate_style('Mode of Island', inputan['island'].mode().iloc[0], '#FFF5C2'), unsafe_allow_html=True)
    col2.markdown(generate_style('Mode of Sex', inputan['sex'].mode().iloc[0], '#FFF5C2'), unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(generate_style('Bill Depth (mm)', df['bill_depth_mm'][0], 'yellow'), unsafe_allow_html=True)
    col2.markdown(generate_style('Flipper Length (mm)', df['flipper_length_mm'][0], 'yellow'), unsafe_allow_html=True)
    col3.markdown(generate_style('Bill Length (mm)', df['bill_length_mm'][0], 'yellow'), unsafe_allow_html=True)
    col4.markdown(generate_style('Body Mass (g)', df['body_mass_g'][0], 'yellow'), unsafe_allow_html=True)
else:
    if df['island_Dream'][0]:
        col1.markdown(generate_style('Island', 'Dream', '#FFF5C2'), unsafe_allow_html=True)
    elif df['island_Biscoe'][0]:
        col1.markdown(generate_style('Island', 'Biscoe', '#FFF5C2'), unsafe_allow_html=True)
    else:
        col1.markdown(generate_style('Island', 'Torgersen', '#FFF5C2'), unsafe_allow_html=True)

    if df['sex_male'][0]:
        col2.markdown(generate_style('Sex', 'Male', '#FFF5C2'), unsafe_allow_html=True)
    else:
        col2.markdown(generate_style('Sex', 'Female', '#FFF5C2'), unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(generate_style('Bill Depth (mm)', df['bill_depth_mm'][0], 'yellow'), unsafe_allow_html=True)
    col2.markdown(generate_style('Flipper Length (mm)', df['flipper_length_mm'][0], 'yellow'), unsafe_allow_html=True)
    col3.markdown(generate_style('Bill Length (mm)', df['bill_length_mm'][0], 'yellow'), unsafe_allow_html=True)
    col4.markdown(generate_style('Body Mass (g)', df['body_mass_g'][0], 'yellow'), unsafe_allow_html=True)

# Load the Naive Bayes model
load_model = pickle.load(open("modelNBC_penguin.pkl", "rb"))

# Predict and display results
prediksi = load_model.predict(df)
prediksi_proba = load_model.predict_proba(df)
jenis_penguin = np.array(["Adelie", "Chinstrap", "Gentoo"])

st.markdown(
    """
    <div style="">
        <h3 style="color: #11009E;
        background-color: #FFF78A; border-radius: 25%; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        border-style: double; border-top: 15px; padding: 2%; margin: 10% 0; border-width: 5px; text-decoration: wavy; box-shadow: 0px 0px 10px 2px rgba(0,0,0,0.5); display: inline-block;">
            The Result of Species Prediction
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)
predicted_species = jenis_penguin[prediksi][0]
col1, col2 = st.columns(2)

col2.markdown(f"""
<div style="text-align: center; color: #B80000; font-size: 37px; font-weight: bold; text-transform: capitalize;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    border: 2px solid rgba(0, 0, 0, 0.1); border-radius: 10px;
    padding: 10px; box-shadow: 0px 0px 9px 12px #B31312;
    display: inline-block; margin: 10% 10% 10% 10%; justify-content: center; align-content: center; align-items: center;">
    {predicted_species}
</div>
""", unsafe_allow_html=True)

# Display image based on prediction
if predicted_species == "Gentoo":
    image = Image.open('gentoo-sk.png').resize((700, 451))
    col1.image(image)
elif predicted_species == "Adelie":
    image = Image.open('adelie-sk.png').resize((700, 451))
    col1.image(image)
else:
    image = Image.open('chisntrap.png').resize((700, 451))
    col1.image(image)

st.markdown(
    """
    <div style="">
        <h3 style="color: #11009E;
        background-color: #FFF78A; border-radius: 25%; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        border-style: double; border-top: 15px; padding: 1%; margin: 5% 0; border-width: 5px; box-shadow: 0px 0px 10px 2px rgba(0,0,0,0.5); display: inline-block;">
            Probability Prediction
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

# Display prediction probabilities
col1, col2, col3 = st.columns(3)
pre = pd.DataFrame(prediksi_proba)

col1.markdown(f'<div style="color: blue; font-size: 30px; font-weight: bold; text-align: center; background-color: #e0e0e0; border-radius: 5px; box-shadow: 5px 10px 20px blue; padding: 3px; margin: 12%;">Adelie<br><span style="color: #776B5D; font-size: 150%; font-weight: bold; padding-top: 5px;">{pre[0][0]:,.3f}</span></div>', unsafe_allow_html=True)

col2.markdown(f'<div style="color: green; font-size: 30px; font-weight: bold; text-align: center; background-color: #e0e0e0; border-radius: 5px; box-shadow: 5px 10px 20px green; padding: 3px; margin: 12%;">Chinstrap<br><span style="color: #776B5D; font-size: 150%; font-weight: bold; padding-top: 5px;">{pre[1][0]:,.3f}</span></div>', unsafe_allow_html=True)

col3.markdown(f'<div style="color: red; font-size: 30px; font-weight: bold; text-align: center; background-color: #e0e0e0; border-radius: 5px; box-shadow: 5px 10px 20px red; padding: 3px; margin: 12%;">Gentoo<br><span style="color: #776B5D; font-size: 150%; font-weight: bold; padding-top: 5px;">{pre[2][0]:,.3f}</span></div>', unsafe_allow_html=True)



   