import streamlit as st
import pandas as pd
import numpy as np
from calculation import perform_calculation

def design_app():
    # Setting up page configurations
    st.set_page_config(
        page_title="My Regional Cities Electricity Usage Report",
        page_icon=":fa-light fa-bolt:", 
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Setting up image links
    imagePath = "image/pic2.png"
    
    # Calling variables
    fiscalYear, city, averageEnergyConsumption, averageGasEmission, peakEnergyConsumption, dataForBar, dataForPie, total_consumption_per_month, controlled_load_per_month, peak_and_off_peak_by_month, peak_and_off_peak_by_quarter = perform_calculation()

    # Header Starts
    logo, title = st.columns([1, 11])
    logo.image(imagePath, width=100)
    title.markdown("<h1 style='font-size:50px;'>Regional Cities Electricity Usage Report</h1>", unsafe_allow_html=True)
    # st.markdown("<br>", unsafe_allow_html=True)
    # Header Ends

    # Select Options Starts
    citySelect, yearSelect = st.columns(2)
    with citySelect:
      selected_option = st.selectbox("Select Fiscal Year:", fiscalYear, index=0)
    with yearSelect:
      selected_option = st.selectbox("Select a City:", city, index=0)
    # Select Options Ends
    
    # For Gap
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI's Starts
    kpiInitial, energyKpi, greenHouseGasKpi, peakConsumption, lastKpi = st.columns([0.5, 2, 2, 2, 0.5])
    with energyKpi:
       st.write("<p style= 'margin-bottom: 0px; text-align: center'>Average Energy Consumption</p>", unsafe_allow_html=True)
       st.markdown("<h6 style='font-size: 30px; text-align: center;'>{} kWhs</h6>".format(averageEnergyConsumption), unsafe_allow_html=True)
    with greenHouseGasKpi:
       st.write("<p style= 'margin-bottom: 0px; text-align: center'>Average Green House Gas Emission</p>", unsafe_allow_html=True)
       st.markdown("<h6 style='font-size:30px; text-align: center;'>{} Tonnes</h6>".format(averageGasEmission), unsafe_allow_html=True)
    with peakConsumption:
       st.write("<p style= 'margin-bottom: 0px; text-align: center'>Peak Energy Consumption(kWhs)</p>", unsafe_allow_html=True)
       st.markdown("<h6 style='font-size: 30px; text-align: center;'>{} kWhs</h6>".format(peakEnergyConsumption), unsafe_allow_html=True)
    # KPI's Ends

    # For Gap
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Section1 Starts
    graph1, graph2 = st.columns([7,5])
    with graph1:
       st.write("<p style= 'margin-bottom: 0px; text-align: center; '><b>Average Energy Consumption by Cities</b></p>", unsafe_allow_html=True)
       dataForBar.update_layout(width=600, height=450)
       st.plotly_chart(dataForBar, use_container_width=True)
    with graph2:
       st.write("<p style= 'margin-bottom: 0px; text-align: center'><b>Peak and Off Peak Power Usage</b></p>", unsafe_allow_html=True)
       dataForPie.update_layout(width=450, height=450)
       st.plotly_chart(dataForPie, use_container_width=True)
    # Section1 Ends
    
    # For Gap
    st.markdown("<br>", unsafe_allow_html=True)

    # Section2 Starts
    graph1, graph2 = st.columns(2)
    with graph1:
       st.write("<p style= 'text-align: center'><b>Monthly Power Consumption By Fiscal Year</b></p>", unsafe_allow_html=True)
       total_consumption_per_month.update_layout(legend_title_text='Legend', showlegend=False, height=450)
       st.plotly_chart(total_consumption_per_month, use_container_width=True)
    with graph2:
       st.write("<p style='text-align: center'><b>Monthly Controlled Load By Fiscal Year</b></p>", unsafe_allow_html=True)
       controlled_load_per_month.update_layout(legend_title_text='Legend', showlegend=False, height=450)
       st.plotly_chart(controlled_load_per_month, use_container_width=True)
    # Section2 Ends

   # Section3 Starts
    graph1, graph2 = st.columns([6,5])
    with graph1:
       st.write("<p style= 'margin-bottom: 5px; text-align: center; '><b>Monthly Peak and Off Peak Power Consumption</b></p>", unsafe_allow_html=True)
       st.plotly_chart(peak_and_off_peak_by_month, height=400)
    with graph2:
       st.write("<p style= 'margin-bottom: -5px; text-align: center'><b>Quarterly Peak and Off Peak Power Consumption</b></p>", unsafe_allow_html=True)
      #  total_consumption_per_month.update_layout(legend_title_text='Legend', showlegend=False, height=450)
       st.plotly_chart(peak_and_off_peak_by_quarter, use_container_width=True)
    # Section3 Ends