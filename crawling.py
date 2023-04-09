from bs4 import BeautifulSoup
import requests

def get_products_link(soup):
    '''
    Purpose : 각 도서 상세 페이지 링크를 추출하는 함수
    Input : 
        - soup : BeautifulSoup 객체로 변환한 html 코드(soup)
    Output : 각 도서의 상세 페이지 링크(list)
    '''
    book_html = soup.find_all("div",attrs={"class":"goodsImgW"})
    products_link = []

    for i in book_html:
        product_link = 'http://www.yes24.com' + i.find('a')['href']
        book_title = i.find('img')['alt']
        contents = {}
        contents['product_link'] = product_link
        contents['book_title'] = book_title
        products_link.append(contents)

    return products_link

#------------------------------------------------------------------

def get_books_detail(products_link):
    '''
    Purpose : 각 도서의 제목명, 저자명,출판사명, 중분류, 소분류 카테고리, 가격, 별점, 이미지 링크, 책 소개 글을 추출하는 함수
    Input : 
        - products_link : 상세 정보를 가져올 도서 구매 페이지 링크(str)
    Output : 각 도서의 상세 정보(list)
    '''
    book_detail_list = []

    for i in range(len(products_link)):
        response =requests.get(products_link[i]['product_link'])
        soup = BeautifulSoup(response.text, "html.parser")

        # 해당 상품이 '문구/GIFT'면 크롤링하지 않음
        if soup.find("div",attrs={'class':'gd_titArea'}).find('em',attrs={'class':'txt'}).get_text() == '문구/GIFT':
            continue

        else:
            print('*',i+1,'. <',products_link[i]['book_title'],'> \n수집 시작 ->')

        # 도서 제목 추출
        title_html = soup.find("h2", attrs={'class':'gd_name'})
        title = title_html.get_text().replace('[할인]','').replace('[대여]','').replace('[100% 페이백]','').replace('[단독]','').replace('[세트]','').replace('[ePub3.0]','').replace('(개정판)','') # 제목명
        print('--- 제목명 수집 완료')

        # 저자명 추출
        author_html = soup.find("span", attrs={'class':'gd_auth'})
        if (author_html.find('a') in author_html) == False :
            author = author_html.get_text().replace('\r\n','').replace('  ','').replace(',',' ')
        else :
            author = author_html.find('a').get_text() # 저자명

        # 출판사명 추출
        pub_html = soup.find("span", attrs={'class':'gd_pub'})
        publisher = pub_html.find('a').get_text() # 출판사명
        print('--- 출판사명 수집 완료')

        # 중분류 카테고리명 추출
        cat_html = soup.find("dl", attrs={'class':'yesAlertDl'})
        category1 = cat_html.find_all('a')[1].get_text() # 중분류 카테고리명
        print('--- 중분류 카테고리명 수집 완료')
        
        # 소분류 카테고리명 추출
        if len(cat_html.find_all('a')) < 3:
            category2 = "없음"
        else :
            category2 = cat_html.find_all('a')[2].get_text() # 소분류 카테고리명
        print('--- 소분류 카테고리명 수집 완료')

        # 가격 추출
        price_html = soup.find("em", attrs={'class':'yes_m'})
        price = price_html.get_text() # 가격
        print('--- 가격 수집 완료')

        # 별점 추출
        if soup.find("span", attrs={"class":"gd_reviewCount"}).find('a').get_text() == '첫번째 구매리뷰를 남겨주세요.' : # 리뷰가 없으면 별점 None으로 설정
            rate = None
        else :
            rate = float(soup.find("em", attrs={"class":"yes_b"}).get_text())
        print('--- 별점 수집 완료')

        # 도서 이미지 링크 추출
        book_img_html = soup.find("div", attrs={"class":"tp_book"})
        img_link = book_img_html.find('img')['src'].replace('XL','L') #이미지 사이즈 변경
        print('--- 이미지 링크 수집 완료')

        # 도서 소개글 추출
        intro_html = soup.find("textarea", attrs={'class':'txtContentText'})
        if intro_html == None: # 소개글이 없으면 None으로 설정
            intro_contents = None
        else:
            intro_contents = intro_html.get_text().replace('\r\n','').replace('                    ','').replace('</br>','').replace('\n','') # 책 소개
        print('--- 책 소개 수집 완료')
        
        # 추출한 도서의 상세 정보를 딕셔너리 형태로 저장
        detail = {}
        detail['title'] = title
        detail['author'] = author
        detail['publisher'] = publisher
        detail['category1'] = category1
        detail['category2'] = category2
        detail['price'] = price
        detail['rate'] = rate
        detail['product_link'] = products_link[i]['product_link']
        detail['img_link'] = img_link
        detail['introduce'] = intro_contents

        # 리스트에 각 도서의 상세 정보를 추가
        book_detail_list.append(detail)

        print('>>> 수집 완료')
        print('\n-------------------------------------------\n')

    return book_detail_list

#------------------------------------------------------------------

# 크롤링 실행
book_detail = []
for i in range(1,13):
    print('[',i,'번째 페이지 수집 시작 ]')
    print('\n===========================================\n')
    # 크롤링 할 도서 목록이 있는 페이지
    response = requests.get("http://www.yes24.com/24/category/bestseller?categorynumber=017&sumgb=06&fetchsize=80&ao=2&pagenumber="+str(i))
    soup = BeautifulSoup(response.text, "html.parser")

    # 페이지 내 도서 상세 페이지 링크 추출
    book_list = get_products_link(soup)
    # 도서 상세 페이지 내 해당 도서의 도서명, 저자명, 출판사명, 중분류, 소분류 카테고리명, 가격, 별점, 이미지 링크, 책 소개 크롤링
    book_detail_list = get_books_detail(book_list)
    
    book_detail.append(book_detail_list)
    print('[',i, '번째 페이지 수집 완료 ]')
    print('\n===========================================\n')

ebook_list = sum(book_detail,[])

#------------------------------------------------------------------

# 추출한 도서별 상세 정보 데이터 json파일로 저장
import json
with open('ebook_list.json','w') as file:
    json.dump(ebook_list, file)

