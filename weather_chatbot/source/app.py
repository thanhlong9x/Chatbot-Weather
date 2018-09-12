from flask import Flask, request
import info
import requests

app = Flask(__name__)

thoitiet = {"0": " bão ", "1": " bão nhiệt đới ", "2": " lốc xoáy ", "3": " giông bão nghiêm trọng ",
            "4": " giông bão ", "5": " mưa tuyết ", "6": " mưa đá ", "7": " mưa đá và tuyết ",
            "8": " mưa phùn lạnh giá ", "9": " mưa phùn ", "10": " mưa lạnh ", "11": " mưa rào ", "12": " mưa rào ",
            "13": " tuyết ", "14": " tuyết rơi nhẹ ", "15": " gió tuyết ", "16": " tuyết rơi ", "17": " mưa đá ",
            "18": " mưa đá ", "19": " bụi ", "20": " sương mù ", "21": " sương mù ", "22": " khói ", "23": " blustery ",
            "24": " gió ", "25": " lạnh ", "26": " mây ", "27": " nhiều mây về đêm ", "28": " nhiều mây ban ngày ",
            "29": " mây thưa về đêm ", "30": " thưa mây ban ngày ", "31": " trời quang về đêm ", "32": " nắng ",
            "33": " quang về đêm ", "34": " quang về ngày", "35": " mưa đá nặng", "36": " nóng ", "37": " mưa giông ",
            "38": " mưa giồng rải rác ", "39": " mưa giồng rải rác ", "40": " mưa rải rác ", "41": " tuyết rơi dày ",
            "42": " tuyết rơi rải rác ", "43": " tuyết rơi nặng ", "44": " thưa mây ", "45": " mưa giông ",
            "46": " mưa tuyết ", "47": " mưa giông ", "3200": " not available "}


def lay_thong_tin_thoi_tiet(req, place, time):
    day = info.info_weather(place, time)
    high = float(day['high'])
    low = float(day['low'])
    cel_hi = float("{0:.2f}".format((high - 32) * 5 / 9))
    cel_lo = float("{0:.2f}".format((low - 32) * 5 / 9))

    to = " , dự báo " + thoitiet[day['code']]
    t1 = " nhiệt độ thấp nhất " + str(cel_lo).format() + " °C, nhiệt độ cao nhất " + str(cel_hi) + " °C"

    if cel_hi >= 35:
        t = "trời nóng," + t1 + to
    elif cel_hi <= 10:
        t = "trời rét," + t1 + to
    else:
        t = "trời mát," + t1 + to

    return t


@app.route("/chat", methods=['GET', 'POST'])
def query():
    message = request.args.get('message')
    print(message)

    url = "https://api.dialogflow.com/v1/query"
    querystring = {"query": message, "sessionId": "4dd82fa8-8500-bda2-9186-2d12a26e7fb9", "timezone": "Asia/Saigon",
                   "lang": "en", "v": "20170712"}
    payload = ""
    headers = {'authorization': 'Bearer 9d0171aec019413ea138a5ac82b8ffdd'}
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    print(response)
    obj = response.json()
    text = obj['result']['fulfillment']['messages'][0]['speech']

    if obj['result']['action'] == 'hoi':
        time = obj['result']['parameters']['Time']
        place = obj['result']['parameters']['Location']
        if time == '' or place == '':
            place = "hà nội"
            time = 'hôm nay'
        text = text.replace('<place>', place)
        text = text.replace('<time>', time)

        if time == '':
            text = ' Thời điểm chưa được dự đoán hoặc chưa có thời điểm cụ thể để dự đoán  '
        elif place == '':
            text = 'Địa điểm chưa được cập nhật, vui lòng thử lại sau'
        else:
            text = text.replace('<thong_tin_thoi_tiet>', lay_thong_tin_thoi_tiet(obj, place, time))

    return text


if __name__ == '__main__':
    app.run()
