import MarketData
import json
import schedule
import time
import requests

API_ID = 24154420
API_HASH = "661a3019c7ae36a7422f0aa87b7d6b80"
CHAT_ID = 2064935123

#client = TelegramClient("correlation", API_ID, API_HASH)


def send_telegram_message(message):
    TOKEN = "6927010137:AAFOw_Z3WYTzcf_kumFD4a4f8f0mSwIj3lo"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={-1001998826152}&text={message}"
    print(requests.get(url).json())


def get_coinlist():
    f = open('data.json')

    coin_list = []
    file1 = open('coinlist.txt', 'r')
    Lines = file1.readlines()

    for line in Lines:
        coin_list.append(line.strip())

    f.close()
    return coin_list


def get_correlations_dictionary():
    f = open("daily_corr.json", "r")

    data = json.load(f)
    f.close()

    return data


def get_correlated_pairs(coin):
    returnDictionary = {}
    data = get_correlations_dictionary()
    for i in data:
        if i == coin:
            returnDictionary = data[i].copy()
            returnDictionary = dict(sorted(returnDictionary.items(), key=lambda item: item[1], reverse=True))

    return returnDictionary


def get_hour_data(coin):
    candle_info = MarketData.get_data(coin, "1h", 2)

    lastHourOpening = float(candle_info[0][1])
    currentPrice = float(candle_info[1][4])

    change = (currentPrice / lastHourOpening - 1) * 100

    return round(change, 2), currentPrice


def get_day_data(coin):
    candle_info = MarketData.get_data(coin, "1d", 1)

    lastHourOpening = float(candle_info[0][1])
    currentPrice = float(candle_info[0][4])

    change = (currentPrice / lastHourOpening - 1) * 100

    return round(change, 2)


def get_emoji(value):
    if value > 0:
        return "\U0001F7E2"
    else:
        return "\U0001F534"


def append_output(output, coin, correlation, hourly, daily, current_price):
    returnStr = output

    returnStr += \
        f"""
        {coin}: {current_price}
        1 Saat: {get_emoji(hourly)}\t\t%{hourly}
        Günlük: %{get_emoji(daily)}\t\t%{daily}
        Korelasyon:\t\t{round(float(correlation), 3)}
    
        """
    return returnStr


def handle_signal(coin):
    correlations = get_correlated_pairs(coin)

    if len(correlations) == 0:
        return

    coin_hour_data = get_hour_data(coin)
    coin_daily_data = get_day_data(coin)

    output = \
        f"""
{coin}
1 Saat: {get_emoji(coin_hour_data[0])}\t%{coin_hour_data[0]}
Günlük: %{get_emoji(coin_daily_data)}\t%{coin_daily_data}
    """

    for i in correlations:
        corr_hour_data = get_hour_data(i)
        corr_daily_data = get_day_data(i)
        output = append_output(output, i, correlations[i], corr_hour_data[0], corr_daily_data, corr_hour_data[1])

    send_telegram_message(output)


def search_for_signal():
    send_telegram_message("\U000023F0 \U000023F0 \U000023F0 \U000023F0")
    coinlist = get_coinlist()

    for coin in coinlist:
        hourly_change = get_hour_data(coin)[0]
        daily_change = get_day_data(coin)

        if hourly_change > 5 or daily_change > 10:
            handle_signal(coin)


# @client.on(events.NewMessage(outgoing=True, incoming=True, pattern="/Signal"))
# async def get_ticker(event):
#    chat = await event.get_chat()
#    print(chat)
#    msg = event.message.message
#    message_split = msg.split(" ")
#
#    coin = message_split[1]
#    if coin not in get_correlations_dictionary():
#        await client.send_message(CHAT_ID, "Korelasyon bulunamadı.")
#    else:
#        await client.send_message(CHAT_ID, handle_signal(message_split[1]))


def main():
    schedule.every().hour.at(":10").do(search_for_signal)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
