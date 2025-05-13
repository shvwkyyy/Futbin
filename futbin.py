import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

players = pd.read_csv('C:/Users/fares/OneDrive/Desktop/PYTHON/Scrap/players2.csv')
icons = pd.read_csv('C:/Users/fares/OneDrive/Desktop/PYTHON/Scrap/Icons.csv')

def clean_players(df):
    df.rename(columns={'In Game Stats': 'IGS'}, inplace=True)
    df.drop(columns='Side Position', axis=1, inplace=True)
    df['Position'] = df['Position'].str.replace('++', '', regex=False)
    df['Popularity'] = df['Popularity'].str.replace(',', '').astype(float)
    df[['Height (cm)', 'Height (ft)', 'Body Description']] = df['Body Type'].str.extract(
        r'(\d+\s*cm)\s*\|\s*([\d\'\"]+)\s*\n*(.*)'
    )
    df['Body Description'] = df['Body Description'].str.replace(r'\s*\(.*?\)', '', regex=True)
    df.drop(columns=['Body Type', 'Height (ft)'], axis=1, inplace=True)
    df['Weight'] = df['Weight'].str.replace('kg', '', regex=False).astype(int)
    df['Price'] = df['Price'].apply(lambda x: float(x.replace('K', '')) * 1000 if 'K' in x else float(x))
    df['Height (cm)'] = df['Height (cm)'].str.replace('cm', '', regex=False).astype(int)
    return df

def clean_icons(df):
    df.drop(index=259, inplace=True)
    df.rename(columns={'Player': 'Name'}, inplace=True)
    df.rename(columns={'Physic': 'Physicality'}, inplace=True)
    df.drop(columns='sidePosition', inplace=True)
    df['Position'] = df['Position'].str.replace('++', '', regex=False)
    df['Popularity'] = df['Popularity'].str.replace(',', '').astype(float)
    df['Weight'] = df['Weight'].str.replace('kg', '', regex=False).astype(int)
    df[['Height (cm)', 'Height (ft)', 'Body']] = df['Body'].str.extract(
        r'(\d+\s*cm)\s*\|\s*([\d\'\"]+)\s*\n*(.*)'
    )
    df.drop(columns=['Body','Height (ft)','Club','League'], inplace=True)
    df['Height (cm)'] = df['Height (cm)'].str.replace('cm', '', regex=False).astype(int)

    def replace(price):
        if 'K' in price:
            return float(price.replace('K', '')) * 1000
        elif 'M' in price:
            return float(price.replace('M', '')) * 1000000
        else:
            return float(price)

    df['Price'] = df['Price'].apply(replace)
    df.index = df['Name']
    df.loc['Edson Arantes Nascimento','Name']= 'Pelé'
    df.reset_index(drop=True, inplace=True)
    return df

players = clean_players(players)
icons = clean_icons(icons)

