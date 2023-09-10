import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import timedelta


def perform_calculation():
    df = pd.read_excel(r"C:\Users\saura\OneDrive\Desktop\Extratech\Python\analysis-on-vec\data\electricity_data.xlsx")
    print(df.columns)

    # Changing date to datetime format
    df[['Usage Period From', 'Usage Period To']] = df[['Usage Period From', 'Usage Period To']].apply(pd.to_datetime, format='%Y%m%d')
    print(df[['Usage Period From', 'Usage Period To']])

    # Calculating Usage Days
    df['Usage Days'] = df['Usage Days'].fillna(((df['Usage Period To'] - df['Usage Period From'])+timedelta(days=1)).dt.days)
    print(df['Usage Days'])
    print(df['Usage Days'].isnull().any())

    # Calculating missing Peak Kwhs
    df['Peak kWhs'] = df['Peak kWhs'].fillna(df['Total Consumption kWhs'] - df['Off Peak kWhs'] - df['Controlled Load kWhs'])
    print(df['Peak kWhs'])
    print(df['Peak kWhs'].isnull().any())

    # Finding Usage Year
    df['Usage Year'] = df['Usage Period From'].dt.year
    print(df)
    
    # Finding Quarter
    df['Quarter'] = pd.PeriodIndex(df['Usage Period From'], freq='Q-JUN')

    #Finding Fiscal Year
    df['Fiscal Year'] = df['Usage Period From'].apply(lambda x: f"{x.year}-{(x.year + 1)%100:02d}" if x.month >= 7 else f"{(x.year - 1)}-{x.year%100:02d}")
    print(df['Fiscal Year'])
    fiscalYear = df['Fiscal Year'].unique()
    fiscalYear = np.concatenate((['All Fiscal Year'], fiscalYear))

    #Finding Cities
    df['City'] = df['Address'].str.split(',').str[-2].str.strip()
    city = df['City'].unique()
    city = np.concatenate((['All Cities'], city))
    city = city[city != '']
    print(city)

    # Calculating Average Energy Consumption for KPI's
    averageEnergyConsumption = df['Total Consumption kWhs'].mean().round(2).astype(str)

    # Calculating Average Green House Gas Emission for KPI's
    averageGasEmission = df['Green House Gas Emissions (Tonnes)'].mean().round(2).astype(str)

    # Calculating Peak Energy Consumption for KPI's
    peakEnergyConsumption = df['Peak kWhs'].max().astype(str)

    # Finding Energy Consumption By City for Bar
    energyConsumptionByCity = df.groupby([ 'City', 'Fiscal Year'])['Total Consumption kWhs'].sum().unstack()
    energyConsumptionByCity = energyConsumptionByCity.reset_index().melt(id_vars='City', var_name='Fiscal Year', value_name='Total Consumption kWhs')
    energyConsumptionByCity = energyConsumptionByCity.sort_values(by='Total Consumption kWhs', ascending=False).head(20)
    custom_colors = {'2014-15': 'coral', '2015-16': 'teal'}
    dataForBar = px.bar(energyConsumptionByCity, x='City', y='Total Consumption kWhs', color='Fiscal Year', barmode='group', color_discrete_map=custom_colors)
   
    # Finding Peak and Off Peak Consumption for Pie
    sum_peak_kwhs = df['Peak kWhs'].mean()
    sum_off_peak_kwhs = df['Off Peak kWhs'].mean()
    dataForPie = px.pie(
        names=['Peak kWhs', 'Off-Peak kWhs'],
        values=[sum_peak_kwhs, sum_off_peak_kwhs],
        color_discrete_sequence=['coral', 'teal']
    )
    
    # Finding Average Total Consumption per month
    total_consumption_per_month = df.groupby(df['Usage Period From'].dt.to_period('M'))['Total Consumption kWhs'].mean()
    total_consumption_per_month = total_consumption_per_month.reset_index()
    total_consumption_per_month['Usage Period From'] = total_consumption_per_month['Usage Period From'].dt.strftime('%Y-%m')
    total_consumption_per_month = px.line(total_consumption_per_month, x='Usage Period From', y=['Total Consumption kWhs'], color_discrete_sequence=['#FF5733', '#FFB733'])
    
    # Finding Average Controlled Load per month
    controlled_load_per_month = df.groupby(df['Usage Period From'].dt.to_period('M'))['Controlled Load kWhs'].mean()
    controlled_load_per_month = controlled_load_per_month.reset_index()
    controlled_load_per_month['Usage Period From'] = controlled_load_per_month['Usage Period From'].dt.strftime('%Y-%m')
    controlled_load_per_month = px.line(controlled_load_per_month, x='Usage Period From', y=['Controlled Load kWhs'], color_discrete_sequence=['#33CC99', '#FFB533'])

    # Finding Peak and Off Peak Consumption per Month for Fiscal Year
    peak_and_off_peak_by_month = df.groupby(df['Usage Period From'].dt.to_period('M')).agg({'Peak kWhs': 'mean', 'Off Peak kWhs': 'mean'})
    peak_and_off_peak_by_month = peak_and_off_peak_by_month.reset_index()
    peak_and_off_peak_by_month['Usage Period From'] = peak_and_off_peak_by_month['Usage Period From'].dt.strftime('%Y-%m')
    peak_and_off_peak_by_month = px.line(peak_and_off_peak_by_month, x='Usage Period From', y=['Peak kWhs', 'Off Peak kWhs'], color_discrete_sequence=['coral', 'teal'])
    
    # Finding Peak and Off Peak Consumption Quarterly
    peak_and_off_peak_by_quarter = df.groupby(df['Quarter']).agg({'Peak kWhs': 'mean', 'Off Peak kWhs': 'mean'})
    peak_and_off_peak_by_quarter = peak_and_off_peak_by_quarter.reset_index()
    peak_and_off_peak_by_quarter['Quarter'] = peak_and_off_peak_by_quarter['Quarter'].dt.strftime('%YQ%q')
    peak_and_off_peak_by_quarter = px.line(peak_and_off_peak_by_quarter, x='Quarter', y=['Peak kWhs', 'Off Peak kWhs'], color_discrete_sequence=['coral', 'teal'])
    
    
    return fiscalYear, city, averageEnergyConsumption, averageGasEmission, peakEnergyConsumption, dataForBar, dataForPie, total_consumption_per_month, controlled_load_per_month, peak_and_off_peak_by_month, peak_and_off_peak_by_quarter