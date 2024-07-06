import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage to scrape
url = "https://www.1mg.com/categories/health-conditions/derma-care-1183"

# Send a GET request to fetch the webpage content
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the webpage content
soup = BeautifulSoup(response.content, 'html.parser')

# # Find the main container containing all the products
# main_container = soup.select_one('.row.style_grid-container__1Xvb-')
# main_container = soup.select_one('.style__sku-list-container___3s_JF')
# main_container = soup.select_one('.col-xs-12 col-md-10 col-sm-9')
main_container = soup.select_one('.col-xs-12 col-md-10 col-sm-9')

# Check if the main container was found
if not main_container:
    print("Main container not found.")
else:
    # Initialize a list to store product data
    products_data = []

    # Iterate through each product container inside the main container
    for product_container in main_container.select('.col-md-3.col-sm-4.col-xs-6.style_container__1TL2R'):
        # Initialize variables for image link, product name, MRP, and original price
        image_link = product_name = mrp = original_price = 'N/A'
        
        # Check if image_tag exists before accessing src attribute
        image_tag = product_container.select_one('.style_image_Ny-Sa.styleloaded__22epL')
        if image_tag and 'src' in image_tag.attrs:
            image_link = image_tag['src']
        
        # Find product name
        name_tag = product_container.select_one('.style_pro-title__2QwJy')
        product_name = name_tag.get_text(strip=True) if name_tag else 'N/A'
        
        # Find MRP
        mrp_tag = product_container.select_one('.style_discount-price__25Bya')
        mrp = mrp_tag.get_text(strip=True) if mrp_tag else 'N/A'
        
        # Find original price
        original_price_tag = product_container.select_one('.style_price-tag__cOxYc')
        original_price = original_price_tag.get_text(strip=True) if original_price_tag else 'N/A'
        
        # Append the extracted data to the products_data list
        products_data.append([product_name, mrp, original_price, image_link])

    # Define the CSV file name
    csv_file = 'products_data.csv'

    # Write the data to the CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Product Name', 'MRP', 'Original Price', 'Image Link'])
        # Write the data
        writer.writerows(products_data)

    print(f"Data has been written to {csv_file}")