import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from scraper import TokopediaScraper
from sentiment import analyze_sentiment
from lda import preprocess_text, perform_lda, display_topics  # Import fungsi dari lda.py

# Konfigurasi halaman
st.set_page_config(page_title="Tokopedia Review Scraper", layout="wide")

st.title("📦 Scraper & Analisis Sentimen Review Tokopedia")
st.markdown("Masukkan URL produk Tokopedia dan lihat analisis sentimen komentar dari pelanggan.")

# Input URL
product_url = st.text_input("🔗 Masukkan URL produk Tokopedia:")

# Tombol eksekusi scraping dan analisis
if st.button("Mulai Scraping & Analisis") and product_url:
    with st.spinner("Mengambil data review dan melakukan analisis sentimen..."):
        scraper = TokopediaScraper(product_url)
        reviews = scraper.scrape_and_analyze()
        st.write(reviews)

        if not reviews:
            st.warning("Tidak ada review ditemukan.")
        else:
            st.success(f"Berhasil mengambil {len(reviews)} review.")

            # Analisis sentimen
            for review in reviews:
                review['Sentimen'] = analyze_sentiment(review['Komentar'])

            # Ubah jadi DataFrame
            df = pd.DataFrame(reviews)
            df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')

            # Tampilkan tabel
            st.subheader("📊 Tabel Review & Sentimen")
            st.dataframe(df)

            # Tombol download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, "review_tokopedia.csv", "text/csv")

            # ---- VISUALISASI ----
            st.subheader("📈 Visualisasi Analisis")
            df = df[df["Komentar"] != "(komentar tidak ditemukan)"]
            
            # 1. Bar Chart Jumlah Review per Rating
            st.markdown("### Jumlah Review per Rating")
            fig1, ax1 = plt.subplots()
            sns.countplot(x="Rating", hue="Rating", data=df, ax=ax1, legend=False)
            ax1.set_xlabel("Rating")
            ax1.set_ylabel("Jumlah Review")
            ax1.set_title("Distribusi Rating")
            st.pyplot(fig1)

            # 2. Pie Chart Komposisi Sentimen
            st.markdown("### Komposisi Sentimen")
            sentimen_counts = df["Sentimen"].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.pie(sentimen_counts, labels=sentimen_counts.index, autopct='%1.1f%%', startangle=90,
                    colors=['lightgreen', 'salmon', 'gold'])
            ax2.set_title("Distribusi Sentimen")
            st.pyplot(fig2)

            # 3. Word Cloud untuk Komentar Positif
            st.markdown("### Word Cloud Komentar Positif")
            positive_comments = " ".join(df[df["Sentimen"] == "positive"]["Komentar"])
            if positive_comments.strip():
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_comments)
                fig3, ax3 = plt.subplots(figsize=(10, 5))
                ax3.imshow(wordcloud, interpolation='bilinear')
                ax3.axis("off")
                st.pyplot(fig3)
            else:
                st.info("Tidak ada komentar positif untuk ditampilkan dalam word cloud.")

            # 4. Word Cloud untuk Komentar Negatif
            st.markdown("### Word Cloud Komentar Negatif")
            negative_comments = " ".join(df[df["Sentimen"] == "negative"]["Komentar"])
            if negative_comments.strip():
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(negative_comments)
                fig4, ax4 = plt.subplots(figsize=(10, 5))
                ax4.imshow(wordcloud, interpolation='bilinear')
                ax4.axis("off")
                st.pyplot(fig4)
            else:
                st.info("Tidak ada komentar negatif untuk ditampilkan dalam word cloud.")

            # 5. Word Cloud untuk Komentar Netral
            st.markdown("### Word Cloud Komentar Netral")
            neutral_comments = " ".join(df[df["Sentimen"] == "neutral"]["Komentar"])
            if neutral_comments.strip():
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(neutral_comments)
                fig5, ax5 = plt.subplots(figsize=(10, 5))
                ax5.imshow(wordcloud, interpolation='bilinear')
                ax5.axis("off")
                st.pyplot(fig5)
            else:
                st.info("Tidak ada komentar netral untuk ditampilkan dalam word cloud.")

            # ---- ANALISIS LDA ----
            st.subheader("📊 Analisis LDA - Topik dari Komentar")
            # Preprocess komentar untuk LDA
            preprocessed_comments = preprocess_text(df['Komentar'])

            # Perform LDA
            num_topics = 5  # Anda bisa menyesuaikan jumlah topik
            topics = perform_lda(preprocessed_comments, num_topics=num_topics)

            # Menampilkan topik yang ditemukan
            display_topics(topics)
            st.markdown("### Visualisasi Topik LDA")
            fig6, ax6 = plt.subplots()
            sns.barplot(x=[len(topic[1]) for topic in topics], y=[topic[0] for topic in topics], ax=ax6)
            ax6.set_xlabel("Jumlah Kata")
            ax6.set_ylabel("Topik")
            ax6.set_title("Topik LDA dari Komentar")
            st.pyplot(fig6)
            