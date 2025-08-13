import requests
from bs4 import BeautifulSoup
import csv
import json

# URL of the HTML page
url = "https://baraasalout.github.io/test.html"

# Fetch the HTML content
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")

# =====================
# 1. Extract Text Data
# =====================
text_data = []

# Extract h1 and h2
for tag in soup.find_all(["h1", "h2"]):
    text_data.append(["heading", tag.get_text(strip=True)])

# Extract p and li
for tag in soup.find_all(["p", "li"]):
    text_data.append([tag.name, tag.get_text(strip=True)])

# Save to CSV
with open("Extract_Text_Data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Tag", "Text"])
    writer.writerows(text_data)

# =====================
# 2. Extract Table Data
# =====================
table_data = []
table = soup.find("table")
if table:
    rows = table.find_all("tr")[1:]  # skip header
    for row in rows:
        cols = row.find_all("td")
        product_name = cols[0].get_text(strip=True)
        price = cols[1].get_text(strip=True)
        stock = cols[2].get_text(strip=True)
        table_data.append([product_name, price, stock])

# Save to CSV
with open("Extract_Table_Data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Product Name", "Price", "Stock Status"])
    writer.writerows(table_data)

# ================================
# 3. Extract Product Information
# ================================
products_info = []
cards = soup.select(".book-card")
for card in cards:
    title = card.find("h3").get_text(strip=True)
    price = card.find(class_="price").get_text(strip=True)
    stock = card.find(class_="stock").get_text(strip=True)
    button_text = card.find("button").get_text(strip=True)
    products_info.append({
        "Book Title": title,
        "Price": price,
        "Stock Availability": stock,
        "Button Text": button_text
    })

with open("Product_Information.json", "w", encoding="utf-8") as f:
    json.dump(products_info, f, indent=4)

# ========================
# 4. Extract Form Details
# ========================
form_details = []
form = soup.find("form")
if form:
    inputs = form.find_all("input")
    for inp in inputs:
        form_details.append({
            "Field Name": inp.get("name"),
            "Input Type": inp.get("type"),
            "Default Value": inp.get("value", "")
        })

with open("Form_Details.json", "w", encoding="utf-8") as f:
    json.dump(form_details, f, indent=4)

# ============================
# 5. Extract Video Link
# ============================
video_info = {}
iframe = soup.find("iframe")
if iframe:
    video_info["Video Link"] = iframe.get("src")

with open("Video_Link.json", "w", encoding="utf-8") as f:
    json.dump(video_info, f, indent=4)

# =================================
# 6. Featured Products Challenge
# =================================
featured_products = []
featured_section = soup.select(".featured-product")
for product in featured_section:
    product_id = product.get("data-id")
    name = product.find("span", class_="name").get_text(strip=True)
    price = product.find("span", class_="price").get_text(strip=True)
    colors = product.find("span", class_="colors").get_text(strip=True)
    featured_products.append({
        "id": product_id,
        "name": name,
        "price": price,
        "colors": colors
    })

with open("Featured_Products.json", "w", encoding="utf-8") as f:
    json.dump(featured_products, f, indent=4)

print("✅ All files have been created successfully!")
