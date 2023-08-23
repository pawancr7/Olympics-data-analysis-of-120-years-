import streamlit as st 
import pandas as pd 
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.figure_factory as ff 

df = pd.read_csv('athlete_events.csv')
region_df =  pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image("olympics.jpg")
user_menu = st.sidebar.radio(
  'Chose an option',
   ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
  # st.header('Medal Tally')
  st.sidebar.header('Medal Tally')  
  years,country = helper.Country_year_list(df)

  selected_year = st.sidebar.selectbox("Select Year",years)
  selected_country = st.sidebar.selectbox("Select Country",country)

  medal_tally =  helper.fetch_medal_tally(df,selected_year,selected_country)
  if selected_year == 'Overall' and selected_country == 'Overall':
      st.title('Overall Tally')
  if selected_year != 'Overall' and selected_country == 'Overall':
      st.title('Medal Tally in ' + str(selected_year) + ' Olympicss')
  if selected_year == 'Overall' and selected_country != 'Overall':
      st.title(selected_country + ' overall performance')
  if selected_year != 'Overall' and selected_country != 'Overall':
      st.title(selected_country + ' performance in ' + str(selected_year) + ' Olympics')
  st.table(medal_tally)

if user_menu == 'Overall Analysis':
  editions = df['Year'].unique().shape[0] -1
  cities = df['City'].unique().shape[0]
  sports = df['Sport'].unique().shape[0]
  events = df['Event'].unique().shape[0]
  athletes = df['Name'].unique().shape[0]
  nations = df['region'].unique().shape[0]

  st.header("Top Statistics")
  col1,col2,col3  = st.columns(3)
  with col1:
      st.header('Editions')
      st.title(editions)
  with col2:
      st.header('Hosts')
      st.title(cities)
  with col3:
      st.header('Sports')
      st.title(sports)
 
  col1,col2,col3  = st.columns(3)
  with col1:
      st.header('Events')
      st.title(events)
  with col2:
      st.header('Nations')
      st.title(nations)
  with col3:
      st.header('Athletes')
      st.title(athletes)

  nations_over_time = helper.data_over_time(df,'region')

  nations_over_time = nations_over_time.sort_values(by='Edition')
  fig = px.line(nations_over_time, x="Edition", y="region")
  st.title('Participating Nations Over the years')
  st.plotly_chart(fig)

  events_over_time = helper.data_over_time(df,'Event')

  events_over_time = events_over_time.sort_values(by='Edition')
  fig = px.line(events_over_time, x="Edition", y="Event")
  st.title('Events Over the years')
  st.plotly_chart(fig)

  athlete_over_time = helper.data_over_time(df, 'Name')
  
  athlete_over_time = athlete_over_time.sort_values(by='Edition')
  fig = px.line(athlete_over_time, x="Edition", y="Name")
  st.title("Athletes over the years")
  st.plotly_chart(fig)

  st.title('No. of Events over time (Every Sport)')
  fig , ax = plt.subplots(figsize= (20,20))
  x = df.drop_duplicates(['Year','Sport','Event'])
  ax = sns.heatmap(x.pivot_table(index= 'Sport',columns = 'Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
  st.pyplot(fig)

  st.title("Most Succesfully athletees")
  sport_list = df['Sport'].unique().tolist()
  sport_list.sort()
  sport_list.insert(0,'Overall')

  selected_sport = st.selectbox('Please select a sport',sport_list)
  x=helper.most_succesful(df,selected_sport)
  st.table(x)


if user_menu == 'Country-wise Analysis':
    st.title('Country wise analysiss')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    
    selected_country = st.selectbox('Select a country ',country_list)

    country_df =  helper.year_wise_medal_tally(df,selected_country)
    fig = px.line( country_df, x="Year", y="Medal")
    st.title(selected_country  + ' Medal TAlly  Over the years')
    st.plotly_chart(fig)

    st.title(selected_country  + ' excels in fallowing sports :)')
    pt = helper.country_event_heatmap(df,selected_country)
    fig , ax = plt.subplots(figsize= (20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title('Top 10 athletes of ' + selected_country)    
    top10_df = helper.most_succesful_country_wise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset= ['Name','region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    
    fig= ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold medalist ','Silver medalist','Brown medalist'],show_hist =False ,show_rug = False)
    
    fig.layout.update(autosize = False ,height = 600 , width = 700 )
    st.title("Atheletics Age Distribution")
    st.plotly_chart(fig)


    
    x = []
    name =[]
    fam_sprt = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
            'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
             'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
             'Water Polo', 'Hockey', 'Rowing', 'Fencing',
           'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
              'Tennis', 'Golf', 'Softball', 'Archery',
              'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
            'Rhythmic Gymnastics', 'Rugby Sevens',
              'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in fam_sprt :
        temp_df =  athlete_df[athlete_df['Sport'] == sport ]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist= False , show_rug= False )
    fig.update_layout(autosize = False , height = 600 ,width = 600 )
    st.title('Distribution of Age (Gold medal players)')
    st.plotly_chart(fig)

    st.title('Weight and Height (analysed)')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Please select a sport',sport_list)

    temp_df = helper.W_VS_H(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x = temp_df['Weight'],y = temp_df['Height'],hue= temp_df['Medal'],style= temp_df['Sex'],s = 50)
    st.pyplot(fig)

    st.title('Men vs Wommen year wise analysis ')
    final = helper.men_vs_wommen(df)
    fig = px.line(final,x= 'Year',y = ['Male','Female'])
    fig.update_layout(autosize = False , height = 600 ,width = 600 )
    st.plotly_chart(fig)




