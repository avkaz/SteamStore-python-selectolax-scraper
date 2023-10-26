from selectolax.parser import HTMLParser
from utils.extract import extract_full_body_html

url = 'https://store.steampowered.com/specials'
wait_for_tag = 'div[class*="salepreviewwidgets_StoreSaleWidgetContainer"]'

if __name__ == '__main__':

    html = extract_full_body_html(from_url = url, wait_for = wait_for_tag)
    tree = HTMLParser(html)
    divs = tree.css('div[class*="salepreviewwidgets_StoreSaleWidgetContainer"]') # *= is should contain

    print(len(divs))

    for d in divs:
        title = d.css_first('div[class*="salepreviewwidgets_StoreSaleWidgetTitle"]').text()
        thumbnail = d.css_first('img[class*="salepreviewwidgets_CapsuleImage"]').attributes.get('src')
        tags = [a.text() for a in d.css('div[class*="salepreviewwidgets_StoreSaleWidgetTags"] > a')[:5]]
        release_date = d.css_first('div[class*="salepreviewwidgets_WidgetReleaseDateAndPlatformCtn"] > div[class*= "salepreviewwidgets_StoreSaleWidgetRelease"]').text()
        rate = d.css_first('div[class*="ReviewScoreValue"] div').text()
        reviewed_by = d.css_first('div[class*="ReviewScoreCount"]').text()
        original_price = d.css_first('div[class*="StoreOriginalPrice"]').text()
        sale_price = d.css_first('div[class*="StoreSalePriceBox"]').text()
        attrs = {'title': title,
                    'release_date': release_date,
                    'rate': rate,
                    'reviewed_by': reviewed_by,
                    'original_price': original_price,
                    'sale_price': sale_price,
                    'tags': tags,
                    'thumbnail' : thumbnail,
                    }
        print(attrs)