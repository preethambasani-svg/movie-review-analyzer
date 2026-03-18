import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Title
st.title("🎬 IMDb Movie Review Analyzer (Advanced)")

# Load dataset
df = pd.read_csv("dataset.csv")

# Input
movie_name = st.text_input("Enter keyword (e.g., good, bad, love, worst)")

if st.button("Analyze"):

    st.subheader(f"Results for: {movie_name}")

    # 🔍 Filter reviews based on keyword
    filtered_df = df[df['review'].str.contains(movie_name, case=False, na=False)]

    # ⚠️ Handle no results
    if len(filtered_df) == 0:
        st.warning("⚠️ No reviews found for this keyword")
    else:
        # Count sentiments
        positive = (filtered_df['sentiment'] == "positive").sum()
        negative = (filtered_df['sentiment'] == "negative").sum()

        total = len(filtered_df)

        pos_percent = (positive / total) * 100
        neg_percent = (negative / total) * 100

        # 📊 Display results
        st.write(f"👍 Positive Reviews: {pos_percent:.2f}%")
        st.write(f"👎 Negative Reviews: {neg_percent:.2f}%")

        # 📊 Bar Chart
        chart_data = pd.DataFrame({
            "Sentiment": ["Positive", "Negative"],
            "Percentage": [pos_percent, neg_percent]
        })

        st.subheader("📊 Bar Chart")
        st.bar_chart(chart_data.set_index("Sentiment"))

        # 🥧 Pie Chart
        st.subheader("🥧 Sentiment Distribution")
        fig, ax = plt.subplots()
        ax.pie(
            [pos_percent, neg_percent],
            labels=["Positive", "Negative"],
            autopct='%1.1f%%'
        )
        st.pyplot(fig)

        # ☁️ Word Cloud (filtered data)
        st.subheader("☁️ Word Cloud")
        text = " ".join(filtered_df['review'])

        wordcloud = WordCloud(width=800, height=400).generate(text)

        fig2, ax2 = plt.subplots()
        ax2.imshow(wordcloud)
        ax2.axis("off")
        st.pyplot(fig2)

        # ⭐ Final Verdict
        if pos_percent > neg_percent:
            st.success("✅ Overall Sentiment is Positive")
        else:
            st.error("❌ Overall Sentiment is Negative")