import streamlit as st
from PIL import Image
from streamlit_extras.let_it_rain import rain
import os
from datetime import datetime
import base64

# Function to display and center the logo in the sidebar
def display_logo():
    logo_path = 'logo.png'  # Adjust path to your logo file
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        st.sidebar.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{encoded_image}" width="150" />
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.sidebar.error(f"Logo file '{logo_path}' not found. Please ensure the file is in the correct directory.")

# Function to display the header
def display_header():
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="color: #11009E; background-color: #FFF78A; border-radius: 25%; display: inline-block; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); border-style: double; padding: 2%; margin: 5% 0; border-width: 5px; box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, 0.5);">
                Palmer Penguins Prediction
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display the current date and time
def display_date_time():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%d-%m-%Y %H:%M:%S')
    day_name = current_datetime.strftime('%A')

    st.markdown(
        f"""
        <div style="text-align: right; color: #6DB9EF; border-radius: 25%; display: inline-block; font-size: medium; text-shadow: 3px red; padding: 2%; margin-left: 65%; font-weight: bold; text-decoration: underline;">
            {day_name}, {formatted_datetime}
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to display the penguin image
def display_penguin_image():
    img_path = 'lter_penguins.png'  # Adjust path to your image file
    if os.path.exists(img_path):
        img = Image.open(img_path).resize((700, 451))
        st.image(img, caption='Source: https://allisonhorst.github.io/palmerpenguins/', use_column_width=True)
    else:
        st.error(f"Image file '{img_path}' not found. Please ensure the file is in the correct directory.")

# Function to display data information
def display_data_info():
    st.markdown(
        """
        <span style="color: #0F2167; font-size: 19px;">**The Palmer Penguins** refer to a dataset that includes information about three species of penguins: **Adelie, Gentoo, and Chinstrap**. 
        This dataset is often used in data science and educational settings for various analyses and exercises.
        <br><br>The dataset was introduced by **Dr. Kristen Gorman** and the Palmer Station, Antarctica LTER (Long Term Ecological Research) program. 
        It includes measurements and observations of penguins collected from the Palmer Archipelago near the Palmer Station in Antarctica.</span>

        <span style="color: #6DB9EF; font-size: 35px; font-weight: bold; text-decoration: underline;"> Data Columns</span>
        1. `species`: Penguin species (Adelie, Chinstrap, or Gentoo).
        2. `island`: Island in the Palmer Archipelago where observations were made (Biscoe, Dream, or Torgersen).
        3. `bill_length_mm` and `bill_depth_mm`: Measure the length and depth of the penguin's bill, respectively.
        4. `flipper_length_mm`: Indicates the length of the penguin's flipper.
        5. `body_mass_g`: Represents the body mass of the penguin in grams.
        6. `sex`: Indicates the gender of the penguin, which can be `male` or `female` if the information is not available.
        """,
        unsafe_allow_html=True
    )

# Function to display the culmen image
def display_culmen_image():
    img_path = 'culmen_depth.png'  # Adjust path to your image file
    if os.path.exists(img_path):
        img = Image.open(img_path).resize((700, 451))
        st.image(img, caption='Source: https://allisonhorst.github.io/palmerpenguins/', use_column_width=True)
    else:
        st.error(f"Image file '{img_path}' not found. Please ensure the file is in the correct directory.")

# Function to display additional information
def display_additional_info():
    st.write(
        """
        <p style="color: #0F2167; font-size: 19px;">Researchers and data scientists use the Palmer Penguins dataset for tasks like exploratory data analysis, classification, regression, and clustering. It serves as a practical and interesting dataset for learning and practicing data science techniques while also contributing valuable information about penguin populations in the Antarctic region.<br><br>This dataset is widely used in the data science and machine learning community for exercises, experiments, and data analysis technique demonstrations.</p>
        """,
        unsafe_allow_html=True
    )


# Optional: Add rain effect
rain(
    emoji="❄️",
    font_size=25,
    falling_speed=7,
    animation_length="infinite",
)

# Display content for the single page
display_logo()
st.sidebar.markdown('This application is designed to help users quickly and accurately learn about the species of Palmer Penguins')

display_header()
display_date_time()
display_penguin_image()
display_data_info()
display_culmen_image()
display_additional_info()

# Info message with a link to the dataset
st.info('For more information, you can access the Palmer Penguins dataset on GitHub: [palmerpenguins](https://github.com/allisonhorst/palmerpenguins)')


