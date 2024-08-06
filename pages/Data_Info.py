import streamlit as st
import plotly.express as px
import pandas as pd
import os
import time
from PIL import Image
import warnings
from io import BytesIO
import base64
from datetime import datetime

warnings.filterwarnings('ignore')
st.snow()

# Function to calculate metrics
def calculate_metrics(filtered_data):
    avg_bill_length = round(filtered_data['bill_length_mm'].mean(), 2)
    avg_flipper_length = round(filtered_data['flipper_length_mm'].mean(), 2)
    avg_body_mass = round(filtered_data['body_mass_g'].mean(), 2)
    penguin_count = filtered_data.shape[0]

    return avg_bill_length, avg_flipper_length, penguin_count, avg_body_mass


st.markdown(
"""
<div style="text-align: center;">
    <h1 style="color: #525CEB;
    background-color:white;border-radius: 25%;display: inline-block;text-shadow: 2px 2px 4px yellow;
    display:inline-flex;border-style:groove;border-top: 15cap;padding: 2%;margin: 5% 0;border-width: 30px;">Palmer Penguins Dataset Analysis</h1>
</div>
""",
    unsafe_allow_html=True
)

def tanggal():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%d-%m-%Y %H:%M:%S')
    day_name = current_datetime.strftime('%A')  # Mendapatkan nama hari

    st.markdown(
        f"""
        <div style="text-align: right; color: #6DB9EF;
            border-radius: 25%; display: inline-block; font-size: medium;text-shadow: 3px red;
            padding: 2%; margin-left: 65%;font-weight: bold;text-decoration: underline;">
            {day_name}, {formatted_datetime}
        </div>
        """, unsafe_allow_html=True
    )
tanggal()


with st.spinner('Wait for it...'):
    time.sleep(0.05)
fl = st.file_uploader("📁 Upload a file", type=(["csv", "txt", "xlsx", "xls"]))

if st.toast('Choose the Filter!', icon='🚀'):
    time.sleep(1)
    with st.spinner('Wait for it...'):
        time.sleep(1)
st.sidebar.info('Choose your Filter below ⬇️')
if fl is not None:
    filename = fl.name
    with st.spinner('Wait for it...'):
        time.sleep(1)
    # st.write(filename)
    
    df = pd.read_csv(fl, usecols=['sex', 'species', 'island', 'bill_depth_mm', 'bill_length_mm', 'body_mass_g', 'flipper_length_mm'])
    st.success('Upload data is Success!')
       
else:
    # Change the directory and filename as per your penguins dataset
    
       
    df = pd.read_csv("penguins_cleaned.csv", usecols=['sex', 'species', 'island', 'bill_depth_mm', 'bill_length_mm', 'body_mass_g', 'flipper_length_mm'])

# st.sidebar.header("Choose your filter:")

species = st.sidebar.multiselect("Pick your Species", df["species"].unique())
if not species:
    df2 = df.copy()
else:
    df2 = df[df["species"].isin(species)]
    

island = st.sidebar.multiselect("Pick the Island", df2["island"].unique())
if not island:
    df3 = df2.copy()
else:
    df3 = df2[df2["island"].isin(island)]
   

sex = st.sidebar.multiselect("Pick the Sex", df3["sex"].unique())

if not sex:
    df4 = df3.copy()
else:
    df4 = df3[df3["sex"].isin(sex)]


if not species and not island and not sex:
    filtered_df = df
elif not island and not sex:
    filtered_df = df[df["species"].isin(species)]
elif not species and not sex:
    filtered_df = df[df["island"].isin(island)]
elif island and sex:
    filtered_df = df3[df3["island"].isin(island) & df3["sex"].isin(sex)]
elif species and sex:
    filtered_df = df3[df3["species"].isin(species) & df3["sex"].isin(sex)]
elif species and island:
    filtered_df = df3[df3["species"].isin(species) & df3["island"].isin(island)]
elif sex:
    filtered_df = df3[df3["sex"].isin(sex)]
else:
    filtered_df = df3[df3["species"].isin(species) & df3["island"].isin(island) & df3["sex"].isin(sex)]

# Calculate metrics based on user-selected filters
avg_bill_length, avg_flipper_length, penguin_count, avg_body_mass = calculate_metrics(filtered_df)


def generate_style(column_name, value, background_color):
    return f'''
        <div style="
            background-color: {background_color};
            padding: 15px;
            border-radius: 10px;
            margin: 10% 0;
            text-align: center;
            font-size: 100%;
            font-weight: bold;
            color: blue;
            border: 10px groove #3081D0;
            border-top-style: double;
            border-top-left-radius: 30%;
            border-top-right-radius: 30%;
            box-shadow: 5px 5px 15px #888888;
        ">
            {column_name}<br>
            <span style="color: #6DB9EF; font-size: 200%; font-weight: bold; padding-top: 10px;">{value}</span>
        </div>
    '''
