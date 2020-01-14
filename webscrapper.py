import requests
import pandas
from bs4 import BeautifulSoup

base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
c = r.content
soup = BeautifulSoup(c, "html.parser")
page_nr = soup.find_all("a", {"class", "Page"})[-1].text

l = []
for page in range(0, int(page_nr)*10, 10):
    r = requests.get(base_url + str(page) + '.html', headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    
    all_div = soup.find_all("div", {"class": "propertyRow"})
    
    for item in all_div:
        d = {}
        try:
            d["Price"] = item.find_all("h4", {"class": "propPrice"})[0].text.replace("\n","").replace(" ", "")
        except:
            d["Price"] = None

        try:
            d["Address"] = item.find_all("span", {"class", "propAddressCollapse"})[0].text
        except:
            d["Address"] = None

        try:
            d["Locality"] = item.find_all("span", {"class", "propAddressCollapse"})[1].text
        except:
            d["Locality"] = None
        
        try:
            d["Beds"] = item.find("span", {"class", "infoBed"}).find("b").text
        except:
            d["Beds"] = None
        
        try:
            d["Area"] = item.find("span", {"class", "infoSqFt"}).find("b").text
        except:
            d["Area"] = None

        try:
            d["Full Baths"] = item.find("span", {"class", "infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"] = None

        try:
            d["Half Baths"] = item.find("span", {"class", "infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"] = None

        for column_group in item.find_all("div", {"class", "columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class", "featureGroup"}), column_group.find_all("span", {"class", "featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text
        l.append(d)
df = pandas.DataFrame(l)

df.to_csv("Output.csv")