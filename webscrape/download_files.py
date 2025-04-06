import os
import requests
import urllib.parse
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def download_file(url, destination_folder, filename=None):
    """Download a file from a URL to the specified folder."""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        if not filename:
            filename = os.path.basename(urllib.parse.unquote(url)).replace(" ", "_").replace("%20", "_")

        file_path = os.path.join(destination_folder, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def scrape_product_details(csv_file="shl_solutions_catalog2.csv", downloads_folder="downloads"):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file}")
        return

    options = Options()
    options.headless = True
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)

    all_product_details = []

    for index, row in df.iterrows():
        product_url = row['url']
        product_name = row['name']

        print(f"Processing {index + 1}/{len(df)}: {product_name}")

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(product_url)

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "container"))
            )

            soup = BeautifulSoup(driver.page_source, "lxml")

            product_details = {
                "name": product_name,
                "url": product_url,
                "description": "",
                "job_levels": "",
                "languages": "",
                "assessment_length": "",
                "test_types": "",
                "remote_testing": "",
                "downloads": []
            }

            sections = soup.find_all("div", class_="product-catalogue-training-calendar__row")
            for section in sections:
                heading = section.find("h4")
                if not heading:
                    continue
                heading_text = heading.text.strip().lower()
                content_p = section.find("p")

                if heading_text == "description" and content_p:
                    product_details["description"] = content_p.text.strip()

                elif heading_text == "job levels" and content_p:
                    product_details["job_levels"] = content_p.text.strip()

                elif heading_text == "languages" and content_p:
                    product_details["languages"] = content_p.text.strip()

                elif heading_text == "assessment length" and content_p:
                    product_details["assessment_length"] = content_p.text.strip()

                elif heading_text == "downloads":
                    download_items = section.find_all("li", class_="product-catalogue__download")
                    for item in download_items:
                        link_tag = item.find("a", href=True)
                        if link_tag:
                            download_url = urllib.parse.urljoin(product_url, link_tag['href'])
                            download_name = link_tag.text.strip()
                            product_details["downloads"].append({
                                "name": download_name,
                                "url": download_url
                            })

                            file_ext = os.path.splitext(download_url)[1]
                            safe_name = product_name.replace("/", "_").replace("\\", "_").replace(":", "_")
                            file_name = f"{safe_name}_{download_name}{file_ext}"
                            download_file(download_url, downloads_folder, file_name)

            # Extract test types and remote testing indicators
            assess_section = soup.find("h4", string="Assessment length")
            if assess_section:
                parent = assess_section.find_parent("div", class_="product-catalogue-training-calendar__row")
                if parent:
                    keys = parent.select("span.product-catalogue__key")
                    product_details["test_types"] = ", ".join(k.text.strip() for k in keys)

                    remote_span = parent.find("span", class_="catalogue__circle -yes")
                    product_details["remote_testing"] = "Yes" if remote_span else "No"

            all_product_details.append(product_details)

        except TimeoutException:
            print(f"Timeout loading page: {product_url}")
        except Exception as e:
            print(f"Error scraping {product_url}: {e}")
        finally:
            driver.quit()
            time.sleep(1)

    # Save all details
    details_df = pd.DataFrame(all_product_details)
    details_df.to_csv("shl_product_details2.csv", index=False)
    print(f"Saved details for {len(all_product_details)} products to shl_product_details.csv")

    return all_product_details

if __name__ == "__main__":
    scrape_product_details()
