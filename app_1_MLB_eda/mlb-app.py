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
import datetime

st.set_page_config(page_title='MLB Analysis', page_icon=':baseball:',layout="wide")

image = Image.open(r"app_1_MLB_eda/mlb-logo.png")
st.image(image, use_column_width=True)

st.title('MLB Regular Season Stats Explorer')

st.markdown("""
This app performs webscraping and analysis of MLB player stats data!
* **Python libraries:** Streamlit, Pandas, NumPy, BeautifulSoup, Requests, base64, Matplotlib, Seaborn, and PIL
* **Data source:** [Baseball-reference.com](https://www.baseball-reference.com/)
""")
st.header('Display Player Stats of Selected Team')
tab1, tab2 = st.tabs(["Hitting", "Pitching"])

st.sidebar.title('User Input Features')
selected_year = st.sidebar.selectbox('Select Year', list(reversed(range(1998,2024))))

################### Web scraping of MLB player stats ##########################
# Hitting Stats #
with tab1:
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
        df.drop(['Rk','Pos\xa0Summary'],axis=1, inplace=True)
        df.drop(df.tail(1).index,inplace=True)
        df.drop_duplicates(keep=False,inplace=True)
        col = (['Age','G','PA','AB','R','H','2B','3B','HR','RBI','SB','CS','BB','SO','BA','OBP','SLG','OPS','OPS+','TB','GDP','HBP','SH','SF','IBB'])
        for x in col:
            df[x] = pd.to_numeric(df[x])
        df = df[df.Tm != 'TOT']
        df['Name'] = df['Name'].apply(lambda x: str(x).replace(u'\xa0', u' '))
        df['Name'] = df['Name'].map(lambda x: x.rstrip('*#'))
        df = df.reset_index(drop=True)
        hit_stats = df.set_index('Name')
        return hit_stats
    hit_stats = hit_data(selected_year)

# Pitching Stats #
with tab2:
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

selected_team = st.sidebar.selectbox('Select Team', [None] + unique_team)

################### data filter for each tab #####################
# hitting tab #
if selected_team is None :
    hit_selected_team = hit_stats
else:
    hit_selected_team = hit_stats[(hit_stats.Tm == selected_team)]

# pitching tab #
if selected_team is None :
    pitch_selected_team = pitch_stats
else :
    pitch_selected_team = pitch_stats[(pitch_stats.Tm == selected_team)]

##################### Data Display for hitting tab ############################
with tab1 :
    if hit_selected_team is not None :
        st.write('Data Dimension: ' + str(hit_selected_team.shape[0]) + ' rows and ' + str(hit_selected_team.shape[1]) + ' columns.')
        st.dataframe(hit_selected_team)
    else :
        st.write('Data Dimension: ' + str(hit_stats(selected_year).shape[0]) + ' rows and ' + str(hit_stats(selected_year).shape[1]) + ' columns.')
        st.dataframe(hit_stats(selected_year))

    def filedownload(df):
         csv = df.to_csv(index=True)
         b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
         href = f'<a href="data:file/csv;base64,{b64}" download="hitter-stats.csv">Download CSV File</a>'
         return href
    st.markdown(filedownload(hit_selected_team), unsafe_allow_html=True)
################# Exploratory Analysis Button for hitting tab ##################
with tab1:
    if st.button('Exploratory Analysis', key='hit'):
        if selected_team is not None :
            st.header(f'''{str(selected_team[:]).replace("[", "").replace("]", "").replace("'","")} Team Analysis, ''' f'{(selected_year)}''')
        else :
            st.header('League Analysis, 'f'{(selected_year)}')

        if selected_year == 2020:
            st.markdown('''
            * Due to the COVID-19 pandemic, a shortened season of just 60 games was played.
            * Selecting 'None' for team will show ranking-qualified league leaders for each stat (min. 186 PA in 2020).
            * Selecting a team will show up to the top 5 qualified players in that team for each category.
            * The correlation plot is in reference to the team and year selected. If team selection is 'None', correlation is league-wide.
            ''')
        else:
            st.markdown('''
            * Selecting 'None' for team will show ranking-qualified league leaders for each stat (min. 502 PA).
            * Selecting a team will show up to the top 5 qualified players in that team for each category.
            * The correlation plot is in reference to the team and year selected. If team selection is 'None', correlation is league-wide.
            ''')
        hit_selected_team.to_csv('output.csv',index=False)
        df = pd.read_csv('output.csv')
