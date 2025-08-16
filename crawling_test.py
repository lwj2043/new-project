import asyncio
import pandas as pd
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def get_naver_webtoons():
    """
    Playwright를 사용하여 네이버 웹툰의 요일별 제목을 안정적으로 스크래ping하고
    하나의 CSV 파일로 저장합니다.
    """
    # 네이버 웹툰은 월(mon)부터 일(sun)요일 및 신작(dailyPlus)으로 구성됩니다.
    days_of_week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun", "dailyPlus"]
    all_webtoons_data = []  # 모든 웹툰 데이터를 저장할 최종 리스트

    print("🚀 네이버 웹툰 스크래핑을 시작합니다...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for day in days_of_week:
            # 1. 최신 URL 구조를 사용합니다.
            url = f"https://comic.naver.com/webtoon?tab={day}"
            print(f"\n[{day.upper()}] 페이지로 이동 중... ({url})")
            
            try:
                await page.goto(url)

                # 2. 현재 시점의 정확한 선택자를 변수로 지정합니다.
                # 이 부분은 웹사이트 구조가 바뀌면 수정이 필요할 수 있습니다.
                webtoon_title_selector = "span.ContentTitle__title--e3qXt"

                # 3. 페이지 로딩을 기다리되, 타임아웃 에러를 대비합니다. (가장 중요!)
                # wait_for_selector는 해당 요소가 나타날 때까지 지정된 시간만큼 기다립니다.
                await page.wait_for_selector(webtoon_title_selector, timeout=15000) # 15초 대기

                # 4. locator를 사용해 페이지에 있는 모든 웹툰 제목을 가져옵니다.
                titles = await page.locator(webtoon_title_selector).all_inner_texts()

                if titles:
                    print(f"✅ [{day.upper()}] {len(titles)}개의 웹툰을 찾았습니다!")
                    for title in titles:
                        # 요일 정보와 제목을 함께 딕셔너리로 만들어 리스트에 추가합니다.
                        all_webtoons_data.append({"Day": day.upper(), "Title": title})
                else:
                    # 요소는 찾았으나 비어있는 경우 (일어날 확률은 낮음)
                    print(f"🤔 [{day.upper()}] 웹툰 목록을 찾았지만, 제목이 비어있습니다.")

            except PlaywrightTimeoutError:
                # 15초 동안 선택자를 찾지 못하면 TimeoutError가 발생합니다.
                print(f"❌ [{day.upper()}] 페이지에서 웹툰 요소를 찾는 데 실패했습니다. (Timeout)")
                print("-> 페이지 구조가 변경되었거나, 네트워크 문제일 수 있습니다.")
                continue  # 현재 요일은 건너뛰고 다음 요일로 계속 진행합니다.
            
            except Exception as e:
                # 그 외 예기치 못한 에러 처리
                print(f"🚨 [{day.upper()}] 알 수 없는 에러가 발생했습니다: {e}")
                continue

        await browser.close()

    # 5. 수집된 모든 데이터를 하나의 DataFrame으로 변환 후 CSV 파일로 저장합니다.
    if all_webtoons_data:
        df = pd.DataFrame(all_webtoons_data)
        filename = "naver_webtoons_list.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"\n🎉 모든 작업 완료! '{filename}' 파일에 총 {len(all_webtoons_data)}개의 웹툰이 저장되었습니다.")
    else:
        print("\n아무런 웹툰 데이터도 수집하지 못했습니다. 선택자를 다시 확인해보세요.")


# 스크립트 실행
if __name__ == "__main__":
    asyncio.run(get_naver_webtoons())