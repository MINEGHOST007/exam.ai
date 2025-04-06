from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

def scrape_shl_catalog():
    # Setup Chrome options
    options = Options()
    options.headless = True
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    all_solutions = []
    page_num = 1
    start = 1
    has_next_page = True
    
    while has_next_page:
        try:
            # Initialize the WebDriver for each page to avoid memory issues
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            
            # Construct URL with pagination parameter
            # url = f"https://www.shl.com/solutions/products/product-catalog/?type=1&start={start}&type=1"
            url = f"https://www.shl.com/solutions/products/product-catalog/?type=2&start={start}&type=2"
            
            print(f"Scraping page {page_num}, URL: {url}")
            
            driver.get(url)
            
            # Wait for table to be present
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "table"))
                )
                
                # Parse page source directly without saving to file
                soup = BeautifulSoup(driver.page_source, "lxml")
                table = soup.find("table")
                
                if table:
                    # Get all rows except the header row
                    rows = table.find("tbody").find_all("tr")
                    
                    if not rows:
                        print("No rows found on this page. Ending pagination.")
                        has_next_page = False
                        break
                    
                    for row in rows:
                        # Extract solution name and URL
                        solution_cell = row.find("td", class_="custom__table-heading__title")
                        if solution_cell and solution_cell.find("a"):
                            solution_link = solution_cell.find("a")
                            solution_name = solution_link.text.strip()
                            solution_url = "https://www.shl.com" + solution_link.get("href")
                            
                            # Check for Remote Testing
                            remote_cell = row.find_all("td", class_="custom__table-heading__general")[0]
                            remote_testing = bool(remote_cell.find("span", class_="catalogue__circle -yes"))
                            
                            # Check for Adaptive/IRT
                            adaptive_cell = row.find_all("td", class_="custom__table-heading__general")[1]
                            adaptive_irt = bool(adaptive_cell.find("span", class_="catalogue__circle -yes"))
                            
                            # Get test types
                            types_cell = row.find("td", class_="custom__table-heading__general product-catalogue__keys")
                            test_types = []
                            if types_cell:
                                type_elements = types_cell.find_all("span", class_="product-catalogue__key")
                                test_types = [elem.text for elem in type_elements]
                            
                            # Add to our collection
                            all_solutions.append({
                                "name": solution_name,
                                "url": solution_url,
                                "remote_testing": remote_testing,
                                "adaptive_irt": adaptive_irt,
                                "test_types": ', '.join(test_types)
                            })
                else:
                    print(f"Table not found on page {page_num}")
                    has_next_page = False
                    break
        
            except TimeoutException:
                print(f"Timeout waiting for table on page {page_num}. Ending pagination.")
                has_next_page = False
                break
            
            # Prepare for next page
            page_num += 1
            start = (page_num - 1) * 12   # Each page shows 12 items
            
            # Optional: Add a condition to limit pages for testing
            if page_num > 32:  # Limit to 32 pages
                has_next_page = False
                
        except Exception as e:
            print(f"Error on page {page_num}: {str(e)}")
            has_next_page = False
        finally:
            # Close the browser for this page
            driver.quit()
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(all_solutions)
    df.to_csv("shl_solutions_catalog2.csv", index=False)
    print(f"Saved {len(all_solutions)} solutions to shl_solutions_catalog.csv")
    
    return all_solutions

if __name__ == "__main__":
    solutions = scrape_shl_catalog()
    print(f"Total solutions scraped: {len(solutions)}")