# averages among ranking-qualified hitters across the MLB # (min.502 PA, min. 186 PA for shortened 2020 Season)
        if selected_year == 2023:
            games_played = 47
            current_time = datetime.datetime.now().time()
            if current_time.hour == 2 and current_time.minute == 30:
                games_played = games_played + 1
            qualifier = hit_stats[hit_stats['PA'] >= (games_played * 3.1)]
            qualified = pd.DataFrame(qualifier.mean())
            qualified.columns = ['League Average per Hitter']
            team = hit_selected_team[hit_selected_team['PA'] >= (games_played * 3.1)]
            team_qualified = pd.DataFrame(team.mean())
            team_qualified.columns = [f'{selected_team} Average per Hitter']
#         if selected_year == 2023 :
#             qualifier = hit_stats[hit_stats['PA']>=(47*3.1)]
#             qualified = pd.DataFrame(qualifier.mean())
#             qualified.columns=['League Average per Hitter']
#             team = hit_selected_team[hit_selected_team['PA']>=(47*3.1)]
#             team_qualified = pd.DataFrame(team.mean())
#             team_qualified.columns=[''f'{selected_team} ' 'Average per Hitter']
        elif selected_year == 2020 :
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

        with st.expander('CLICK HERE FOR COMPARISON TO LEAGUE AVERAGE STATS FOR '  f'{(selected_year)}') :
            st.write('''Stats shown are average among players who qualify for ranking in the year and team selected.''')
            with st.container() :
                if selected_team is not None :
                    st.table(compare)
                else :
                    st.table(qualified)

        st.set_option('deprecation.showPyplotGlobalUse', False) #ignore deprecation warning

        c1, c2, c3, c4 = st.columns(4)
        with c1 :
            corr = df.corr()
            mask = np.zeros_like(corr)
            mask[np.triu_indices_from(mask)] = True
            with sns.axes_style("white"):
                f, ax = plt.subplots(figsize=(7, 5))
                ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
                st.pyplot()
            if selected_team is None :
                st.bar_chart(team['RBI'].nlargest(10))
                st.bar_chart(team['OPS+'].nlargest(10))
            else :
                st.bar_chart(team['RBI'].nlargest(5))
                st.bar_chart(team['OPS+'].nlargest(5))
        with c2 :
            if selected_team is None :
                st.bar_chart(team['H'].nlargest(10))
                st.bar_chart(team['OBP'].nlargest(10))
                st.bar_chart(team['BB'].nlargest(10))
            else :
                st.bar_chart(team['H'].nlargest(5))
                st.bar_chart(team['OBP'].nlargest(5))
                st.bar_chart(team['BB'].nlargest(5))
        with c3:
            if selected_team is None :
                st.bar_chart(team['HR'].nlargest(10))
                st.bar_chart(team['SLG'].nlargest(10))
                st.bar_chart(team['SO'].nlargest(10))
            else :
                st.bar_chart(team['HR'].nlargest(5))
                st.bar_chart(team['SLG'].nlargest(5))
                st.bar_chart(team['SO'].nlargest(5))

        with c4:
            if selected_team is None :
                st.bar_chart(team['R'].nlargest(10))
                st.bar_chart(team['BA'].nlargest(10))
                st.bar_chart(team['OPS'].nlargest(10))
            else :
                st.bar_chart(team['R'].nlargest(5))
                st.bar_chart(team['BA'].nlargest(5))
                st.bar_chart(team['OPS'].nlargest(5))
###############################################################################
###############################################################################
###############################################################################

####################### Data Display for pitching tab #########################
with tab2 :
    if pitch_selected_team is not None :
         st.write('Data Dimension: ' + str(pitch_selected_team.shape[0]) + ' rows and ' + str(pitch_selected_team.shape[1]) + ' columns.')
         st.dataframe(pitch_selected_team)
    else :
         st.write('Data Dimension: ' + str(pitch_stats(selected_year).shape[0]) + ' rows and ' + str(pitch_stats(selected_year).shape[1]) + ' columns.')
         st.dataframe(pitch_stats(selected_year))
 # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
    def filedownload(df) :
        csv = df.to_csv(index=True)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}"  download="pitcher-stats.csv">Download CSV File</a>'
        return href
    st.markdown(filedownload(pitch_selected_team), unsafe_allow_html=True)
