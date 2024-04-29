import streamlit as st
import pandas as pd
import numpy as np
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
from bs4 import Comment
from PIL import Image
import requests
import re
import plotly as py
import plotly.graph_objects as go
import plotly.express as px
import altair as alt

st.set_page_config(page_title='MLB Analysis', page_icon=':baseball:',layout="wide")

image = Image.open(r"Projects/app_1_MLB_eda/mlb-logo.png")
st.image(image, use_column_width=True)

st.title('MLB Regular Season Stats Explorer')

st.markdown("""
This app performs webscraping and analysis of MLB player stats data!
* **Python libraries:** Streamlit, Pandas, NumPy, BeautifulSoup, Requests, base64, Matplotlib, Seaborn, and PIL
* **Data source:** [Baseball-reference.com](https://www.baseball-reference.com/)
""")
# st.header('Display Player Stats of Selected Team')
tab1, tab2 = st.tabs(["Hitting", "Pitching"])

st.sidebar.title('User Input Features')
selected_year = st.sidebar.selectbox('Select Year', list(reversed(range(1998,2025))))

################### Web scraping of MLB player stats ##########################
# Hitting Stats #
with tab1:
    if selected_year == 2024 : 
        def hit_data(current_year):
            url = "https://www.baseball-reference.com/leagues/majors/2024-standard-batting.shtml"
            r = requests.get(url).text
            stats_page = BeautifulSoup(r,'lxml')
            comment = stats_page.find_all(text=lambda text:isinstance(text, Comment))
            str1 = ''.join(comment)
            test1 = BeautifulSoup(str1,'lxml')
            data = pd.read_html(str(test1))
            df = pd.DataFrame(data[0])
            df.drop(['Rk'],axis=1, inplace=True) #'Pos\xa0Summary'
            df.drop(df.tail(1).index,inplace=True)
            df.drop_duplicates(keep=False,inplace=True)
            col = (['Age','G','PA','AB','R','H','2B','3B','HR','RBI','SB','CS','BB','SO','BA','OBP','SLG','OPS','OPS+','TB','GDP','HBP','SH','SF','IBB'])
            for x in col:
                df[x] = pd.to_numeric(df[x])
            df = df[df.Tm != 'TOT']
            df = df.rename(columns={'Pos\xa0Summary': 'Pos'})
            column_to_move = df.pop('Pos')
            df.insert(3, 'Pos', column_to_move)
            df['Pos'] = df['Pos'].str.extract('(\d)', expand=False)
            df['Pos'] = df['Pos'].fillna('DH')
            positions = {'1':'P', '2':'C', '3':'1B', '4':'2B', '5':'3B', '6':'SS', '7':'LF', '8':'CF', '9':'RF'}
            df['Pos'] = df['Pos'].replace(positions)
            df['Pos'] = df['Pos'].astype(str)
            df['Name'] = df['Name'].apply(lambda x: str(x).replace(u'\xa0', u' '))
            df['Name'] = df['Name'].map(lambda x: x.rstrip('*#'))
            df = df.reset_index(drop=True)
            hit_stats = df.set_index('Name')
            return hit_stats
    else :
        @st.cache_data
        def hit_data(year):
            url = "https://www.baseball-reference.com/leagues/majors/" + str(year) + "-standard-batting.shtml"
            r = requests.get(url).text
            stats_page = BeautifulSoup(r,'lxml')
            comment = stats_page.find_all(text=lambda text:isinstance(text, Comment))
            str1 = ''.join(comment)
            test1 = BeautifulSoup(str1,'lxml')
            data = pd.read_html(str(test1))
            df = pd.DataFrame(data[0])
            df.drop(['Rk'],axis=1, inplace=True) #,'Pos\xa0Summary'
            df.drop(df.tail(1).index,inplace=True)
            df.drop_duplicates(keep=False,inplace=True)
            col = (['Age','G','PA','AB','R','H','2B','3B','HR','RBI','SB','CS','BB','SO','BA','OBP','SLG','OPS','OPS+','TB','GDP','HBP','SH','SF','IBB'])
            for x in col:
                df[x] = pd.to_numeric(df[x])
            df = df[df.Tm != 'TOT']
            df = df.rename(columns={'Pos\xa0Summary': 'Pos'})
            column_to_move = df.pop('Pos')
            df.insert(3, 'Pos', column_to_move)
            df['Pos'] = df['Pos'].str.extract('(\d)', expand=False)
            df['Pos'] = df['Pos'].fillna('DH')
            positions = {'1':'P', '2':'C', '3':'1B', '4':'2B', '5':'3B', '6':'SS', '7':'LF', '8':'CF', '9':'RF'}
            df['Pos'] = df['Pos'].replace(positions)
            df['Pos'] = df['Pos'].astype(str)
            df['Name'] = df['Name'].apply(lambda x: str(x).replace(u'\xa0', u' '))
            df['Name'] = df['Name'].map(lambda x: x.rstrip('*#'))
            df = df.reset_index(drop=True)
            hit_stats = df.set_index('Name')
            return hit_stats
    hit_stats = hit_data(selected_year)

