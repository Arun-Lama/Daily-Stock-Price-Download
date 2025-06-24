# Daily Stock Price Downloader 🚀

[![GitHub Actions Status](https://github.com/Arun-Lama/Daily-Stock-Price-Download/workflows/Daily%20Stock%20Update/badge.svg)](https://github.com/Arun-Lama/Daily-Stock-Price-Download/actions)

A Python automation tool that scrapes daily stock prices from [Sharesansar](https://www.sharesansar.com/) and appends them to a historical dataset in Google Sheets. The entire process runs automatically via **GitHub Actions** on a daily schedule.

📊 **[View Live Google Sheet](https://docs.google.com/spreadsheets/d/1n_QX2H3HEM1wYbEQmHV4fYBwfDzd19sBEiOv4MBXrFo/edit?gid=1092951433)**

## Features ✨
- Automated daily scraping of Nepalese stock prices  
- Clean data processing & validation  
- Automatic Google Sheets updates  
- GitHub Actions automation (3:15 PM NPT)  
- Error handling & logging  

## Installation 🛠️
```bash
git clone https://github.com/Arun-Lama/Daily-Stock-Price-Download.git
cd Daily-Stock-Price-Download
pip install -r requirements.txt
cp .env.example .env  # Configure your credentials
