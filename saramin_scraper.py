import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# 사람인에서 검색할 키워드와 옵션 설정
KEYWORDS = ["frontend", "backend"]
SEARCH_OPTION = "&exp_cd=1"  # 신입

# 웹 서버에 요청 시 브라우저처럼 보이게 하기 위한 User-Agent 설정
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_saramin_jobs():
    """사람인에서 주어진 키워드로 신입 채용 공고를 스크랩하여 CSV 파일로 저장"""
    
    print("스크래핑을 시작합니다...")
    
    jobs_list = []
    for keyword in KEYWORDS:
        try:
            print(f"키워드 '{keyword}' (신입) 공고를 검색합니다...")
            
            # 키워드와 옵션을 포함한 URL 생성
            url = f"https://www.saramin.co.kr/zf_user/search?search_action=search&search_optional_item=n&searchword={keyword}{SEARCH_OPTION}"
            
            # URL에 GET 요청
            response = requests.get(url, headers=HEADERS)
            # 요청이 성공했는지 확인 (상태 코드가 200이 아니면 에러 발생)
            response.raise_for_status()

            # BeautifulSoup 객체 생성
            soup = BeautifulSoup(response.text, "html.parser")

            # 채용 공고 목록 선택
            recruit_items = soup.find_all("div", class_="item_recruit")

            # 각 공고를 순회하며 정보 추출
            for item in recruit_items:
                # 공고 제목
                title_element = item.find("h2", class_="job_tit").find("a")
                title = title_element.get_text(strip=True)
                
                # 상세 정보 링크 (상대 경로를 절대 경로로 변환)
                link = "https://www.saramin.co.kr" + title_element["href"]

                # 회사명
                company_name = item.find("strong", class_="corp_name").get_text(strip=True)

                # 근무 조건
                job_condition = item.find("div", class_="job_condition").get_text(strip=True).replace("\n", " | ")

                # 마감일
                deadline = item.find("span", class_="date").get_text(strip=True)

                # 추출한 정보를 딕셔너리로 저장
                job_info = {
                    "검색 키워드": keyword,
                    "회사명": company_name,
                    "공고 제목": title,
                    "근무 조건": job_condition,
                    "마감일": deadline,
                    "상세 링크": link
                }
                jobs_list.append(job_info)

            # 다음 요청 전에 랜덤한 시간 지연 추가 (서버 부하 감소)
            sleep_time = random.uniform(1, 3)
            print(f"다음 요청까지 {sleep_time:.2f}초 대기합니다...")
            time.sleep(sleep_time)

        except requests.exceptions.RequestException as e:
            print(f"오류 발생 (키워드: {keyword}): {e}")
        except Exception as e:
            print(f"알 수 없는 오류 발생 (키워드: {keyword}): {e}")

    if not jobs_list:
        print("수집된 채용 공고가 없습니다.")
        return

    # pandas DataFrame으로 변환
    df = pd.DataFrame(jobs_list)
    
    # 중복된 공고 제거 (링크 기준)
    df.drop_duplicates(subset=["상세 링크"], keep="first", inplace=True)

    # CSV 파일로 저장 (UTF-8-BOM 인코딩으로 한글 깨짐 방지)
    output_filename = "saramin_junior_dev_jobs.csv"
    df.to_csv(output_filename, index=False, encoding="utf-8-sig")

    print(f"스크래핑 완료! '{output_filename}' 파일이 생성되었습니다. (총 {len(df)}개 공고)")


if __name__ == "__main__":
    scrape_saramin_jobs()