# Pitching Stats #
with tab2:
    if selected_year == 2024 : 
        def pitch_data(year):
            url = "https://www.baseball-reference.com/leagues/majors/" + str(year) + "-standard-pitching.shtml"
            r = requests.get(url).text
            stats_page = BeautifulSoup(r,'lxml')
            comment = stats_page.find_all(text=lambda text:isinstance(text, Comment))
            str1 = ''.join(comment)
            test1 = BeautifulSoup(str1,'lxml')
            data = pd.read_html(str(test1))
            df = pd.DataFrame(data[0])
            df.drop(['Rk'], axis=1, inplace=True)
            df.drop(df.tail(1).index,inplace=True)
            df.drop_duplicates(keep=False,inplace=True)
            col = (['Age','W','L','W-L%','ERA','G','GS','GF','CG','SHO','SV','IP','H','R','ER','HR','BB','IBB','SO','HBP','BK','WP','BF','ERA+','FIP', 'WHIP','H9','HR9','BB9','SO9','SO/W'])
            for x in col:
                df[x] = pd.to_numeric(df[x])
            df = df[df.Tm != 'TOT']
            df['Name'] = df['Name'].apply(lambda x: str(x).replace(u'\xa0', u' '))
            df['Name'] = df['Name'].map(lambda x: x.rstrip('*#'))
            #df = df.reset_index(drop=True)
            pitch_stats = df.set_index('Name')
            return pitch_stats
    else :
        @st.cache_data
        def pitch_data(year):
            url = "https://www.baseball-reference.com/leagues/majors/" + str(year) + "-standard-pitching.shtml"
            r = requests.get(url).text
            stats_page = BeautifulSoup(r,'lxml')
            comment = stats_page.find_all(text=lambda text:isinstance(text, Comment))
            str1 = ''.join(comment)
            test1 = BeautifulSoup(str1,'lxml')
            data = pd.read_html(str(test1))
            df = pd.DataFrame(data[0])
            df.drop(['Rk'], axis=1, inplace=True)
            df.drop(df.tail(1).index,inplace=True)
            df.drop_duplicates(keep=False,inplace=True)
            col = (['Age','W','L','W-L%','ERA','G','GS','GF','CG','SHO','SV','IP','H','R','ER','HR','BB','IBB','SO','HBP','BK','WP','BF','ERA+','FIP', 'WHIP','H9','HR9','BB9','SO9','SO/W'])
            for x in col:
                df[x] = pd.to_numeric(df[x])
            df = df[df.Tm != 'TOT']
            df['Name'] = df['Name'].apply(lambda x: str(x).replace(u'\xa0', u' '))
            df['Name'] = df['Name'].map(lambda x: x.rstrip('*#'))
            #df = df.reset_index(drop=True)
            pitch_stats = df.set_index('Name')
            return pitch_stats
    pitch_stats = pitch_data(selected_year)


#Sidebar - Team selection
data = [hit_stats, pitch_stats]
mlb_df = pd.concat(data)

unique_team = sorted(mlb_df.Tm.unique())
unique_pos = mlb_df['Pos'].dropna().unique()

###########  team filter
selected_team = st.sidebar.multiselect('Select Team(s)', unique_team)

if 'include_all_teams_checked' not in st.session_state:
    st.session_state.include_all_teams_checked = True

