import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from read_write_google_sheet import read_google_sheet, write_to_google_sheet
from datetime import timedelta


def download_price(google_sheet_id):
    data = read_google_sheet(google_sheet_id)
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d', errors='coerce')
    data.sort_values(by='Date', ascending=True, inplace=True)
    latest_data_available = data['Date'].dropna().iloc[-1]
    print(f'Latest available data on excel file is as of {latest_data_available.strftime("%Y-%m-%d")}')
    date_to_start_scraping_from = latest_data_available + timedelta(days=1)
    today = pd.to_datetime("today").normalize()
    dates = pd.date_range(start=date_to_start_scraping_from, end=today)
    dates = [d for d in dates if d.isoweekday() not in [5, 6]]
    if dates:
        print(f'Downloading stock data from {dates[0].strftime("%Y-%m-%d")} to {dates[-1].strftime("%Y-%m-%d")}')
    else:
        print("No dates to scrape — all within weekend range.")
      
    # Setup Chrome options to run headless and disable images
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("window-size=1920,1080")  # Set the window size for consistency
    
    # Disable images
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get('https://www.sharesansar.com/today-share-price')
    
    blank_df = []
    for date in dates:
        driver.find_element(By.XPATH, '//*[@id="fromdate"]').clear()
        driver.find_element(By.XPATH, '//*[@id="fromdate"]').send_keys(f'{date.date()}')
        driver.find_element(By.XPATH, '//*[@id="btn_todayshareprice_submit"]').click()
    
        # Wait for the loading indicator to appear
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'loading'))
        )
    
        # Wait for the loading indicator to disappear
        WebDriverWait(driver, 60).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'loading'))
        )
    
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        todays_price = soup.find('table', id='headFixed')
    
        if len(todays_price.find_all('tr')) >= 10:
            output_rows = []
            for table_row in todays_price.find_all('tr')[1:]:
                columns = table_row.find_all('td')
                output_row = [column.text.strip() for column in columns]
                output_rows.append(output_row)
    
            headers_list = [header.text.strip() for header in todays_price.find_all('th')]
            
            if output_rows:
                todays_price_dataframe = pd.DataFrame(output_rows, columns=headers_list)
                todays_price_dataframe['Symbol'] = todays_price_dataframe['Symbol'].str.replace("\n", "")
                todays_price_dataframe.set_index('S.No', inplace=True)
                todays_price_dataframe['Date'] = date.date()
                blank_df.append(todays_price_dataframe)    
    driver.quit()
    
    if len(blank_df) == 0:
        print("Stock data is up to date, no need to download!")
        return []
    else:
        # Concatenate DataFrames
        df = pd.concat(blank_df)

        # Continue processing if DataFrame is not empty
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        df = df[['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Vol', 'Turnover', 'Trans.']]

        columns_except_symbol = df.columns.difference(['Date', 'Symbol'])
        df[columns_except_symbol] = df[columns_except_symbol].replace(',', '', regex=True).astype(float)

        stock_price_history = df
        return stock_price_history
    

price_history_sheet_id = "1n_QX2H3HEM1wYbEQmHV4fYBwfDzd19sBEiOv4MBXrFo"
downloaded_price_history = download_price(price_history_sheet_id)
from datetime import datetime

dateti = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if  len(downloaded_price_history) != 0:
    write_to_google_sheet(downloaded_price_history, price_history_sheet_id, mode='append')
    