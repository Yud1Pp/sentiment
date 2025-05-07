import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from scraper import TokopediaScraper
from sentiment import analyze_sentiment
from lda import preprocess_text, perform_lda, display_topics

st.set_page_config(page_title="Tokopedia Review Scraper", layout="wide")

st.title("📦 Scraper & Analisis Sentimen Review Tokopedia")
st.markdown("Masukkan URL produk Tokopedia dan lihat analisis sentimen komentar dari pelanggan.")

product_url = st.text_input("🔗 Masukkan URL produk Tokopedia:", value="https://www.tokopedia.com/khagi-jaya-baby/3-pcs-my-baby-minyak-telon-plus-lavender-90ml-3pcs-minyak-anti-nyamuk-8-jam-exp-2026-bayi-1730376089904121178?t_id=1746632666571&t_st=5&t_pp=homepage&t_efo=pure_goods_card&t_ef=homepage&t_sm=rec_homepage_outer_flow&t_spt=homepage")

if st.button("Mulai Scraping & Analisis") and product_url:
    with st.spinner("Mengambil data review dan melakukan analisis sentimen..."):
        servicePath = "chromedriver.exe"
        scraper = TokopediaScraper(product_url, servicePath)
        reviews = scraper.scrape_and_analyze()
        
        if not reviews:
            st.warning("Tidak ada review ditemukan.")
        else:
            st.success(f"Berhasil mengambil {len(reviews)} review.")

            df = pd.DataFrame(reviews)
            df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')
            df["Processed Komentar"] = preprocess_text(df['Komentar'])
            comments = df["Processed Komentar"].tolist()
        
            df["Sentimen"] = df["Processed Komentar"].apply(analyze_sentiment)

            df1 = df.copy()
            df1.drop(columns=["Processed Komentar"], inplace=True)

            st.subheader("📊 Tabel Review & Sentimen")
            st.dataframe(df1, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, "review_tokopedia.csv", "text/csv")

            st.subheader("📈 Visualisasi Analisis")
            df = df[df["Komentar"] != "(komentar tidak ditemukan)"]
            
            st.markdown("### Jumlah Review per Rating")
            fig1, ax1 = plt.subplots()
            sns.countplot(x="Rating", hue="Rating", data=df, ax=ax1, legend=False)
            ax1.set_xlabel("Rating")
            ax1.set_ylabel("Jumlah Review")
            ax1.set_title("Distribusi Rating")
            st.pyplot(fig1)

            st.markdown("### Komposisi Sentimen")
            sentimen_counts = df["Sentimen"].value_counts()
            sentimen_counts = sentimen_counts[sentimen_counts.index != "unknown"]
            fig2, ax2 = plt.subplots()
            ax2.pie(sentimen_counts, labels=sentimen_counts.index, autopct='%1.1f%%', startangle=90,
                    colors=['lightgreen', 'salmon', 'gold'])  # pastikan urutan warnanya sesuai dengan jumlah label
            ax2.set_title("Distribusi Sentimen")
            st.pyplot(fig2)

            st.markdown("### Word Cloud Komentar Positif")
            positive_comments = " ".join(df[df["Sentimen"] == "positive"]["Processed Komentar"])
            if positive_comments.strip():
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_comments)
                fig3, ax3 = plt.subplots(figsize=(10, 5))
                ax3.imshow(wordcloud, interpolation='bilinear')
                ax3.axis("off")
                st.pyplot(fig3)
            else:
                st.info("Tidak ada komentar positif untuk ditampilkan dalam word cloud.")

            st.markdown("### Word Cloud Komentar Negatif")
            negative_comments = " ".join(df[df["Sentimen"] == "negative"]["Processed Komentar"])
            if negative_comments.strip():
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(negative_comments)
                fig4, ax4 = plt.subplots(figsize=(10, 5))
                ax4.imshow(wordcloud, interpolation='bilinear')
                ax4.axis("off")
                st.pyplot(fig4)
            else:
                st.info("Tidak ada komentar negatif untuk ditampilkan dalam word cloud.")

            st.markdown("### Word Cloud Komentar Netral")
            neutral_comments = " ".join(df[df["Sentimen"] == "neutral"]["Processed Komentar"])
            if neutral_comments.strip():
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(neutral_comments)
                fig5, ax5 = plt.subplots(figsize=(10, 5))
                ax5.imshow(wordcloud, interpolation='bilinear')
                ax5.axis("off")
                st.pyplot(fig5)
            else:
                st.info("Tidak ada komentar netral untuk ditampilkan dalam word cloud.")

            st.subheader("📊 Analisis LDA - Topik dari Komentar")
            preprocessed_comments = df["Processed Komentar"].tolist()
            num_topics = 5  
            topics = perform_lda(preprocessed_comments, num_topics=num_topics)
            
            display_topics(topics)
            st.markdown("### Visualisasi Topik LDA")
            fig6, ax6 = plt.subplots()
            sns.barplot(x=[len(topic[1]) for topic in topics], y=[topic[0] for topic in topics], ax=ax6)
            ax6.set_xlabel("Jumlah Kata")
            ax6.set_ylabel("Topik")
            ax6.set_title("Topik LDA dari Komentar")
            st.pyplot(fig6)