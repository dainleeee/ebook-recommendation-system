from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import psycopg2
import re

# 데이터 불러오기
def load_data():
    host = "jelani.db.elephantsql.com"
    user = "dbmjodhp"
    password = "ZBkJSjivgLQ9ffvcmUm_lZulOvyCmfO6"
    database = "dbmjodhp"

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cur = connection.cursor()
    cur.execute("SELECT * FROM ebook;")
    result = cur.fetchall()
    connection.close()

    ebook_df = pd.DataFrame(result)
    ebook_df = pd.DataFrame(result).loc[:,1:]
    ebook_df.rename(columns={1: 'title', 2: 'author', 3: 'publisher', 4: 'category1', 5: 'category2', 6: 'price', 7: 'rate', 8: 'product_link', 9: 'img_link', 10: 'introduce'}, inplace=True)
    
    return ebook_df


# 도서에 대한 컨텐츠(소개글, 저자명, 출판사, 대분류, 소분류)를 하나로 합치기
def create_soup(x):
    return ''.join(x['author']) + ' ' + ''.join(x['publisher']) + ' ' + ''.join(x['category1']) + ' ' + ''.join(x['category2']) + ' ' + ''.join(x['introduce'])

# 한글, 영문, 숫자만 남기고 모두 제거
def clean_text(text):
    text = re.sub('[^가-힣a-zA-Z0-9\\s]', '', str(text))
    return text

# 한글제거
def remove_won(text):
    text = re.sub('[가-힣]', '', str(text))
    return text


# 도서 제목을 입력받아 해당 도서와 유사한 도서 12개를 추천하는 함수
def get_recommendations(title):
    ebook_df = load_data()

    # rate 변수값 중 na값에 빈칸 채우기
    ebook_df['rate'] = ebook_df['rate'].fillna('평점 없음')
    # introduce 변수값 중 na값에 빈칸 채우기
    ebook_df['introduce'] = ebook_df['introduce'].fillna('')
    # 도서에 대한 컨텐츠(소개글, 저자명, 출판사, 대분류, 소분류)를 하나로 합치기
    ebook_df['soup'] = ebook_df.apply(create_soup, axis=1)
    # 한글, 영문, 숫자만 남기고 모두 제거
    ebook_df['soup_clean'] = ebook_df['soup'].apply(clean_text)
    # price변수의 한글 제거
    ebook_df['price'] = ebook_df['price'].apply(remove_won)

    # tfidf를 이용한 벡터화
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(ebook_df['soup_clean'])

    # 입력된 도서의 인덱스를 가져오기
    book_idx = ebook_df[ebook_df['title'] == title].index[0]
    # 코사인 유사도 계산
    cosine_sim = cosine_similarity(tfidf_matrix[book_idx], tfidf_matrix)
    # 모든 도서에 대해 해당 도서와의 유사도 계산 후 리스트로 저장
    sim_scores = list(enumerate(cosine_sim[0]))
    # 유사도에 따라 도서들을 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:13]
    # 가장 유사한 도서 12개의 인덱스 가져오기
    book_indices = [i[0] for i in sim_scores]
    # 인덱스에 해당하는 도서 리스트트 반환
    return ebook_df.iloc[book_indices]
