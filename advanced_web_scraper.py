import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Banner
print("""
============================================================
          Advanced Web Scraper with Selenium
          Coded by Pakistani Ethical Hacker: Mr. Sabaz Ali Khan
          Date: {}
============================================================
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def initialize_driver():
    """Initialize Chrome WebDriver with options."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape_quotes():
    """Scrape quotes from quotes.toscrape.com."""
    driver = initialize_driver()
    url = "http://quotes.toscrape.com"
    driver.get(url)
    
    quotes_data = []
    page = 1
    
    try:
        while True:
            print(f"Scraping page {page}...")
            
            # Wait for quotes to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
            )
            
            # Scroll to bottom to ensure all dynamic content loads
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Allow time for dynamic content
            
            # Find all quote elements
            quotes = driver.find_elements(By.CLASS_NAME, "quote")
            
            for quote in quotes:
                try:
                    # Extract quote text, author, and tags
                    text = quote.find_element(By.CLASS_NAME, "text").text
                    author = quote.find_element(By.CLASS_NAME, "author").text
                    tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]
                    
                    quotes_data.append({
                        "quote": text,
                        "author": author,
                        "tags": ", ".join(tags)
                    })
                except NoSuchElementException as e:
                    print(f"Error extracting quote: {e}")
                    continue
            
            # Check for next page
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.next > a")
                next_button.click()
                page += 1
                time.sleep(2)  # Wait for page to load
            except NoSuchElementException:
                print("No more pages to scrape.")
                break
                
    except TimeoutException:
        print("Timeout while loading page.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    
    return quotes_data

def save_to_csv(data, filename="quotes.csv"):
    """Save scraped data to a CSV file."""
    if not data:
        print("No data to save.")
        return
    
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")

def main():
    """Main function to run the scraper."""
    try:
        # Scrape quotes
        quotes_data = scrape_quotes()
        
        # Save to CSV
        save_to_csv(quotes_data)
        
        # Print summary
        print(f"Scraped {len(quotes_data)} quotes successfully.")
        
    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()