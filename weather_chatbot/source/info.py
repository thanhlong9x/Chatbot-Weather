import urllib
import requests

weakdays = {"thứ 2": "Mon", "thứ 3": "Tue", "thứ 4": "Wed", "thứ 5": "Thu", "thứ 6": "Fri", "thứ 7": "Sat", "chủ nhật": "Sun",
            "thứ hai": "Mon", "thứ ba": "Tue", "thứ tư": "Wed", "thứ năm": "Thu", "thứ sáu": "Fri", "thứ bảy": "Sat"}


def info_weather(place,time):

    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"" + str(place) + "\")"
    yql_url = baseurl + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
    # result = urllib.request.urlopen(yql_url).read()
    response = requests.get(yql_url).json()
    # print(response)
    forecast_data = response['query']['results']['channel']['item']['forecast']
    #print(forecast_data)

    order_day = []

    for i in range(0, 8):
        order_day.append(forecast_data[i]["day"])

    if time in weakdays:
        for i in range(0, 8):
            if weakdays[time] == order_day[i]:
                index = i
                break
    else:
        if time == 'hôm nay':
            index = 0
        elif time == 'ngày mai':
            index = 1
        elif time == 'ngày kia':
            index = 2
    # print(response)

    return forecast_data[index]




