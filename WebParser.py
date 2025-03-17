from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json

class WebScraper:
    def __init__(self):
        self.website = requests.get("https://www.prospektmaschine.de/hypermarkte/")
        self.soup = BeautifulSoup(self.website.text, "html.parser")

    def parse_thumbnail(self, img_tag):
        if img_tag:
            if img_tag.get("src"):
                return img_tag["src"]
            elif img_tag.get("data-src"):
                return img_tag["data-src"]
            else:
               return "N/A"
        else:
            return "N/A"


    def parse_date(self, date_text):
        date_text = date_text.split(" ")[-1]
        try:
            return datetime.strptime(date_text, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError:
            return "Invalid Date"

    def parse(self):
        brochures = self.soup.find_all("div", {"class": "brochure-thumb col-xs-6 col-sm-3"})
        data = []

        for brochure in brochures:
            title_tag = brochure.find("p", {"class": "grid-item-content"}).find("strong")
            if title_tag:
                title = title_tag.text.strip()
            else:
                title = "N/A"

            shop_name_tag = brochure.find("a", {"title": True})
            # nenasiel som lepsi sposob ako dostat meno obchodu ako prve slovo po des Geschäftes
            if shop_name_tag:
                shop_name = shop_name_tag["title"].split("des Geschäftes")[1].split(",")[0].strip()
            else:
                shop_name = "N/A"

            thumbnail = self.parse_thumbnail(brochure.find("img"))

            date_tag = brochure.find("small")
            valid_from = "N/A"
            valid_to = "N/A"

            if date_tag:
                date_text = date_tag.text.strip()
                if " - " in date_text:
                    dates = date_text.split(" - ")
                    if len(dates) == 2:
                        valid_from = self.parse_date(dates[0])
                        valid_to = self.parse_date(dates[1])
                else:
                    valid_from = self.parse_date(date_text)


            parsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            data.append({
                "title": title,
                "thumbnail": thumbnail,
                "shop_name": shop_name,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "parsed_time": parsed_time
            })

        with open("brochures.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    scraper = WebScraper()
    scraper.parse()