if st.sidebar.button('Submit') or st.button('Dataset Analysis'):
    
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(0.07)
    my_bar.empty()
    # Metrics columns
    col1, col2, col3, col4 = st.columns(4)

    # Define background color
    background_color = "#FFF5C2"
    
    # Apply styles to columns
    col1.markdown(generate_style("Count Rows", penguin_count, '#EEF5FF'), unsafe_allow_html=True)
    col2.markdown(generate_style("AVG Bill Length (mm)", avg_bill_length, background_color), unsafe_allow_html=True)
    col3.markdown(generate_style("AVG Flipper Length (mm)", avg_flipper_length, background_color), unsafe_allow_html=True)
    col4.markdown(generate_style("AVG Body Mass (g)", avg_body_mass, background_color), unsafe_allow_html=True)
    

    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(0.07)
    my_bar.empty()
    
    with st.spinner('Wait for it...'):
        time.sleep(2)
    
    import math
    # Define a function to add color to DataFrame values
    def highlight(val, justify='center'):
        try:
            val = float(val)  # Convert the value to a float
        except ValueError:
            pass  # Handle non-numeric values if needed

        text_color = 'red' if val < 0 else '#3081D0'  # Text color based on condition
        background_color = '#FFEBD8'  # Background color for all cells
        formatted_val = f'{val:.3f}'.rstrip('0')

        return f'color: {text_color}; background-color: {background_color}; display: center;justify-content: space-between;box-shadow: 5px 5px 15px #888888;margin: 50px;text-align: {justify};padding: 15px;border-radius: 50px;', formatted_val
    # Display metrics dynamically
    st.markdown(
    """
    <div style="text-align: center;color: #0F2167;">
        <h2 style="color: #6DB9EF;
        ">Metrics Summary</h2>
    </div>
    """,
        unsafe_allow_html=True
    )
    # Custom HTML and CSS for Yellow Background Download Button with Underline
    yellow_button_html = f"""
        <style>
            .download-button {{
                background-color: #F4F27E;
                color: black;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: underline;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }}
        </style>
        <a href="data:file/text;base64,{base64.b64encode(filtered_df.describe().to_markdown().encode('utf-8')).decode('utf-8')}" download="penguin_analysis_report.md" class="download-button">
            Download Data Info
        </a>
    """

    
    # Download Button
    st.markdown(yellow_button_html, unsafe_allow_html=True)
    # Round and format the DataFrame
    formatted_df = filtered_df.describe().applymap(lambda x: highlight(x)[1]) 

    # DataFrame with Styler and color added to values
    styled_df = formatted_df.style.applymap(lambda x: highlight(x)[0])

    table_html = styled_df.to_html(escape=True, classes='no-border', table_styles=[{
        'selector': 'td, th',
        'props': [
            
            ('text-align', 'center'),
            ('font-size', '19px'),
            ('font-weight', 'bold'),
            ('margin', '10px'),('padding','0px'),('border', '4px solid #E0AED0'),
            ('display', 'center'),('box-shadow', '5px 5px 15px #888888'),('flex-flow', 'wrap'),('align-content','space-around'),('border-radius','12px'),
        ]
    },{
        'selector': 'thead,tbody',
        'props': [
            ('background-color','#E0AED0'),('display','center'),('border-radius','12px'),('margin','50px'),('box-shadow', '5px 5px 15px #888888'),('border', '4px solid #E0AED0'),
        ]
    },])


    centered_html = f"""
        <div style="display: flex; justify-content: center;margin: 2%;">
            {table_html}

    """

    st.markdown(centered_html, unsafe_allow_html=True)


    species_df = filtered_df.groupby(by=["species"], as_index=False)["body_mass_g"].mean()
    

    # Define col1 and col2
    col1, col2 = st.columns((2))

    # Custom CSS for theme
    custom_css = """
        <style>
            body {
                background-color: #f0f2f6; /* Set the background color */
                font-family: 'Arial', sans-serif; /* Set the font family */
                color: #2d3a4b; /* Set the text color */
                # margin-top: 10%;

            }

            h4 {
                color: #0F2167; /* Set the heading color */
                background-color:#FFF5C2;border-radius: 25%;display: inline-block;
                border-style: dashed;border-top: 10cap;margin-top: 15%;
            }
        </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)

    # Chart in col1
    with col1:
        st.markdown(
            """
            <div style="text-align: center;">
                <h4>The Body Mass of Palmer Penguins</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        fig = px.bar(species_df, x="species", y="body_mass_g",
                    text=['{:.2f}g'.format(x) for x in species_df["body_mass_g"]],
                    template="seaborn")
        
        # Set font size for labels in Plotly chart
        fig.update_layout(
            xaxis=dict(title=dict(font=dict(size=15))),
            yaxis=dict(title=dict(font=dict(size=15))),
            font=dict(size=15),
        )
        
        st.plotly_chart(fig, use_container_width=True, height=200)

    # Chart in col2
    with col2:
        st.markdown(
            """
            <div style="text-align: center;">
                <h4>The Palmer Penguins on the Island</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        fig = px.pie(filtered_df, values="body_mass_g", names="island", hole=0.5)
        fig.update_traces(text=filtered_df["island"], textposition="outside")
        
        # Set font size for labels in Plotly chart
        fig.update_layout(
            font=dict(size=15),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.sidebar.success('Success!')