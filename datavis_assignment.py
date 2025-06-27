# app.py
import streamlit as st
import altair as alt
import pandas as pd
df = pd.read_csv("listings.csv")

st.header("Sarah's Week 6 Assignment on Airbnb Data Visualization")
st.markdown("### Visualization 1: Filtered Scatterplot of Review Scores by Neighborhood")

# Clean and convert 'host_response_rate'
# Remove '%' and convert to numeric, coercing errors to NaN
df['host_response_rate'] = df['host_response_rate'].astype(str).str.replace('%', '', regex=False)
df['host_response_rate'] = pd.to_numeric(df['host_response_rate'], errors='coerce')

# ***Visualization 1: Filtered Scatterplot of Host Response Rates***
# **Filter select box
#Filter by Neighborhood

neighborhood =st.selectbox("Filter by Neighborhood", options=df["host_neighbourhood"].unique())

#Slider: Filter by Review Scores
min_score = round(df["review_scores_rating"].min(), 1)
max_score = round(df["review_scores_rating"].max(), 1)

review_scores_range = st.slider(
    "Select Review Scores Range",
    min_value=min_score,
    max_value=max_score,
    value=(min_score, max_score),
    step=0.1
)

# Apply filters to the DataFrame by neighborhood
filtered_df_neighborhood = df[
    (df["host_neighbourhood"] == neighborhood) &
    (df["review_scores_rating"].between(*review_scores_range))
]

# Create a chart
chart = alt.Chart(filtered_df_neighborhood).mark_circle(size=60, opacity=0.6).encode(
    x=alt.X("review_scores_rating:Q", title="Host Review Ratings"),
    y=alt.Y("number_of_reviews:Q", title="Number of Reviews"),
).interactive()

#Display the chart
st.altair_chart(chart, use_container_width=True)

# ***Visualization 2: Linked Bar Graphs of Airbnb listings by Neighborhood***
st.markdown("### Visualization 2: Linked Bar Graphs of Airbnb listings by Neighborhood")

click = alt.selection_point(encodings=['color'])

# Bar chart: Clicking a bar selects an "Origin" and highlights it
top10_neigh = (
    df['neighbourhood_cleansed']
    .value_counts()
    .nlargest(10)
    .index
)

neightopten_df = df[df['neighbourhood_cleansed'].isin(top10_neigh)]

hist = alt.Chart(neightopten_df).mark_bar().encode(
    x='count()',  # Count the number of cars per Origin
    y=alt.Y('neighbourhood_cleansed:N', sort='-x'),  # Categorical axis for car origin
    color=alt.condition(click, 'neighbourhood_cleansed:N', alt.value('lightgray'))  # Highlight selection, gray out others
).add_params(
    click  # Add interactive selection to the chart
)

linked_chart = alt.Chart(df).mark_bar().encode(
    y=alt.Y("room_type:N", title="Room Type"),
    x=alt.X("count():Q", title="Count"),
).transform_filter(
    click
)

combined_chart = hist & linked_chart
st.altair_chart(combined_chart, use_container_width=True)


# ***Visualization 3: Coordinated Histograms of Room Characteristics***
st.markdown("### Visualization 3: Coordinated Histograms of Room Characteristics")

# Remove '$' and commas (if any), and convert to numeric, coercing errors to NaN
df['price'] = df['price'].astype(str).str.replace('$', '', regex=False)
df['price'] = df['price'].astype(str).str.replace(',', '', regex=False) # Also remove commas
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Create price filter that limits Airbnb prices to below $3000
df_price_filtered = df[(df['price'] <= 3000) & (df['estimated_revenue_l365d'] < 200000) & (df['review_scores_rating'] > 3)].copy()

brush_4 = alt.selection_interval(encodings=['x'])

chart_4 = alt.Chart(df_price_filtered).mark_tick().encode(
    color=alt.when(brush_4).then(alt.value('steelblue')).otherwise(alt.value('lightgray'))
).add_params(
    brush_4
)
(
chart_4.encode(x='price:Q') &
chart_4.encode(x='number_of_reviews:Q') &
chart_4.encode(x='estimated_revenue_l365d:Q') &
chart_4.encode(x='review_scores_rating:Q')
)

st.altair_chart(chart_4, use_container_width=True)