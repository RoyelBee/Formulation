import sql_queries as s
import random
import string
import json


def generate_random(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def money_converter(taka):
    if len(str(taka)) >= 8:
        val = str(round(taka / 10000000, 2)) + ' Cr'

    elif len(str(taka)) >= 6:
        val = str(round(taka / 100000, 2)) + ' Lac'

    elif len(str(taka)) >= 4:
        val = str(round(taka / 1000, 2)) + ' Th'

    else:
        val = taka
    return val

data = {}

data['LiveSales'] = {
    "uid": generate_random(8, "1234ABCD"),
    "updateDate": str(s.now),
    "titleText": "Todays Live Sales",
    "mainText": "Todays target is " + str(s.todays_target) + " where we only made sales of " + str(
        s.todays_sales) + " Which indicates  " +
                str(s.todays_achv) + " achievements",
    "redirectionUrl": ""
}

with open("data.json", "w") as f:
    json.dump(list(data.values()), f)
    print('JSON Data created.')
