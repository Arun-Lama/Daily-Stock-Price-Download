# Daily Stock Price Downloader 🚀

GitHub Actions Status: [Workflow](https://github.com/Arun-Lama/Daily-Stock-Price-Download/actions)

🐍 Python 3.8+: [![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)  
📜 License: [![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python automation tool that scrapes daily Nepalese stock prices from [Sharesansar](https://www.sharesansar.com/) and updates a historical dataset in Google Sheets. The entire process runs automatically via GitHub Actions on a daily schedule.

📊 **[View Live Google Sheet](https://docs.google.com/spreadsheets/d/1n_QX2H3HEM1wYbEQmHV4fYBwfDzd19sBEiOv4MBXrFo/edit?gid=1092951433)**

## Features ✨

- 🕒 Automated daily scraping of NEPSE stock data
- 📈 Clean data processing with pandas
- 🔄 Automatic Google Sheets synchronization
- 🤖 Headless browser operation with Selenium
- 📅 Scheduled execution via GitHub Actions (3:15 PM NPT daily)
- 🔒 Secure credential management with environment variables
- 📝 Comprehensive logging

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Google Cloud Platform service account
- Access to Sharesansar

### Step 1: Clone the Repository
```bash
git clone https://github.com/Arun-Lama/Daily-Stock-Price-Download.git
cd Daily-Stock-Price-Download
