from selenium import webdriver
from urllib.parse import quote_plus
from urllib.request import urlopen
import os


def save_images(images, save_path):
    for index, image in enumerate(images[:10]):  # images[:크롤링하고 싶은 사진 개수]
        src = image.get_attribute('src')
        t = urlopen(src).read()
        file = open(os.path.join(save_path, str(index + 1) + ".jpg"), "wb")
        file.write(t)
        print("img save " + save_path + str(index + 1) + ".jpg")


def create_folder_if_not_exists(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def make_url(search_term):
    # 네이버 이미지 검색
    base_url = 'https://search.naver.com/search.naver?where=image&section=image&query='
    # CCL 상업적 이용 가능 옵션
    end_url = '&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=2' \
              '&nso=so%3Ar%2Ca%3Aall%2Cp%3Aall&recent=0&datetype=0&startdate=0&enddate=0&gif=0&optStr=&nso_open=1'
    return base_url + quote_plus(search_term) + end_url


def crawl_images(search_term):
    # URL 생성
    url = make_url(search_term)

    # chrome 브라우저 열기
    browser = webdriver.Chrome('chromedriver')
    browser.implicitly_wait(3)  # 브라우저를 오픈할 때 시간간격을 준다.
    browser.get(url)

    # 이미지 긁어오기
    images = browser.find_elements_by_class_name("_image")

    # 저장 경로 설정
    save_path = "/Users/danuri/Desktop/images/" + search_term + "/"
    create_folder_if_not_exists(save_path)

    # 이미지 저장
    save_images(images, save_path)

    # 마무리
    print(search_term + " 저장 성공")
    browser.close()


if __name__ == '__main__':
    crawl_images(input('원하는 검색어: '))
