import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import altair as alt
import pydeck as pdk
import seaborn as sns
import plotly.express as px


DATE_TIME = "date/time"
DATA_URL = ("https://github.com/vinayakms221/market-analysis-streamlit/blob/master/datasets/indiat.csv"
)

def main():
    html_temp="""
    <div style="align:centre"><p style="color: red; font-size: 35px"><b>TERRORISM ATTACK IN INDIA</p></div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    st.sidebar.title("Analysis type")
    app_mode = st.sidebar.selectbox("Choose the analysis type",["Data Analysis", "Geographical Analysis"])
    if app_mode=="Data Analysis":
        data()
    else:
        graph()

@st.cache
def get_data():
    metadata=pd.read_csv("./datasets/indiat.csv")
    return metadata

@st.cache
def map_data():
    metadata=pd.read_csv("./datasets/map3.csv")
    return metadata

def graph():
    df=map_data()
    st.header("Graphical Analysis")
    st.header("")


    midpoint = (np.average(df["latitude"]), np.average(df["longitude"]))
    # df = df[df.latitude.notnull()]
    # df = df[df.longitude.notnull()]
    maptype=st.selectbox('select type of graph layer',["ScatterplotLayer","Number of Attacks", "Advanced Map"])
    if maptype=="ScatterplotLayer":
          st.subheader("The map plots the location of Places where attacks happened")
          st.write(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": midpoint[0],
                "longitude": midpoint[1],
                "zoom": 3,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position=["longitude", "latitude"],
                    #radius=100,
                    elevation_scale=4,
                    get_fill_color=[255, 0, 0, 100],
                    get_radius=20000,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        ))
    # elif maptype=="Number of Deaths" :
    #     st.write(pdk.Deck(
    #         map_style="mapbox://styles/mapbox/light-v9",
    #         initial_view_state={
    #             "latitude": midpoint[0],
    #             "longitude": midpoint[1],
    #             "zoom": 10.5,
    #             "pitch": 50,
    #         },
    #         layers=[
    #             pdk.Layer(
    #                 "ColumnLayer",
    #                 data=df,
    #                 get_position=["longitude", "latitude"],
    #                 radius=20000,
    #                 elevation_scale=100,
    #                 get_fill_color=[0, 255, 0, 100],
    #                 get_radius=20000,
    #                 getElevationValue= ["nkill"],
    #                 elevation_range=[0, 10000000],
    #                 pickable=True,
    #                 extruded=True,
    #             ),
    #         ],
    #     ))
    elif maptype=="Number of Attacks" :
        st.subheader("The map plots the location of Places where attacks happened and the height represents the frequency of attacks heppened in a particular coordinate values")
        st.write(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": midpoint[0],
                "longitude": midpoint[1],
                "zoom": 3,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=df,
                    get_position=["longitude", "latitude"],
                    radius=20000,
                    elevation_scale=2000,
                    get_fill_color=[255, 0, 0, 100],
                    get_radius=20000,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        ))
    
    elif maptype=="Advanced Map" :
        st.write(px.scatter_mapbox(df, lat="latitude", lon="longitude", color="attacktype1_txt",size="nkill",hover_name="city",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=1,
                  mapbox_style="carto-positron",title='Advanced Map'))


def data():
    #st.sidebar.header("choose analysis")
    unit=st.sidebar.selectbox("",["India","Global"])
    if unit=="India":
        fulldata()
    

def fulldata():
    df=get_data()
    st.header("Data analysis on Indian Terrorism Data")
    st.header("")
    st.subheader("Choose Which Analysis You Want To Make")
    analysis=st.selectbox("",['Per year terrorism activities','Attacking Type','Terrorist Groups','Attack Success Analysis'])
    
    
  
    if analysis=="Attack Success Analysis":
        plt.figure(figsize=(20,12))   
        plt.title("Percentage of Success vs Failure") 
        sns.set_style('darkgrid') 
        ax=sns.countplot(x ='iyear', hue = "success", data = df) 
        plt.show()
        plt.ylabel('Counts', fontsize=20)
        plt.xlabel('Year', fontsize=20)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.xticks(rotation=90)
        st.write(ax)
        st.pyplot()

    elif analysis=="Terrorist Groups":
        st.subheader("Terrorist Groups")
        st.header("")
        ptype=st.multiselect("Select Attack Group",['Sikh Extremists','Maoists','Naxalites','Lashkar-e-Taiba (LeT)','CPI-Maoist','ULFA','Hizbul Mujahideen (HM)','Muslim Separatists','Muslim Militants'])
        plottype=st.selectbox('select what you want to analyse',["Number of attacks","Number of Kills per Attack Type"])
        l= len(ptype)
        f=df['eventid'].copy()
        if l!=0:
            for i in range(l):
                d=df[df['gname'] ==ptype[i]]
                dd=pd.concat([f,d],axis=0)
                f=dd.copy()
            if (plottype=="Number of attacks"):
                plt.subplots(figsize=(18,14))
                abc=sns.countplot('gname',data=dd, palette='inferno',order=dd["gname"].value_counts().index)
                plt.xticks(rotation=30)
                plt.xticks(fontsize=12)
                plt.yticks(fontsize=16)
                plt.xlabel('Group Name', fontsize=18)
                plt.ylabel('Counts', fontsize=20)
                plt.title('Attacking methods by terrorist', fontsize=20)
                
                if st.button("Plot"):
                    st.write(abc)
                    st.pyplot()
            else:
                abc=px.pie(dd, values='nkill', names='gname', title='Number of Kills by each group')
                if st.button("Plot"):
                    st.write(abc)
                    st.pyplot()
        else:
            html_temp="""<div style="align:centre"><p style="color: red; font-size: 20px">*select any from Group</p></div>"""
            st.markdown(html_temp,unsafe_allow_html=True)

    elif analysis=="Attacking Type":
        st.subheader("Attacking Type")
        st.header("")
        ptype=st.multiselect("Select Attacking Type",['Bombing/Explosion','Armed Assault','Assassination','Hostage Taking (Kidnapping)','Facility/Infrastructure Attack','Unknown','Unarmed Assault','Hostage Taking (Barricade Incident)','Hijacking'])
        plottype=st.selectbox('select what you want to analyse',["Number of attacks","Number of Kills per Attack Type"])
        l= len(ptype)
        f=df['eventid'].copy()
        if l!=0:
            for i in range(l):
                d=df[df['attacktype1_txt'] ==ptype[i]]
                dd=pd.concat([f,d],axis=0)
                f=dd.copy()
            if (plottype=="Number of attacks"):
                plt.subplots(figsize=(18,14))
                abc=sns.countplot('attacktype1_txt',data=dd, palette='inferno',order=dd["attacktype1_txt"].value_counts().index)
                plt.xticks(rotation=30)
                plt.xticks(fontsize=12)
                plt.yticks(fontsize=16)
                # plt.xlabel('xlabel', fontsize=18)
                plt.ylabel('Counts', fontsize=20)
                plt.title('Attacking methods by terrorist', fontsize=20)
                
                if st.button("Plot"):
                    st.write(abc)
                    st.pyplot()
                
            else:
                abc=px.pie(dd, values='nkill', names='attacktype1_txt', title='Number of Kills per Attack Type')
                if st.button("Plot"):
                    st.write(abc)
                    st.pyplot()

            
        else:
            html_temp="""<div style="align:centre"><p style="color: red; font-size: 20px">*select any from Attacking Type</p></div>"""
            st.markdown(html_temp,unsafe_allow_html=True)
            
    else:
        st.subheader("Per year terrorism activities")
        st.header("")
        # st.subheader("Choose Which Analysis You Want To Make")
        plottype=st.selectbox('select Plot Type',["Bar Plot","Distribution Plot", "Line Plot"])
        year = st.slider("select year", 1972, 2017, 2017)
        dd=df[(df.iyear >= 1972) & (df.iyear <= year)]
        if (plottype=="Bar Plot"):
            plt.subplots(figsize=(20,12))
            cust_plot= sns.countplot('iyear',data=dd)
            sns.set_style('darkgrid')
            plt.xticks(rotation=90)
            plt.title('Number of terrorist Activities each year', fontsize=25)
            plt.ylabel('Counts', fontsize=20)
            plt.xlabel('Year', fontsize=20)
            plt.xticks(fontsize=16)
            plt.yticks(fontsize=16)
            # if st.button("Plot"):
            st.write(cust_plot)
            st.pyplot()
        elif (plottype=="Distribution Plot"):
            plt.subplots(figsize=(20,12))
            fig = sns.distplot(dd["iyear"].values, color = 'r')
            plt.title('Number of terrorist Activities each year', fontsize=25)
            plt.ylabel('Counts', fontsize=20)
            plt.xlabel('Year', fontsize=20)
            plt.xticks(fontsize=16)
            plt.yticks(fontsize=16)
            st.write(fig)
            st.pyplot()
        elif (plottype=="Line Plot"):
            year = dd['eventid'].groupby(dd['iyear']).count()
            plt.subplots(figsize=(20,12))
            ax = sns.lineplot(data=year)
            plt.title('Number of terrorist Activities each year', fontsize=25)
            plt.ylabel('Counts', fontsize=20)
            plt.xlabel('Year', fontsize=20)
            plt.xticks(fontsize=16)
            plt.yticks(fontsize=16)
            st.write(ax)
            st.pyplot()
@st.cache
def dataA():
    data=get_data()
    metadata=data[data['Branch']=="A"]
    return metadata
@st.cache
def dataB():
    data=get_data()
    metadata=data[data['Branch']=="B"]
    return metadata
@st.cache
def dataC():
    data=get_data()
    metadata=data[data['Branch']=="C"]
    return metadata


    

if __name__=='__main__':
    main()
