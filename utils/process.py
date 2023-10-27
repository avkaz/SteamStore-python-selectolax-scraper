import re
from datetime import datetime
from selectolax.parser import Node
import pandas as pd


def get_attrs_from_node(node: Node, attr: str):
    if node is None or not issubclass(Node, type(node)):
        raise ValueError("The function expects a selecolax node to be provided")

    return node.attributes.get(attr)


def get_first_n(input_list: list, n: int = 5):
    return input_list[:n]


def reformat_date(date_raw: str, input_format: str = '%b %d, %Y', output_format: str = '%Y-%m-%d'):
    dt_obj = datetime.strptime(date_raw, input_format)
    return datetime.strftime(dt_obj, output_format)


def regex(input_str: str, pattern: str, do_what: str = "findall"):
        if do_what == "findall":
            return re.findall(pattern, input_str)
        elif do_what == "split":
            return re.split(pattern, input_str)
        else:
            raise ValueError("The function expects 'findall' or 'split' to be provided")


{'title': 'ARK: Survival Ascended', 'thumbnail': 'https://cdn.akamai.steamstatic.com/steam/apps/2399830/header.jpg?t=1698342194', 'tags': ['Survival', 'Dinosaurs', 'Open World', 'Adventure', 'Action'], 'release_date': '2023-10-26', 'review_score': 'Mixed', 'reviewed_by': 7199, 'price_currency': '40,49€', 'sale_price': '40,49€', 'original_price': ' '}
{'title': 'Euro Truck Simulator 2', 'thumbnail': 'https://cdn.akamai.steamstatic.com/steam/apps/227300/header.jpg?t=1697795373', 'tags': ['Driving', 'Transportation', 'Simulation', 'Open World', 'Automobile Sim'], 'release_date': '2012-10-12', 'review_score': 'Overwhelmingly Positive', 'reviewed_by': 505740, 'price_currency': '4,99€', 'sale_price': '4,99€', 'original_price': '19,99€'}


def split_price(input, position):
    try:
        splited_val = input[position]
    except IndexError:
        splited_val = "0,00"
    return splited_val

def to_float(value_str):
    value_float = None  # Initialize with a default value
    value_str = value_str.replace(',', '.')
    try:
        value_float = float(value_str)
    except ValueError:
        pass
    return value_float

def format_and_transform(attrs: dict):
    transforms = {
        "thumbnail": lambda n: get_attrs_from_node(n, "src"),
        "tags": lambda input_list: get_first_n(input_list, 5),
        "release_date": lambda date: reformat_date(date, '%b %d, %Y', '%Y-%m-%d'),
        "reviewed_by": lambda raw: int(''.join(regex(raw, r'\d+', "findall"))),
        "price_currency": lambda raw: regex(raw, r"(\d+,\d+)([€$¥£₹₽₩₨₴₣₿₦฿₺₸₼₻₵₡₢₫₣₤₥₦₧₱₰₳₲₥₸₹₺₦₲₥₷₻₽₦])", "split")[2],
        "sale_price": lambda raw: to_float(split_price(regex(raw, r"(\d+,\d+)([€$¥£₹₽₩₨₴₣₿₦฿₺₸₼₻₵₡₢₫₣₤₥₦₧₱₰₳₲₥₸₹₺₦₲₥₷₻₽₦])", "split"),1)),
        "original_price": lambda raw: to_float(split_price(regex(raw, r"(\d+,\d+)([€$¥£₹₽₩₨₴₣₿₦฿₺₸₼₻₵₡₢₫₣₤₥₦₧₱₰₳₲₥₸₹₺₦₲₥₷₻₽₦])", "split"),1))
    }

    for k, v in transforms.items():
        if k in attrs:
            attrs[k] = v(attrs[k])
 
    if attrs.get("original_price") != 0 and attrs.get("sale_price") != 0:
        attrs["discount_pct"] = round((attrs["original_price"] - attrs["sale_price"]) / attrs["original_price"] * 100, 2)
    else:
        attrs["discount_pct"] = 0.00
    
    return attrs


def save_to_file(filename="extract", data: list[dict] = None):
    if data is None:
        raise ValueError("The function expects data to be provided as a list of dictionaries")

    df = pd.DataFrame(data)
    filename = f"{datetime.now().strftime('%Y_%m_%d')}_{filename}.csv"
    df.to_csv(filename, index=False)
