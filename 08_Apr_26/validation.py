import json
from pydantic import BaseModel
from typing import List,Optional,Dict

class addressInfo(BaseModel):
    full_address :str
    region :str
    city :str
    pincode :int
    state :str

class cuisines(BaseModel):
    name: str
    url: str

class timings(BaseModel):
    open:str
    close:str

class days(BaseModel):
    monday: timings
    tuesday: timings
    wednesday: timings
    thursday: timings
    friday: timings
    saturday: timings
    sunday: timings

class items(BaseModel):
    item_id:str
    item_name:str
    item_slugs:List['str']
    item_url:str
    item_description: Optional['str']
    item_price: Optional[float]
    is_veg: bool

class menu_categories(BaseModel):
    category_name:str
    items:List[items]

class ZomatoData(BaseModel):
    restaurant_id:int
    restaurant_name:str
    restaurant_url:str
    restaurant_contact:str
    fssai_licence_number:str
    address_info:addressInfo
    cuisines:List[cuisines]
    timings: Dict[str, timings]
    menu_categories:List[menu_categories]

