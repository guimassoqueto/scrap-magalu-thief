from pydantic import BaseModel


class Item(BaseModel):
  id: str
  title: str
  category: str
  reviews: int
  image_url: str
  price: float
  free_shipping: bool
  previous_price: float
  discount: int