def main():
    kind = st.selectbox("Select Name Type", options=['Icons', 'Normal'], index=0)

    if kind == 'Icons':
        min_rating = st.slider("Minimum Rating", int(icons['Rating'].min()), int(icons['Rating'].max()), 80)
        filtered_df = icons[
            (icons['Rating'] >= min_rating)
        ]
    else:
        min_rating = st.slider("Minimum Rating", int(players['Rating'].min()), int(players['Rating'].max()), 80)
        filtered_df = players[
            (players['Rating'] >= min_rating)
        ]
        def generate_wordcloud(text):
            wordcloud = WordCloud(width=800, height=400, background_color='white', min_font_size=10).generate(text)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            return fig
        text = ' '.join(filtered_df['Club'].str.replace(' ', '_', regex=False))
        fig = generate_wordcloud(text)
        st.pyplot(fig)

        # 1. Distribution of Top Leagues (Pie Chart)
        top_leagues = ['LALIGA EA SPORTS','Premier League','Bundesliga','Serie A TIM','Ligue 1 Uber Eats']
        filtered_df['Top_Leagues'] = filtered_df['League'].apply(lambda x: 'other' if x not in top_leagues else x)
        league_counts = filtered_df['Top_Leagues'].value_counts()

        fig = px.pie(league_counts, values='count',names=league_counts.index, 
                    title='Distribution of Top Leagues')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)


    st.title("Summary")
    st.subheader("Fastest Players")
    st.write(filtered_df[filtered_df['Pace'] ==filtered_df['Pace'].max()][["Name",'Position','Rating','Price','Pace']])
    st.subheader("Highest Shooting Players")
    st.write(filtered_df[filtered_df['Shooting'] ==filtered_df['Shooting'].max()][["Name",'Position','Rating','Price','Shooting']])
    st.subheader("Highest Passing Players")
    st.write(filtered_df[filtered_df['Passing'] ==filtered_df['Passing'].max()][["Name",'Position','Rating','Price','Passing']])
    st.subheader("Highest Dribbling Players")
    st.write(filtered_df[filtered_df['Dribbling'] ==filtered_df['Dribbling'].max()][["Name",'Position','Rating','Price','Dribbling']])
    st.subheader("Highest Defending Players")
    st.write(filtered_df[filtered_df['Defending'] ==filtered_df['Defending'].max()][["Name",'Position','Rating','Price','Defending']])
    st.subheader("Highest Physicality Players")
    st.write(filtered_df[filtered_df['Physicality'] ==filtered_df['Physicality'].max()][["Name",'Position','Rating','Price','Physicality']])
    st.subheader("Most Popular Players")
    st.write(filtered_df[filtered_df['Popularity'] ==filtered_df['Popularity'].max()][["Name",'Position','Rating','Price','Popularity']])
    st.subheader("Most Expensive Players")
    st.write(filtered_df[filtered_df['Price'] ==filtered_df['Price'].max()][["Name",'Position','Rating','Price']])
    st.subheader("Tallest Players")
    st.write(filtered_df[filtered_df['Height (cm)'] ==filtered_df['Height (cm)'].max()][["Name",'Position','Rating','Price','Height (cm)']])
    st.subheader("Shortest Players")
    st.write(filtered_df[filtered_df['Height (cm)'] ==filtered_df['Height (cm)'].min()][["Name",'Position','Rating','Price','Height (cm)']])
    st.subheader("Heaviest Players")
    st.write(filtered_df[filtered_df['Weight'] ==filtered_df['Weight'].max()][["Name",'Position','Rating','Price','Weight']])
    st.subheader("Lightest Players")
    st.write(filtered_df[filtered_df['Weight'] ==filtered_df['Weight'].min()][["Name",'Position','Rating','Price','Weight']])
    st.subheader("Highest In Game Stats Players")
    st.write(filtered_df[filtered_df['IGS'] ==filtered_df['IGS'].max()][["Name",'Position','Rating','Price','IGS']])


    # spider plot for player attributes
    st.subheader("Name Radar Chart")
    player_name = st.selectbox("Select Name", options=sorted(filtered_df['Name'].unique()), index=0)
    player_data = filtered_df[filtered_df['Name'] == player_name].iloc[0]

    attributes = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physicality']
    values = player_data[attributes].tolist() + [player_data[attributes].iloc[0]]  # Close the loop

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=attributes + [attributes[0]],
        fill='toself',
        name=player_name,
        line_color='blue'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title=f"Radar Chart for {player_name}",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(filtered_df, x='Nation')
    fig.update_traces(marker=dict(color='blue', line=dict(width=2, color='black')))
    fig.update_layout(title='Bar Chart of Nations', xaxis_title='Nations', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)

    # 2. Price vs. Rating
    ratings = filtered_df.groupby('Rating')['Price'].mean().reset_index()
    fig = px.line(ratings, x='Rating', y='Price', 
                title='Price vs. Rating', markers=True)
    fig.update_traces(line=dict(width=2), marker=dict(size=8))
    st.plotly_chart(fig, use_container_width=True)

    # 3. Popularity vs. Rating
    ratings = filtered_df.groupby('Rating')['Popularity'].mean().reset_index()
    fig = px.line(ratings, x='Rating', y='Popularity', 
                title='Popularity vs. Rating', markers=True)
    fig.update_traces(line=dict(width=2), marker=dict(size=8))
    st.plotly_chart(fig, use_container_width=True)

    # 4. Average Price by Position and Strong Foot
    positions = filtered_df.groupby(['Position', 'Strong Foot'])['Price'].mean().reset_index()
    fig = px.bar(positions, x='Position', y='Price', color='Strong Foot',
                barmode='group', title='Average Price by Position and Strong Foot')
    fig.update_layout(xaxis_title='Position', yaxis_title='Average Price')
    st.plotly_chart(fig, use_container_width=True)

    # 5. Average Popularity by Position and Strong Foot
    positions2 = filtered_df.groupby(['Position', 'Strong Foot'])['Popularity'].mean().reset_index()
    fig = px.bar(positions2, x='Position', y='Popularity', color='Strong Foot',
                barmode='group', title='Average Popularity by Position and Strong Foot')
    fig.update_layout(xaxis_title='Position', yaxis_title='Average Popularity')
    st.plotly_chart(fig, use_container_width=True)

    # 6. Scatter Plot of Weight vs. Height colored by Age
    fig = px.scatter(filtered_df, x='Weight', y='Height (cm)', color='Age',
                    title='Scatter Plot of Weight vs. Height (cm) colored by Age',
                    opacity=0.7)
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(xaxis_title='Weight', yaxis_title='Height (cm)')
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()