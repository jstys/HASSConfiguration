import http.client
import json

from actions.push_notify_action import PushNotifyAction

INTERVAL = 90
ENABLED = False
DATE = '1/23/2021'

def callback():
    conn = http.client.HTTPSConnection("www.shopskibluemt.com")
    payload = 'productId=582&productForm=product_attribute_3618%3D%26product_attribute_3617%3D6127431%26product_attribute_3630-startdate%3D%26product_attribute_3630-price%3D0%26product_attribute_3630%3D%26addtocart_582.EnteredQuantity%3D1&start=2021-01-23T00%3A00%3A00&end=2021-01-24T00%3A00%3A00'
    headers = { 'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'Nop.customer=80fce464-b4da-4cbc-b56a-d528f48eaf3f; TS01426631=01c017140d08eade67514b4ccac7aa8ab661b2510d094c3d38791250d06e6b2f37b5939bf01a684f0f0f4f9d5ec17f61092caac88e'}
    conn.request("POST", "/intouchPrices/list", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads((data.decode("utf-8")))
    for day in data:
        if DATE in day['optionDisplay']:
            PushNotifyAction().add_target("jim_cell").set_message(day['optionDisplay']).notify()
