'''
작업 제목: 자바스크립트로 된 데이터를 긁어오고 싶을때! Selenium+BeautifulSoup을 사용한 Web Scraping
출처: [프로그래머 김플] 파이썬 인스타그램 크롤링 이미지 다운로드 beautifulsoup, selenium 사용법(3년전 유튜브 강의 -> 개인적으로 업데이트)
출처 링크: https://www.youtube.com/watch?v=j_BW5vNrcxA&list=PL5bK87xH5V1wKF4ErEB0X4Ltu6kAlBB7X&index=21

목표  : 인스타그램에 아이유라고 검색했을때 나올 이미지 21장을 주르륵 가져오자!
특이점: 설명이미지1에서 보는 화면의 거의 대부분(우클릭>페이지소스보기>하면 다 자바인것을 볼 수 있음) 뷰티풀숩으로는 원하는 걸 가져올 수가 없다.
       그래서 셀레늄으로 페이지 띄워서, 띄운 페이지의 소스를 얻어 그걸 가지고 soup 객체를 만들어야 하는 case(굉장히 보편적인 사례라 함)
'''

from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os



# 스크랩할 타겟 url 지정하기
# 예를 들어 아이유를 hashtag로 하는 이미지들을 볼 수 있는 인스타그램 페이지를 구글에서 찾으면 다음 주소의 페이지를 찾을 수 있음
# https://www.instagram.com/explore/tags/%EC%95%84%EC%9D%B4%EC%9C%A0/
# /tags/<--이부분-->/ 이부분은 "아이유"가 ascii code로 변환된 부분
# 검색 키워드별로 변하지 않는 부분과 변하는 부분으로 나누어 좀 더 응용 가능한 코드로 작성
baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input('원하는 검색 태그를 입력하세요:  ')
url = baseUrl + quote_plus(plusUrl)
### quote_plus() 설명: https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse
print(url)



# selenium의 webdriver로 위에서 지정한 url을 띄우고 띄운 페이지의 페이지 소스 가져오기(이렇게 하면 자바인게 더 이상 문제되지 않음)
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)
html = driver.page_source



# 가져온 소스를 BeautifulSoup에 넣어 soup 객체로 바꿔주고, 그 뒤로는 BeautifulSoup을 이용해서 스크래핑
soup = BeautifulSoup(html, features="lxml")
insta = soup.select('._aabd._aa8k._aanf')
### soup.select(): https://computer-science-student.tistory.com/235
### 인자에 태그명을 넣고 싶으면 "태그명", 클래스이름을 넣고 싶으면 ".클래스이름", 아이디를 넣고 싶으면 "#아이디"
### class="_aabd._aa8k._aanf" 인 tag들을 soup에서 뽑아서 insta로 저장했는지는 스크린샷에...


# 사진들을 저장할 image라는 이름의 폴더(현디랙토리에)를 만들어 주기
os.mkdir("image")
### 함수 설명: https://blockdmask.tistory.com/554



# 현재 insta라는 변수 안에는 같은 계위의 태그들이 리스트로 모여있음, 리스트 원소? 하나 당 사진 하나씩 가져오게 되는 것
n =1
for i in insta: # 겁나면 insta[:3] 등으로 몇개씩만 테스트하면서 돌려보기
    print('https://www.instagram.com'+i.a["href"]) # href에는 목표하는 그 이미지가 있는 포스팅으로 갈 수 있게 해주는 상대주소가 들어있음(그냥 뭔가를 눈으로 보려고 하는 작업)
    imgUrl=i.select_one('._aagv').img['src'] # 원하는 img를 포함하는 윗 태그(=_aagv를 클래스이름으로 같는 태그)의 밑에 img에 'src'링크를 imgURL(리스트)로 가져와라
    ### 밑에 네 줄은 그냥 킵해뒀다가 유알엘 받은 것들 저장하는 코드로 기계적으로 써야할 듯
    with urlopen(imgUrl) as response:
        with open('./image/'+ plusUrl + str(n)+'.jpg','wb') as file:
            print(response.getcode()) # 200으로 허락받은 짓인지 확인
            img = response.read() # 이경우 url이 img scr이었어서 response를 read한 결과가 img인 듯, 보통은 html로 받더라
            file.write(img)
    ### 이게 뭘까... 밑으로 해도 똑같이 돌아감
    ### img = urlopen(imgUrl).read()
    ### open('./image/'+ plusUrl + str(n)+'.jpg','wb').write(img)
    n += 1
    print(imgUrl)
    print()
    ### 결과로 [원포스팅주소,이미지소스유알엘, 빈줄]이 한 세트로 21개 print 될 것임

driver.quit()
