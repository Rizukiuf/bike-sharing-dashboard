import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

sns.set(style='dark')

# Load data
day_df = pd.read_csv('dashboard/day.csv')
hour_df = pd.read_csv('dashboard/hour.csv')

# Create filter components
min_date = pd.to_datetime(day_df['dteday']).min()
max_date = pd.to_datetime(day_df['dteday']).max()

# Sidebar
with st.sidebar:
	st.image("https://rizukiuf.github.io/assets/raw/bike-company.png", width=200)
	st.write('Explore bike sharing data!')
	st.write('Select a date range to explore the data')

	# Date range input
	with st.form(key='date_range_form'):
		date_range = st.date_input('Select date range', value=[min_date, max_date])
		submit_button = st.form_submit_button(label='Submit')

# Filter data
date_range = pd.to_datetime(date_range)
filtered_day_df = day_df[(pd.to_datetime(day_df['dteday']) >= date_range[0]) & (pd.to_datetime(day_df['dteday']) <= date_range[1])]
filtered_hour_df = hour_df[(pd.to_datetime(hour_df['dteday']) >= date_range[0]) & (pd.to_datetime(hour_df['dteday']) <= date_range[1])]


# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_agg_year_month_df(df):
  return df.groupby(['yr', 'mnth'], as_index=False).agg({
		'cnt': 'sum'
	})

def create_agg_season_df(df):
	return df.groupby('season', as_index=False).agg({
		'casual': 'mean',
		'registered': 'mean',
	})

def create_agg_weekday_df(df):
	return df.groupby('weekday', as_index=False).agg({
		'casual': 'mean',
		'registered': 'mean',
	})

def create_agg_holiday_df(df):
	return df.groupby('holiday', as_index=False).agg({
		'casual': 'mean',
		'registered': 'mean',
		'cnt': 'mean',
	})

def create_agg_workingday_df(df):
	return df.groupby('workingday', as_index=False).agg({
		'casual': 'mean',
		'registered': 'mean',
		'cnt': 'mean',
	})
 
def create_agg_weather_df(df):
	return df.groupby('weathersit', as_index=False).agg({
		'casual': 'mean',
		'registered': 'mean',
		'cnt': 'mean',
	})

def create_agg_hour_weekday_df(df):
	return df.groupby(['weekday', 'hr'], as_index=False).agg({
		'cnt': 'mean',
	})

def create_agg_hour_season_df(df):
	return df.groupby(['season', 'hr'], as_index=False).agg({
		'cnt': 'mean',
	})


# Dashboard title
st.title('Bike Sharing Dashboard 🚲')

# Total bike rental
st.header('Total Bike Rental (Filtered)')
st.write('Filtered from {} to {}'.format(date_range[0].strftime('%d %B %Y'), date_range[1].strftime('%d %B %Y')))
col1, col2, col3 = st.columns(3)
with col1:
	st.metric(label='Casual', value=filtered_day_df['casual'].sum())
with col2:
	st.metric(label='Registered', value=filtered_day_df['registered'].sum())
with col3:
	st.metric(label='Total', value=filtered_day_df['cnt'].sum())


# 1. Trend of bike rental usage each month and year
agg_year_month_df = create_agg_year_month_df(day_df)

st.header('1. Bike Rental Trend')
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(data=agg_year_month_df, x='mnth', y='cnt', hue='yr', ax=ax, marker='o', errorbar=None, palette='viridis')
ax.set_title('Bike Rental Trend by Month and Year')
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax.legend(title='Year', labels=['2011', '2012'])

# add horizontal line for each point
line_colors = ['lightgrey', 'lightblue', 'lightgreen']
for index, row in agg_year_month_df.iterrows():
	color = line_colors[index % len(line_colors)]
	ax.axhline(y=row['cnt'], color=color, linestyle='--', linewidth=0.5)

# add vertical line for each month
for month in range(1, 13):
	ax.axvline(x=month, color='lightgrey', linestyle='--', linewidth=0.5)

st.pyplot(fig)


# 2. Bike rental usage by season
agg_season_df = create_agg_season_df(day_df)

st.header('2. Bike Rental by Season')
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(agg_season_df['season'], agg_season_df['casual'], label='Casual', color='lightcoral')
ax.bar(agg_season_df['season'], agg_season_df['registered'], label='Registered', color='cornflowerblue', bottom=agg_season_df['casual'])
ax.set_title('Average Bike Rental by Season')
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_xticks(ticks=range(1, 5), labels=['Spring', 'Summer', 'Fall', 'Winter'])

st.pyplot(fig)


# 3. Comparison of bike rental usage between days of the week, between holiday and non-holiday, and between workingday and non-workingday
agg_weekday_df = create_agg_weekday_df(filtered_day_df)
agg_holiday_df = create_agg_holiday_df(filtered_day_df)
agg_workingday_df = create_agg_workingday_df(filtered_day_df)

st.header('3. Bike Rental by Day Type (Filtered)')
st.write('Filtered from {} to {}'.format(date_range[0].strftime('%d %B %Y'), date_range[1].strftime('%d %B %Y')))

fig = plt.figure(figsize=(10, 8))
fig.subplots_adjust(hspace=0.4, wspace=0.1)
ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)

