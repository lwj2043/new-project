import requests
import json
import time
import pandas as pd
import os

def get_webtoons_and_save_csv(day_of_week):
    """
    네이버 웹툰 API를 사용하여 특정 요일의 웹툰 제목 목록을 CSV 파일로 저장하는 함수.
    
    Args:
        day_of_week (str): 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun' 중 하나
    """
    
    api_urls = {
        'mon': 'https://comic.naver.com/api/webtoon/titlelist/weekday?week=mon&page=1&per_page=100',
        'tue': 'https://comic.naver.com/api/webtoon/titlelist/weekday?week=tue&page=1&per_page=100',
        'wed': 'https://comic.naver.com/api/webtoon/titlelist/weekday?week=wed&page=1&per_page=100',
        'thu': 'https://comic.naver.com/api/webtoon/titlelist/weekday?week=thu&page=1&per_page=100',
        'fri': 'https://comic.naver.com/api/webtoon/titlelist/weekday?week=fri&page=1&per_page=100',
        'sat': 'https://comic.naver.com/api/webtoon/titlelist/weekday?week=sat&page=1&per_page=100',
        'sun': 'https://comic.naver.com/api/webtoon/titlelist/weekday?week=sun&page=1&per_page=100'
    }

    if day_of_week.lower() not in api_urls:
        print("유효하지 않은 요일입니다. 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun' 중 하나를 입력하세요.")
        return

    url = api_urls[day_of_week.lower()]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        time.sleep(1)
        
        if response.status_code == 200:
            data = response.json()
            
            # API 응답에서 'titleList' 키를 사용하여 목록을 가져옵니다.
            webtoon_list = data.get('titleList')
            
            if webtoon_list:
                # 제목만 추출하여 새로운 리스트를 만듭니다.
                titles = [item.get('titleName') for item in webtoon_list if item.get('titleName')]
                
                # 추출한 제목 리스트를 데이터프레임으로 변환
                df = pd.DataFrame(titles, columns=['Title'])
                
                # CSV 파일로 저장
                filename = f"naver_webtoons_{day_of_week}.csv"
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                
                print(f"✅ {day_of_week.upper()}요일 웹툰 제목 목록이 '{filename}' 파일로 저장되었습니다.")
            else:
                print(f"({day_of_week.upper()}요일) 웹툰 목록을 찾을 수 없습니다. 'titleList' 키가 없거나 비어 있습니다.")
        else:
            print(f"API에 접근할 수 없습니다. 상태 코드: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON 디코딩 오류 발생: {e}")
    except KeyError as e:
        print(f"JSON 데이터에 필요한 키가 없습니다: {e}")

# 함수 실행 예시
get_webtoons_and_save_csv('tue')