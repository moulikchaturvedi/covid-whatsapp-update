from datetime import datetime, timedelta

import requests

from twilio.rest import Client
from dateutil.parser import parse

def get_country_confirmed_infected(country, start_date, end_date):
    resp = requests.get(f"https://api.covid19api.com/country/{country}/status/confirmed", params={"from": start_date, "to": end_date})
    return resp.json()


numbers_to_message=['whatsapp:+918005060991','whatsapp:+91933588990']


def send_whatsapp_message(msg):
    account_sid = 'AC7cbca01ceddfa8bcdaf1bd8b8d190379'
    auth_token = 'f1cbf86b2a543275ffbeeb87ace6e3bf'
    for number in numbers_to_message:
    	Client(account_sid, auth_token).messages.create(
        from_='whatsapp:+14155238886',
        to='number',
        body=msg
    )

def main():
    country = "India"
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    print("Getting COVID data")
    cases = get_country_confirmed_infected(country, week_ago, today)
    latest_day = cases[-1]
    earliest_day = cases[0]
    percentage_increase = (latest_day['Cases'] - earliest_day['Cases']) / (earliest_day['Cases'] / 100)
    msg = f"There were {latest_day['Cases']} confirmed COVID cases in {country} " \
          f"on {parse(latest_day['Date']).date()}\n"
    if percentage_increase > 0:
        msg += f"This is {round(abs(percentage_increase), 4)}% increase over the last week. " \
               f"Travel is not recommended."
    else:
        msg += f"This is {round(abs(percentage_increase), 4)}% decrease over the last week. " \
               f"Travel may be OK."
    print("Sending Whatsapp message")
    send_whatsapp_message(msg)
    print("Job finished successfully")

if __name__ == '__main__':
    main()