# bar average comparison between days of the week
ax1.bar(agg_weekday_df['weekday'], agg_weekday_df['casual'], label='Casual', color='lightcoral')
ax1.bar(agg_weekday_df['weekday'], agg_weekday_df['registered'], label='Registered', color='cornflowerblue', bottom=agg_weekday_df['casual'])
ax1.set_title('Average Bike Rental by Day of the Week')
ax1.set_xlabel(None)
ax1.set_ylabel(None)
ax1.set_xticks(ticks=range(0, 7), labels=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
ax1.legend()

# pie chart average comparison between holiday and non-holiday
ax2 = plt.subplot2grid((2, 2), (1, 0))
ax2.pie(agg_holiday_df['cnt'], labels=['Non-Holiday', 'Holiday'], autopct='%1.1f%%', startangle=60, colors=['violet', 'aquamarine'])
ax2.set_title('Average Bike Rental by Holiday')

# pie chart average comparison between workingday and non-workingday
ax3 = plt.subplot2grid((2, 2), (1, 1))
ax3.pie(agg_workingday_df['cnt'], labels=['Non-Workingday', 'Workingday'], autopct='%1.1f%%', startangle=60, colors=['lightskyblue', 'lightpink'])
ax3.set_title('Average Bike Rental by Workingday')

st.pyplot(fig)


# 4. Bike rental usage by weather, temperature, humidity, and wind speed
agg_weather_df = create_agg_weather_df(filtered_day_df)

st.header('4. Bike Rental by Weather, Temperature, Humidity, and Wind Speed (Filtered)')
st.write('Filtered from {} to {}'.format(date_range[0].strftime('%d %B %Y'), date_range[1].strftime('%d %B %Y')))

# visualize bike rental by weather situation
st.subheader('Bike Rental by Weather Situation')
fig, ax = plt.subplots(figsize=(12, 3))
ax.barh(agg_weather_df['weathersit'], agg_weather_df['casual'], label='Casual', color='lightcoral')
ax.barh(agg_weather_df['weathersit'], agg_weather_df['registered'], label='Registered', color='cornflowerblue', left=agg_weather_df['casual'])
ax.set_title('Average Bike Rental by Weather Situation')
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_yticks(ticks=range(1, 4), labels=['Clear/Partly Cloudy', 'Mist/Cloudy', 'Light Rain/Snow'])
ax.legend()

st.pyplot(fig)

# visualize the impact of temperature, humidity, and wind speed on bike rental usage using scatter plot
st.subheader('Bike Rental by Temperature, Humidity, and Wind Speed')
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
sns.scatterplot(data=filtered_day_df, x='temp', y='cnt', ax=ax[0], color='skyblue')
sns.scatterplot(data=filtered_day_df, x='hum', y='cnt', ax=ax[1], color='lightgreen')
sns.scatterplot(data=filtered_day_df, x='windspeed', y='cnt', ax=ax[2], color='lightcoral')
ax[0].set_title('Bike Rental by Temperature')
ax[0].set_xlabel('Temperature')
ax[0].set_ylabel('Count')
ax[1].set_title('Bike Rental by Humidity')
ax[1].set_xlabel('Humidity')
ax[1].set_ylabel(None)
ax[2].set_title('Bike Rental by Wind Speed')
ax[2].set_xlabel('Wind Speed')
ax[2].set_ylabel(None)

st.pyplot(fig)

# heatmap correlation between temperature, humidity, wind speed, and bike rental usage
st.subheader('Correlation Heatmap')
fig, ax = plt.subplots(figsize=(10, 4))
corr = filtered_day_df[['temp', 'hum', 'windspeed', 'cnt']].corr()
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', mask=mask)
ax.set_title('Correlation Heatmap between Temperature, Humidity, Wind Speed, and Bike Rental Usage')

st.pyplot(fig)


# 5. Distribution of bike rental per hour between days of the week and between seasons
agg_hour_weekday_df = create_agg_hour_weekday_df(filtered_hour_df)
agg_hour_season_df = create_agg_hour_season_df(filtered_hour_df)

st.header('5. Distribution of Bike Rental per Hour (Filtered)')
st.write('Filtered from {} to {}'.format(date_range[0].strftime('%d %B %Y'), date_range[1].strftime('%d %B %Y')))

# visualize bike rental distribution per hour between days of the week
st.subheader('Between Days of the Week')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=agg_hour_weekday_df, x='hr', y='cnt', hue='weekday', ax=ax, marker='o', palette='colorblind', errorbar=None)
ax.set_title('Average Bike Rental per Hour between Days of the Week')
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_xticks(ticks=range(0, 24))
ax.grid(alpha=0.5)
ax.legend(title='Weekday', labels=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])

st.pyplot(fig)

# visualize bike rental distribution per hour between seasons
st.subheader('Between Seasons')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=agg_hour_season_df, x='hr', y='cnt', hue='season', ax=ax, marker='o', palette='colorblind', errorbar=None)
ax.set_title('Average Bike Rental per Hour between Seasons')
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_xticks(ticks=range(0, 24))
ax.grid(alpha=0.5)
ax.legend(title='Season', labels=['Spring', 'Summer', 'Fall', 'Winter'])

st.pyplot(fig)


st.markdown('---')
st.write('© 2024 Rizki Utama Fauzi - All Rights Reserved')