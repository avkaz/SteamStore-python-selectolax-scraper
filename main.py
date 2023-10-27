from selectolax.parser import HTMLParser
from utils.extract import extract_full_body_html
from utils.parse import parse_raw_attributes
from utils.process import format_and_transform, save_to_file
from config.tools import get_config
import pandas as pd

if __name__ == '__main__':
    config = get_config()
    html = extract_full_body_html(
        from_url = config.get('url'), 
        wait_for = config.get('container').get('selector')
        )
    
    nodes = parse_raw_attributes(html, [config.get('container')])


    game_data = []
    for node in nodes.get('store_sale_divs'):
        attrs = parse_raw_attributes(node, config.get('item'))
        attrs = format_and_transform(attrs)
        game_data.append(attrs)

        save_to_file('extract', game_data)




