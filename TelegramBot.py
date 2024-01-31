import os

import telebot
import json
import Correlation
import MarketData
import OutputToJson

SUL_AI_ROBOT_KEY = "6927010137:AAFOw_Z3WYTzcf_kumFD4a4f8f0mSwIj3lo"
PUBLIC_CHANNEL_CHAT_ID = "-1001998826152"

bot = telebot.TeleBot(SUL_AI_ROBOT_KEY)

def save_correlations():
    #MarketData.save_data()

    close_correlation_matrix = Correlation.calculate_correlation('high.xlsx')
    high_correlation_matrix = Correlation.calculate_correlation('high.xlsx')
    low_correlation_matrix = Correlation.calculate_correlation('low.xlsx')

    txtFileName = "daily_corr.txt"
    jsonFileName = "daily_corr.json"
    Correlation.write_correlation(txtFileName, close_correlation_matrix, 0.95)

    OutputToJson.txt_to_json(txtFileName, jsonFileName)


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

    return round(change, 2)


def get_day_data(coin):
    candle_info = MarketData.get_data(coin, "1d", 1)

    lastHourOpening = float(candle_info[0][1])
    currentPrice = float(candle_info[0][4])

    change = (currentPrice / lastHourOpening - 1) * 100

    return round(change, 2)


def append_output(output, coin, correlation, hourly, daily):
    returnStr = output

    returnStr += f"{coin}:\t1H Change: %{hourly}\tDaily Change: %{daily}\tCorrelation: {round(float(correlation), 3)}\n"
    return returnStr


def handle_signal(coin):
    correlations = get_correlated_pairs(coin)

    coin_hour_data = get_hour_data(coin)
    coin_daily_data = get_day_data(coin)

    output = f"""{coin} 1H Change: %{coin_hour_data}\tDaily Change: %{coin_daily_data}\nCorrelated Pairs:\n"""

    for i in correlations:
        corr_hour_data = get_hour_data(i)
        corr_daily_data = get_day_data(i)
        output = append_output(output, i, correlations[i], corr_hour_data, corr_daily_data)

    print(output)
    bot.send_message(PUBLIC_CHANNEL_CHAT_ID, output)
    return output


@bot.channel_post_handler(commands=["Signal"])
def get_signal(message):
    print(message.chat.id)
    message_split = message.text.split(" ")
    if message_split[0] == "/Signal":
        coin = message_split[1]
        if coin not in get_correlations_dictionary():
            bot.send_message(PUBLIC_CHANNEL_CHAT_ID, "Korelasyon bulunamadı.")
        else:
            try:
                handle_signal(message_split[1])
            except Exception:
                print("Exception!")


if __name__ == "__main__":
    #save_correlations()
    bot.polling(non_stop=True, interval=15)
