from selectolax.parser import HTMLParser
from utils.extract import extract_full_body_html
from utils.parse import parse_raw_attributes
from config.tools import get_config
import pandas as pd

if __name__ == '__main__':
    config = get_config()
    html = extract_full_body_html(
        from_url = config.get('url'), 
        wait_for = config.get('container').get('selector')
        )
    

    tree = HTMLParser(html)
    divs = tree.css('div[class*="salepreviewwidgets_StoreSaleWidgetContainer"]') # *= is should contain

    for d in divs:
        attrs = parse_raw_attributes(d, config.get('item'))
        # title = d.css_first('div[class*="StoreSaleWidgetTitle"]').text()
        # thumbnail = d.css_first('img[class*="CapsuleImage"]').attributes.get('src')
        # tags = [a.text() for a in d.css('div[class*="StoreSaleWidgetTags"] > a')[:5]]
        # release_date = d.css_first('div[class*="WidgetReleaseDateAndPlatformCtn"] > div[class*= "StoreSaleWidgetRelease"]').text()
        # review_score = d.css_first('div[class*="ReviewScoreValue"] div').text()
        # reviewed_by = d.css_first('div[class*="ReviewScoreCount"]').text()
        # original_price_element = d.css_first('div[class*="StoreOriginalPrice"]')
        # original_price = original_price_element.text() if original_price_element else ""
        # # original_price = d.css_first('div[class*="StoreOriginalPrice"]').text()            
        # sale_price = d.css_first('div[class*="StoreSalePriceBox"]').text()
        # attrs = {'title': title,
        #             'release_date': release_date,
        #             'review_score': review_score,
        #             'reviewed_by': reviewed_by,
        #             'original_price': original_price,
        #             'sale_price': sale_price,
        #             'tags': tags,
        #             'thumbnail' : thumbnail,
        #             }
        print(attrs)

    df = pd.DataFrame(attrs, columns=["title", "thumbnail", "release_date", "review_score", "reviewed_by", "price_currency", "sale_price", "original_price"])
    df.set_index("title", inplace=True)

    print(df)