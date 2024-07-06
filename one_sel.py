from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver as per your configuration
webdriver_service = Service("C:/Program Files/chromedriver.exe")  # Change this path to your chromedriver location

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# URL to scrape
url = "https://www.1mg.com/categories/health-conditions/derma-care-1183"
driver.get(url)

# Give the page some time to load
driver.implicitly_wait(10)  # seconds

# Parse the rendered HTML with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the driver
driver.quit()

# Find the main container
main_container = soup.find('div', class_='style__sku-list-container___3s_JF')

if main_container:
    print("Main container found.")
    
    # Find the sub container
    sub_container = main_container.find('div', class_='row style__grid-container___1Xvb-')
    
    if sub_container:
        
        # Initialize a list to hold the scraped data
        products_data = []
        
        # Loop through each product container
        for container in sub_container.find_all('div', class_='col-md-3 col-sm-4 col-xs-6 style__container___1TL2R'):
            print("Product container found.")
            
            # Extract product details
            product_box = container.find('div', class_='style__product-box___liepi')
            if product_box:
                product_name = product_box.find('div', class_='style__pro-title___2QwJy')
                mrp = product_box.find('span', class_='style__discount-price___25Bya')
                original_price = product_box.find('div', class_='style__price-tag___cOxYc')
                image_tag = product_box.find('img', class_='style__image___Ny-Sa style__loaded___22epL')
                
                # Ensure each element exists before trying to access it
                product_name_text = product_name.get_text(strip=True) if product_name else 'N/A'
                mrp_text = mrp.get_text(strip=True) if mrp else 'N/A'
                original_price_text = original_price.get_text(strip=True) if original_price else 'N/A'
                image_url = image_tag['src'] if image_tag else 'N/A'
                
                # Append the product details to the list
                products_data.append({
                    'Product Name': product_name_text,
                    'MRP': mrp_text,
                    'Original Price': original_price_text,
                    'Image URL': image_url
                })
                print(f"Scraped: {product_name_text}, {mrp_text}, {original_price_text}, {image_url}")
        
        # Convert the list to a DataFrame
        df = pd.DataFrame(products_data)
        
        # Write the DataFrame to a CSV file
        df.to_csv('products_data.csv', index=False)
        print("Data has been written to 'products_data.csv'")
    else:
        print("Sub container not found. Please check the class name or the structure of the webpage.")
else:
    print("Main container not found. Please check the class name or the structure of the webpage.")
