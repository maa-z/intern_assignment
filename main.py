import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np



headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'} 


# product_data = {
#     "Product URL" : [],
#     "Product Name" : [],
#     "Product Price" : [],
#     "Rating" : []
# }


# print("start")
# for i in range(1,21):


#     url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{str(i)}"
#     webpage=requests.get(url,headers=headers)
#     soup=BeautifulSoup(webpage.text,'lxml')


#     # Find all product containers inside the class "s-result-list"
#     product_containers = soup.find_all("div", class_="s-result-item")

#     # Extract and print tuples of product name, link, price, and rating
#     for product_container in product_containers:
#         product_name_element = product_container.find("span", class_="a-text-normal")
#         product_link_element = product_container.find("a", class_="a-link-normal")
#         product_price_element = product_container.find("span", class_="a-offscreen")
#         product_rating_element = product_container.find("span", class_="a-icon-alt")

#         if product_name_element and product_link_element and product_price_element and product_rating_element:
#             product_name = product_name_element.get_text()
#             product_link = product_link_element["href"]
#             full_product_link = "https://www.amazon.in" + product_link

#             # Fixing the product link for sponsored products
#             if "/spons/" in full_product_link:
#                 product_id = full_product_link.split("/dp/")[1].split("/")[0]
#                 full_product_link = f"https://www.amazon.in/dp/{product_id}"

#             product_price = product_price_element.get_text()
#             product_rating = product_rating_element.get_text()

#             product_data['Product URL'].append(full_product_link)
#             product_data['Product Price'].append(product_price)
#             product_data['Product Name'].append(product_name)
#             product_data['Rating'].append(product_rating[:3])


# df = pd.DataFrame(product_data)
# df.to_csv('file.csv',index=False)
# print("end")



df = pd.read_csv('file.csv')
df = df.drop_duplicates()

newdf = df


def myfun(a):
    print(a,end="\n\n")
    try:
        webpage=requests.get(a,headers=headers)
        soup=BeautifulSoup(webpage.text,'lxml')

        #review
        product_center = soup.find("div", class_="centerColAlign")
        product_total_review = product_center.find('span',id='acrCustomerReviewText')
        review = (product_total_review.text.split(" ")[0])

        #asin
        info = soup.find("div",id='productDetails_db_sections')
        asin = info.find('td',class_='a-size-base prodDetAttrValue')
        asin_number = asin.text.strip()

        #manufacture 
        technical_details = soup.find('table',id="productDetails_techSpec_section_1")
        trs = technical_details.find_all('tr')
        manu = ""
        for tr in trs:
            name = tr.find('th')
            if name.text.strip() == "Manufacturer":
                manufacture = tr.find('td').text
                manu = manufacture.strip()
                break

        
        #desc
        product_desc = product_center.find('div',id='feature-bullets')
        spans = product_desc.find_all('span',class_="a-list-item")
        desc = []
        for i in spans:
            desc.append(i.text)

        try:
            return review,asin_number,desc,manu
        except:
            return np.nan,np.nan,np.nan,np.nan
    except:
        print("not reach able")
        return np.nan,np.nan,np.nan,np.nan


try :
    newdf['Number of reviews'],newdf['ASIN'],newdf['Product Description'],newdf['Manufacture'] = zip(*newdf['Product URL'].map(myfun))
except:
    pass
newdf = newdf.dropna()
newdf.to_csv('final.csv',index=False)





















# product_center = soup.find("div", class_="centerColAlign")
# product_total_review = product_center.find('span',id='acrCustomerReviewText')
# print(product_total_review.text.split(" ")[0])


# info = soup.find("div",id='productDetails_db_sections')
# asin = info.find('td',class_='a-size-base prodDetAttrValue')
# print(asin.text.strip())


# technical_details = soup.find('table',id="productDetails_techSpec_section_1")
# trs = technical_details.find_all('tr')
# for tr in trs:
#     name = tr.find('th')
#     if name.text.strip() == "Manufacturer":
#         manufacture = tr.find('td').text
#         print(manufacture.strip())
#         break







# product_desc = product_center.find('div',id='feature-bullets')
# spans = product_desc.find_all('span',class_="a-list-item")
# desc = []
# for i in spans:
#     desc.append(i.text)











































# desk = soup.find('div',class_='s-result-list')
# products = desk.find_all('div',class_='s-overflow-hidden')

# boxes = soup.find_all('div',class_='sg-col-20-of-24')
# print(len(boxes))

# for box in boxes:
#     try:
#         links = box.find('h2',class_='a-size-mini')
#         print(links.text,end="\n\n")
#     except:
#         print("not found\n\n")


# product_links = []
# for link in soup.find_all("a", class_="a-link-normal"):
#     href = link.get("href")
#     if "/dp/" in href:  # Checking if the link contains "/dp/" to identify product URLs
#         product_links.append("https://www.amazon.in" + href)

# # Print the extracted product links
# for link in product_links:
#     print(link)