# Update include_all_teams based on the selection of teams
if len(selected_team) > 0:
    st.session_state.include_all_teams_checked = False
else:
    st.session_state.include_all_teams_checked = True

# Render the "Select all" checkbox using the session state
include_all_teams = st.sidebar.checkbox('Select all', value=st.session_state.include_all_teams_checked)

# ##########    position filter
sorted_positions = ['P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'DH']
selected_position = st.sidebar.multiselect('Select Position(s)', sorted_positions)

# Manage session state for the "Select all" checkbox for positions
if 'include_all_positions_checked' not in st.session_state:
    st.session_state.include_all_positions_checked = True

# Update include_all_positions_checked based on the selection of positions
if len(selected_position) > 0:
    st.session_state.include_all_positions_checked = False
else:
    st.session_state.include_all_positions_checked = True

# Render the "Select all" checkbox for positions using the session state
include_all_positions = st.sidebar.checkbox('Select all', key='pos', value=st.session_state.include_all_positions_checked)
################### data filter for each tab #####################

# hitting tab #

if include_all_teams and include_all_positions:
    hit_selected_team = hit_stats  # No filtering
elif include_all_teams:
    hit_selected_team = hit_stats[hit_stats['Pos'].isin(selected_position)]
elif include_all_positions:
    hit_selected_team = hit_stats[hit_stats['Tm'].isin(selected_team)]
else:
    # Filter based on both selected team(s) and selected position(s)
    hit_selected_team = hit_stats[(hit_stats['Tm'].isin(selected_team)) & (hit_stats['Pos'].isin(selected_position))]


# pitching tab #

if include_all_teams:
    pitch_selected_team = pitch_stats
else:
    pitch_selected_team = pitch_stats[pitch_stats['Tm'].isin(selected_team)]

##################### Data Display for hitting tab ############################
with tab1:
        if not include_all_teams :
            st.header(f'''{str(selected_team[:]).replace("[", "").replace("]", "").replace("'","")} Team Leaders, ''' f'{(selected_year)}''')
        else :
            st.header('League Leaders, 'f'{(selected_year)}')

        if selected_year == 2020:
            st.markdown('''
            * Due to the COVID-19 pandemic, a shortened season of just 60 games was played in 2020.
            * 'Select all' for both filters will show ranking-qualified league leaders for each stat.
            * A hitter qualifies for stat-ranking, when he averages 3.1 plate appearances per team game (186 PA's total for 2020).
            * Selecting a team(s) and/or position(s) will show up to the top 5 qualified players in that team/position for each category.
            ''')
        elif selected_year == 2024:
            st.markdown('''
            * 'Select all' for both filters will show ranking-qualified league leaders for each stat.
            * A hitter qualifies for stat-ranking, when he averages 3.1 plate appearances per team game (502 PA's over a full 162-game season).
            * Selecting a team(s) and/or position(s) will show up to the top 5 players in that team/position for each category using the least-amount of team games played so far as the qualifier.
            ''')
        else:
            st.markdown('''
            * 'Select all' for both filters will show ranking-qualified league leaders for each stat.
            * A hitter qualifies for stat-ranking, when he averages 3.1 plate appearances per team game (502 PA's over a full 162-game season).
            * Selecting a team(s) and/or position(s) will show up to the top 5 players in that team/position for each category with atleast 400 PA.
            ''')
        hit_selected_team.to_csv('output.csv',index=False)
        df = pd.read_csv('output.csv')
# averages among ranking-qualified hitters across the MLB # (min.502 PA, min. 186 PA for shortened 2020 Season)
        if (selected_year == 2024):
            qualifier = hit_stats[hit_stats['PA']>=74]
            qualified = pd.DataFrame(qualifier.mean())
            qualified.columns=['League Average per Hitter']
            team = hit_selected_team[hit_selected_team['PA']>=74]
            team_qualified = pd.DataFrame(team.mean())
            team_qualified.columns=[''f'{selected_team} ' 'Average per Hitter']
        elif (selected_year == 2020) :
            qualifier = hit_stats[hit_stats['PA']>=186]
            qualified = pd.DataFrame(qualifier.mean())
            qualified.columns=['League Average per Hitter']
            team = hit_selected_team[hit_selected_team['PA']>=186]
            team_qualified = pd.DataFrame(team.mean())
            team_qualified.columns=[''f'{selected_team} ' 'Average per Hitter']
        else :
            qualifier = hit_stats[hit_stats['PA']>=502]
            qualified = pd.DataFrame(qualifier.mean())
            qualified.columns=['League Average per Hitter']
            team = hit_selected_team[hit_selected_team['PA']>=502]
            team_qualified = pd.DataFrame(team.mean())
            team_qualified.columns=[''f'{selected_team} ' 'Average per Hitter']
# league avg vs. team average amongst qualified hitters #
        compare = qualified.join(team_qualified)

# function for downloadable dataframe
        def filedownload(df):
         csv = df.to_csv(index=True)
         b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
         href = f'<a href="data:file/csv;base64,{b64}" download="{", ".join(selected_position)} @ {", ".join(selected_team)}-{selected_year}_hit_stats.csv">Download CSV File</a>'
         return href  

        if hit_selected_team is not None :
            with st.expander('CLICK HERE FOR DOWNLOADABLE DATAFRAME FOR ' + ' , '.join(selected_position) + ' - ' + ' , '.join(selected_team) + ' - ' + str(selected_year)) :
                st.write('Data Dimension: ' + str(hit_selected_team.shape[0]) + ' rows and ' + str(hit_selected_team.shape[1]) + ' columns.')
                st.markdown(filedownload(hit_selected_team), unsafe_allow_html=True)    
                st.dataframe(hit_selected_team)
        else :
            with st.expander('CLICK HERE FOR DOWNLOADABLE MLB DATAFRAME FOR'  f'{(selected_year)}') :
                st.write('Data Dimension: ' + str(hit_stats(selected_year).shape[0]) + ' rows and ' + str(hit_stats(selected_year).shape[1]) + ' columns.')
                st.markdown(filedownload(selected_year), unsafe_allow_html=True)    
                st.dataframe(hit_stats(selected_year))  

        with st.expander('CLICK HERE TO SEE LEAGUE AVERAGE STATS FOR '  f'{(selected_year)}') :
            st.write('''Stats shown are average among players who qualify for ranking in the year and team selected.''')
            with st.container() :
                    st.table(qualified)

        st.set_option('deprecation.showPyplotGlobalUse', False) #ignore deprecation warning

        c1, c2, c3 = st.columns(3)
        with c1 :
            st.header("AVG")
            if include_all_teams == True :
                ba_sorted = team.reset_index().nlargest(10, 'BA')
                ba_fig = px.bar(
                    ba_sorted,
                    x = 'BA',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','BA','Tm', 'Pos', 'PA']
                )
                ba_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                ba_fig.update_xaxes(visible=False)
                ba_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(ba_fig)
            else :
                # team = hit_selected_team[hit_selected_team['PA']>=400]
                ba_sorted = team.reset_index().nlargest(5, 'BA')
                ba_fig = px.bar(
                    ba_sorted,
                    x = 'BA',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','BA', 'Tm', 'Pos', 'PA']
                )
                ba_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                ba_fig.update_xaxes(visible=False)
                ba_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(ba_fig)

            st.header("SLG")
            if include_all_teams == True :
                slg_sorted = team.reset_index().nlargest(10, 'SLG')
                slg_fig = px.bar(
                    slg_sorted,
                    x = 'SLG',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','SLG','Tm', 'Pos', 'PA']
                )
                slg_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                slg_fig.update_xaxes(visible=False)
                slg_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(slg_fig)
                # st.bar_chart(team['RBI'].nlargest(10))
                # st.bar_chart(team['OPS+'].nlargest(10))
            else :
                # team = hit_selected_team[hit_selected_team['PA']>=400]
                slg_sorted = team.reset_index().nlargest(5, 'SLG')
                slg_fig = px.bar(
                    slg_sorted,
                    x = 'SLG',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','SLG', 'Tm', 'Pos', 'PA']
                )
                slg_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                slg_fig.update_xaxes(visible=False)
                slg_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(slg_fig)

            st.header("Homeruns")
            if include_all_teams == True :
                hr_sorted = team.reset_index().nlargest(10, 'HR')
                hr_fig = px.bar(
                    hr_sorted,
                    x = 'HR',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','HR','Tm', 'Pos', 'PA']
                )
                hr_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                hr_fig.update_xaxes(visible=False)
                hr_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(hr_fig)
            else :
                hr_sorted = team.reset_index().nlargest(5, 'HR')
                hr_fig = px.bar(
                    hr_sorted,
                    x = 'HR',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','HR', 'Tm', 'Pos', 'PA']
                )
                hr_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                hr_fig.update_xaxes(visible=False)
                hr_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(hr_fig)

            st.header("Runs")
            if include_all_teams == True :
                r_sorted = team.reset_index().nlargest(10, 'R')
                r_fig = px.bar(
                    r_sorted,
                    x = 'R',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','R','Tm',  'Pos','PA']
                )
                r_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                r_fig.update_xaxes(visible=False)
                r_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(r_fig)
            else :
                # team = hit_selected_team[hit_selected_team['PA']>=400]
                r_sorted = team.reset_index().nlargest(5, 'R')
                r_fig = px.bar(
                    r_sorted,
                    x = 'R',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','R', 'Tm', 'Pos', 'PA']
                )
                r_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                r_fig.update_xaxes(visible=False)
                r_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(r_fig)

        with c3 :
            st.header("OBP")
            if include_all_teams == True :
                obp_sorted = team.reset_index().nlargest(10, 'OBP')
                obp_fig = px.bar(
                    obp_sorted,
                    x = 'OBP',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','OBP','Tm', 'Pos', 'PA']
                )
                obp_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                obp_fig.update_xaxes(visible=False)
                obp_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(obp_fig)
            else :
                # team = hit_selected_team[hit_selected_team['PA']>=400]
                obp_sorted = team.reset_index().nlargest(5, 'OBP')
                obp_fig = px.bar(
                    obp_sorted,
                    x = 'OBP',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','OBP', 'Tm', 'Pos', 'PA']
                )
                obp_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                obp_fig.update_xaxes(visible=False)
                obp_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(obp_fig)

            st.header("OPS")
            if include_all_teams == True :
                ops_sorted = team.reset_index().nlargest(10, 'OPS')
                ops_fig = px.bar(
                    ops_sorted,
                    x = 'OPS',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','OPS','Tm', 'Pos', 'PA']
                )
                ops_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                ops_fig.update_xaxes(visible=False)
                ops_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(ops_fig)
            else :
                ops_sorted = team.reset_index().nlargest(5, 'OPS')
                ops_fig = px.bar(
                    ops_sorted,
                    x = 'OPS',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','OPS', 'Tm', 'Pos', 'PA']
                )
                ops_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                ops_fig.update_xaxes(visible=False)
                ops_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(ops_fig)    

            st.header("Hits")
            if include_all_teams == True :
                hit_sorted = team.reset_index().nlargest(10, 'H')
                hit_fig = px.bar(
                    hit_sorted,
                    x = 'H',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','H','Tm', 'Pos', 'PA']
                )
                hit_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                hit_fig.update_xaxes(visible=False)
                hit_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(hit_fig)
            else :
                hit_sorted = team.reset_index().nlargest(5, 'RBI')
                hit_fig = px.bar(
                    hit_sorted,
                    x = 'RBI',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','RBI', 'Tm', 'Pos', 'PA']
                )
                hit_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                hit_fig.update_xaxes(visible=False)
                hit_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(hit_fig)

            st.header("RBI")
            if include_all_teams == True :
                rbi_sorted = team.reset_index().nlargest(10, 'RBI')
                rbi_fig = px.bar(
                    rbi_sorted,
                    x = 'RBI',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','RBI','Tm', 'Pos','PA']
                )
                rbi_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                rbi_fig.update_xaxes(visible=False)
                rbi_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(rbi_fig)
            else :
                rbi_sorted = team.reset_index().nlargest(5, 'RBI')
                rbi_fig = px.bar(
                    rbi_sorted,
                    x = 'RBI',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','RBI', 'Tm',  'Pos','PA']
                )
                rbi_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                rbi_fig.update_xaxes(visible=False)
                rbi_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(rbi_fig)
                
###############################################################################
###############################################################################
###############################################################################

####################### Data Display for pitching tab #########################           
with tab2:
        def filedownload_pitch(df):
         csv = df.to_csv(index=True)
         b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
         href = f'<a href="data:file/csv;base64,{b64}" download="{", ".join(selected_team)}-{selected_year}_pitch_stats.csv">Download CSV File</a>'
         return href 
        
    # if st.button('Exploratory Analysis', key='pitch'):
        if not include_all_teams :
            st.header(f'''{str(selected_team[:]).replace("[", "").replace("]", "").replace("'","")} Team Leaders, ''' f'{(selected_year)}''')
        else :
            st.header('League Leaders, 'f'{(selected_year)}')

        if selected_year == 2020 :
            st.markdown('''
            * Due to the COVID-19 pandemic, a shortened season of just 60 games was played.
            * 'Select all' will show ranking-qualified league leaders for each stat.
            * A pitcher qualifies for stat-ranking, when he averages 1 inning per team game (60 IP total for 2020).
            * Selecting a team(s) will show up to the top 5 qualified pitchers in that team for each category.
            ''')
        elif selected_year == 2024:
            st.markdown('''
            * 'Select all' will show ranking-qualified league leaders for each stat.
            * A pitcher qualifies for stat-ranking, when he averages 1 inning per team game (162 IP over a full 162-game season).
            * Selecting a team(s) will show up to the top 5 players in that team for each category using the least-amount of team games played so far as the qualifier
            ''')
        else:
            st.markdown('''
            * 'Select all' will show ranking-qualified league leaders for each stat.
            * A pitcher qualifies for stat-ranking, when he averages 1 inning per team game (162 IP over a full 162-game season).
            * Selecting a team(s) will show up to the top 5 players in that team for each category with atleast 100 IP.
            ''')
        pitch_selected_team.to_csv('output.csv',index=False)
        df = pd.read_csv('output.csv')
# averages among ranking-qualified pitchers across the MLB # (min.162 IP)
        if selected_year == 2024 :
            p_qualifier = pitch_stats[pitch_stats['IP']>=24]
            p_qualified = pd.DataFrame(p_qualifier.mean())
            p_qualified.columns=['League Average per Pitcher']
            p_team = pitch_selected_team[pitch_selected_team['IP']>=24]
            p_team_qualified = pd.DataFrame(p_team.mean())
            p_team_qualified.columns=[''f'{selected_team} ' 'Average per Pitcher']
        elif selected_year == 2020 :
            p_qualifier = pitch_stats[pitch_stats['IP']>=60]
            p_qualified = pd.DataFrame(p_qualifier.mean())
            p_qualified.columns=['League Average per Pitcher']
            p_team = pitch_selected_team[pitch_selected_team['IP']>=60]
            p_team_qualified = pd.DataFrame(p_team.mean())
            p_team_qualified.columns=[''f'{selected_team} ' 'Average per Pitcher']
        else :
            p_qualifier = pitch_stats[pitch_stats['IP']>=162]
            p_qualified = pd.DataFrame(p_qualifier.mean())
            p_qualified.columns=['League Average per Pitcher']
            p_team = pitch_selected_team[pitch_selected_team['IP']>=162]
            p_team_qualified = pd.DataFrame(p_team.mean())
            p_team_qualified.columns=[''f'{selected_team} ' 'Average per Pitcher']
 # league avg vs. team average amongst qualified pitchers #
        p_compare = p_qualified.join(p_team_qualified)

        if pitch_selected_team is not None :
            with st.expander('CLICK HERE FOR DOWNLOADABLE DATAFRAME FOR ' + ' , '.join(selected_team) + ' - ' + str(selected_year)) :
                st.write('Data Dimension: ' + str(hit_selected_team.shape[0]) + ' rows and ' + str(hit_selected_team.shape[1]) + ' columns.')
                st.markdown(filedownload_pitch(hit_selected_team), unsafe_allow_html=True)    
                st.dataframe(pitch_selected_team)
        else :
            with st.expander('CLICK HERE FOR DOWNLOADABLE MLB DATAFRAME FOR'  f'{(selected_year)}') :
                st.write('Data Dimension: ' + str(hit_stats(selected_year).shape[0]) + ' rows and ' + str(hit_stats(selected_year).shape[1]) + ' columns.')
                st.markdown(filedownload(selected_year), unsafe_allow_html=True)    
                st.dataframe(pitch_selected_team_stats(selected_year))  


        with st.expander('CLICK HERE TO SEE LEAGUE AVERAGE STATS FOR '  f'{(selected_year)}') :
            st.write('''Stats shown are average among players who qualify for ranking in the year and team selected.''')
            with st.container() :
                    st.table(p_qualified)

        st.set_option('deprecation.showPyplotGlobalUse', False)#ignore deprecation warning

        c1, c2, c3 = st.columns(3)
        with c1 :
            st.header("ERA")
            if include_all_teams == True :
                era_sorted = p_team.reset_index().nsmallest(10, 'ERA')
                era_fig = px.bar(
                    era_sorted,
                    x = 'ERA',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','ERA','Tm', 'GS']
                )
                era_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                era_fig.update_xaxes(visible=False)
                era_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total descending'})
                st.plotly_chart(era_fig)
            else :
                era_sorted = p_team.reset_index().nsmallest(5, 'ERA')
                era_fig = px.bar(
                    era_sorted,
                    x = 'ERA',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','ERA', 'Tm', 'GS']
                )
                era_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                era_fig.update_xaxes(visible=False)
                era_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total descending'})
                st.plotly_chart(era_fig)

            st.header("Strikeouts")
            if include_all_teams == True :
                # p_team = pitch_selected_team[pitch_selected_team['IP']>=162]
                so_sorted = p_team.reset_index().nlargest(10, 'SO')
                so_fig = px.bar(
                    so_sorted,
                    x = 'SO',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','SO','Tm', 'IP']
                )
                so_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                so_fig.update_xaxes(visible=False)
                so_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(so_fig)
                # st.bar_chart(team['RBI'].nlargest(10))
                # st.bar_chart(team['OPS+'].nlargest(10))
            else :
                # p_team = pitch_selected_team[pitch_selected_team['IP']>=100]
                so_sorted = p_team.reset_index().nlargest(5, 'SO')
                so_fig = px.bar(
                    so_sorted,
                    x = 'SO',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','SO', 'Tm', 'IP']
                )
                so_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                so_fig.update_xaxes(visible=False)
                so_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(so_fig)

            st.header("Walks")
            if include_all_teams == True :
                # p_team = pitch_selected_team[pitch_selected_team['IP']>=162]
                w_sorted = p_team.reset_index().nsmallest(10, 'BB')
                w_fig = px.bar(
                    w_sorted,
                    x = 'BB',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','BB','Tm', 'IP']
                )
                w_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                w_fig.update_xaxes(visible=False)
                w_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total descending'})
                st.plotly_chart(w_fig)
                # st.bar_chart(team['RBI'].nlargest(10))
                # st.bar_chart(team['OPS+'].nlargest(10))
            else :
                # p_team = pitch_selected_team[pitch_selected_team['IP']>=100]
                w_sorted = p_team.reset_index().nsmallest(5, 'BB')
                w_fig = px.bar(
                    w_sorted,
                    x = 'BB',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','BB', 'Tm', 'IP']
                )
                w_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                w_fig.update_xaxes(visible=False)
                w_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total descending'})
                st.plotly_chart(w_fig)

            st.header("Saves")
            if include_all_teams == True :
                p_team = pitch_selected_team[pitch_selected_team['IP']>=1]
                sv_sorted = p_team.reset_index().nlargest(10, 'SV')
                sv_fig = px.bar(
                    sv_sorted,
                    x = 'SV',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','SV','Tm', 'IP']
                )
                sv_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                sv_fig.update_xaxes(visible=False)
                sv_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(sv_fig)
            else :
                p_team = pitch_selected_team[pitch_selected_team['IP']>=1]
                sv_sorted = p_team.reset_index().nlargest(5, 'SV')
                sv_fig = px.bar(
                    sv_sorted,
                    x = 'SV',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','SV', 'Tm', 'IP']
                )
                sv_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                sv_fig.update_xaxes(visible=False)
                sv_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(sv_fig)

        with c3:
            st.header("Innings Pitched")
            if include_all_teams == True :
                # p_team = pitch_selected_team[pitch_selected_team['IP']>=162]
                ip_sorted = p_team.reset_index().nlargest(10, 'IP')
                ip_fig = px.bar(
                    ip_sorted,
                    x = 'IP',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','IP', 'Tm']
                )
                ip_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                ip_fig.update_xaxes(visible=False)
                ip_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(ip_fig)
            else :
                # p_team = pitch_selected_team[pitch_selected_team['IP']>=100]
                era_sorted = p_team.reset_index().nlargest(5, 'IP')
                era_fig = px.bar(
                    era_sorted,
                    x = 'IP',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name', 'IP', 'Tm']
                )
                era_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                era_fig.update_xaxes(visible=False)
                era_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(era_fig)
            
            st.header("Hits Allowed")
            if include_all_teams == True :
                # p_team = pitch_selected_team[pitch_selected_team['IP']>=162]
                ha_sorted = p_team.reset_index().nsmallest(10, 'H')
                ha_fig = px.bar(
                    era_sorted,
                    x = 'H',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','H','Tm', 'IP']
                )
                ha_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                ha_fig.update_xaxes(visible=False)
                ha_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total descending'})
                st.plotly_chart(ha_fig)
                # st.bar_chart(team['RBI'].nlargest(10))
                # st.bar_chart(team['OPS+'].nlargest(10))
            else :
                # p_team = pitch_selected_team[pitch_selected_team['IP']>=100]
                ha_sorted = p_team.reset_index().nsmallest(5, 'H')
                ha_fig = px.bar(
                    ha_sorted,
                    x = 'H',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','H', 'Tm', 'IP']
                )
                ha_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                ha_fig.update_xaxes(visible=False)
                ha_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total descending'})
                st.plotly_chart(ha_fig)

            st.header("WHIP")
            if include_all_teams == True :
                # p_team = pitch_selected_team[pitch_selected_team['IP']>=162]
                whip_sorted = p_team.reset_index().nsmallest(10, 'WHIP')
                whip_fig = px.bar(
                    era_sorted,
                    x = 'WHIP',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','WHIP','Tm']
                )
                whip_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                whip_fig.update_xaxes(visible=False)
                whip_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total descending'})
                st.plotly_chart(whip_fig)
                # st.bar_chart(team['RBI'].nlargest(10))
                # st.bar_chart(team['OPS+'].nlargest(10))
            else :
                # p_team = pitch_selected_team[pitch_selected_team['IP']>=100]
                whip_sorted = p_team.reset_index().nsmallest(5, 'WHIP')
                whip_fig = px.bar(
                    whip_sorted,
                    x = 'WHIP',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','WHIP', 'Tm']
                )
                whip_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                whip_fig.update_xaxes(visible=False)
                whip_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total descending'})
                st.plotly_chart(whip_fig)

            st.header("SO/9 (Starters)")
            if include_all_teams == True :
                p_team = pitch_selected_team[pitch_selected_team['IP']>=24]
                SO9_sorted = p_team.reset_index().nlargest(10, 'SO9')
                SO9_fig = px.bar(
                SO9_sorted,
                    x = 'SO9',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','SO9','Tm', 'IP']
                )
                SO9_fig.update_traces(textfont_size=11, texttemplate='<b>%{x}</b>')
                SO9_fig.update_xaxes(visible=False)
                SO9_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(SO9_fig)
                # st.bar_chart(team['RBI'].nlargest(10))
                # st.bar_chart(team['OPS+'].nlargest(10))
            else :
                p_team = pitch_selected_team[pitch_selected_team['IP']>=24]
                SO9_sorted = p_team.reset_index().nlargest(5, 'SO9')
                SO9_fig = px.bar(
                    SO9_sorted,
                    x = 'SO9',
                    y = 'Name',
                    text_auto = True,
                    height = 400,
                    width = 400,
                    hover_data=['Name','SO9', 'Tm', 'IP']
                )
                SO9_fig.update_traces(textfont_size=12, texttemplate='<b>%{x}</b>')
                SO9_fig.update_xaxes(visible=False)
                SO9_fig.update_layout(
                    yaxis_title=None, 
                    xaxis_title=None,
                    yaxis = {'categoryorder':'total ascending'})
                st.plotly_chart(SO9_fig)
