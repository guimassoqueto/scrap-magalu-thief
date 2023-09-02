from app.selectolax.magalu_item import Item
from selectolax.parser import HTMLParser
from urllib.parse import urljoin
import re

class MagaluItemParser:
  def __init__(self, url: str, html_content: str) -> None:
    self.html = HTMLParser(html_content)
    self.url = url
  
  def get_item(self) -> dict:
    try:
      id = self.__get_id()
      category = self.__get_category()
      title = self.__get_title()
      reviews = self.__get_reviews()
      image_url = self.__get_image_url()
      free_shipping = False
      price = self.__get_price()
      previous_price = self.__get_previous_price()
      discount = self.__get_discount(price, previous_price)
      item = Item(
        id=id,
        title=title,
        category=category,
        reviews=reviews,
        free_shipping=free_shipping,
        image_url=image_url,
        price=price,
        previous_price=previous_price,
        discount=discount
      )
      return item.model_dump()
    except Exception as e:
      print(e)

  def __get_id(self) -> str:
    if 'magazineluiza.com.br' in self.url: return self.url
    match = re.search(".com.br/[a-zAZ0-9-]+/(.+)", self.url)
    return urljoin("https://magazineluiza.com.br/", match.group(1))

  def __get_category(self) -> str:
    categories = self.html.css('[data-testid="breadcrumb-item"]')
    category = " ".join([category.text() for category in categories if category.text()])
    return category

  def __get_title(self) -> str:
    return self.html.css_first('[data-testid="heading-product-title"]').text()

  def __get_reviews(self) -> int:
    inner_text = self.html.css_first('[format="score-count"]').text()
    if inner_text:
      match = re.search(r"\((\d+)\)", inner_text)
      return int(match.group(1))
    return 0

  def __get_image_url(self) -> str:
    image_url = self.html.css_first('[data-testid="image-selected-thumbnail"]').attributes["src"]
    if image_url:
        return image_url
    return "https://raw.githubusercontent.com/guimassoqueto/mocks/main/images/404.webp"

  def __get_price(self) -> float:
    price_raw = self.html.css_first('[data-testid="price-value"]').text()
    price_value = re.search(r"[\d\.]+\,\d{2}$", price_raw).group()
    return float(price_value.replace(".", "").replace(",", "."))

  def __get_previous_price(self) -> float | None:
    price_raw = self.html.css_first('[data-testid="price-original"]').text()
    if price_raw:
      price_value = re.search(r"[\d\.]+\,\d{2}$", price_raw).group()
      return float(price_value.replace(".", "").replace(",", "."))
    return None

  def __get_discount(self, price: float, previous_price: float) -> int:
    return round((1 - (price / previous_price)) * 100)