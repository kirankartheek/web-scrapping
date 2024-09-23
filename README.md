## Getting Started

To get started with this project, follow the instructions below to set up your environment and run the application.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/web-scrapper.git
   cd web-scrapper
2. **Create a virtual environment:**:
   ```bash
   python -m venv venv
   ```
    -  On macOS/Linux:
       ```bash
       source venv/bin/activate
       
    + On Windows
      ```bash
      venv\Scripts\activate
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up Redis:**
  - Ensure you have Redis installed and running on your local machine. You can download Redis from redis.io and follow the installation instructions.
  - Start Redis by running
  ```bash
      redis-server
   ```

# Usage
1. **Run the Application:**
  ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```
2. **Trigger the scraping process:** You can send a POST request to the API endpoint to start scraping:
   ```bash
   curl --location 'http://127.0.0.1:8000/api/scrape/products' \
   --header 'Content-Type: application/json' \
   --header 'token: your_token' \
   --data '{
       "pageLimit": 2,
       "proxy": ""
   }'
   ```
3. 

## Documentation

[`Web-Scrapper Application`](https://arrow-pullover-c0c.notion.site/WebScrapping-10af6fef3263802a9c76f2e3f68b0912?pvs=4)