################# Exploratory Analysis Button for pitching tab #################
with tab2:
    if st.button('Exploratory Analysis', key='pitch'):
        if selected_team is not None :
            st.header(f'''{str(selected_team[:]).replace("[", "").replace("]", "").replace("'","")} Team Analysis, ''' f'{(selected_year)}''')
        else :
            st.header('League Analysis, 'f'{(selected_year)}')

        if selected_year == 2020 :
            st.markdown('''
            * Due to the COVID-19 pandemic, a shortened season of just 60 games was played.
            * Selecting 'None' for team will show ranking-qualified league leaders for each stat (min. 60 IP in 2020).
            * Selecting a team will show up to the top 5 qualified players in that team for each category.
            * The correlation plot is in reference to the team and year selected. If team selection is 'None', correlation is league-wide.
            ''')
        else:
            st.markdown('''
            * Selecting 'None' for team will show ranking-qualified league leaders for each stat (min. 162 IP).
            * Selecting a team will show up to the top 5 qualified players in that team for each category.
            * The correlation plot is in reference to the team and year selected. If team selection is 'None', correlation is league-wide.
            ''')
        pitch_selected_team.to_csv('output.csv',index=False)
        df = pd.read_csv('output.csv')
# averages among ranking-qualified pitchers across the MLB # (min.162 IP)
        if selected_year == 2023 :
            games_played = 47
            current_time = datetime.datetime.now().time()
            if current_time.hour == 2 and current_time.minute == 30 :
                games_played = games_played + 1
            p_qualifier = pitch_stats[pitch_stats['IP']>=games_played]
            p_qualified = pd.DataFrame(p_qualifier.mean())
            p_qualified.columns=['League Average per Pitcher']
            p_team = pitch_selected_team[pitch_selected_team['IP']>=games_played]
            p_team_qualified = pd.DataFrame(p_team.mean())
            p_team_qualified.columns=[''f'{selected_team} ' 'Average per Pitcher']
#         if selected_year == 2023 :
#             p_qualifier = pitch_stats[pitch_stats['IP']>=47]
#             p_qualified = pd.DataFrame(p_qualifier.mean())
#             p_qualified.columns=['League Average per Pitcher']
#             p_team = pitch_selected_team[pitch_selected_team['IP']>=47]
#             p_team_qualified = pd.DataFrame(p_team.mean())
#             p_team_qualified.columns=[''f'{selected_team} ' 'Average per Pitcher']
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

        with st.expander('CLICK HERE FOR COMPARISON TO LEAGUE AVERAGE STATS FOR '  f'{(selected_year)}') :
            st.write('''Stats shown are average among players who qualify for ranking in the year and team selected.''')
            with st.container() :
                if selected_team is not None :
                    st.table(p_compare)
                else :
                    st.table(p_qualified)

        st.set_option('deprecation.showPyplotGlobalUse', False)#ignore deprecation warning

        c1, c2, c3, c4 = st.columns(4)
        with c1 :
            corr = df.corr()
            mask = np.zeros_like(corr)
            mask[np.triu_indices_from(mask)] = True
            with sns.axes_style("white"):
                f, ax = plt.subplots(figsize=(7, 5))
                ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
                st.pyplot()
            if selected_team is None :
                st.bar_chart(p_team['H'].nsmallest(10))
                st.bar_chart(p_team['SO'].nlargest(10))
            else :
                st.bar_chart(p_team['H'].nsmallest(5))
                st.bar_chart(p_team['SO'].nlargest(5))
        with c2 :
            if selected_team is None :
                st.bar_chart(p_team['ER'].nsmallest(10))
                st.bar_chart(p_team['BB'].nsmallest(10))
                st.bar_chart(p_team['SO9'].nlargest(10))
            else :
                st.bar_chart(p_team['ER'].nsmallest(5))
                st.bar_chart(p_team['BB'].nsmallest(5))
                st.bar_chart(p_team['SO9'].nlargest(5))
        with c3:
            if selected_team is None :
                st.bar_chart(p_team['ERA'].nsmallest(10))
                st.bar_chart(p_team['IP'].nlargest(10))
                st.bar_chart(p_team['BF'].nlargest(10))
            else :
                st.bar_chart(p_team['ERA'].nsmallest(5))
                st.bar_chart(p_team['IP'].nlargest(5))
                st.bar_chart(p_team['BF'].nlargest(5))

        with c4:
            if selected_team is None :
                st.bar_chart(p_team['ERA+'].nlargest(10))
                st.bar_chart(p_team['WHIP'].nsmallest(10))
                st.bar_chart(p_team['SO/W'].nlargest(10))
            else :
                st.bar_chart(p_team['ERA+'].nlargest(5))
                st.bar_chart(p_team['WHIP'].nsmallest(5))
                st.bar_chart(p_team['SO/W'].nlargest(5))
