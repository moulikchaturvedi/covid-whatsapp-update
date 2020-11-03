# COVID WhatsApp Updater
This is a Python script which uses Twilio and the COVID API to send regular updates of COVID cases in the country through WhatsApp.

## Connect with me at
1. [LinkedIn](https://www.linkedin.com/in/moulik-chaturvedi-7b7aab157/)
2. [GitHub](https://github.com/moulikchaturvedi)
3. [Instagram](https://www.instagram.com/multidimensionalspacesnake/)

## The Following is the Explanation of the Code
Importing the Packages.
```python
from datetime import datetime, timedelta

import requests

from twilio.rest import Client
from dateutil.parser import parse
```

Using the COVID API to fetch the number of cases. The function parameters take in the country and the dates for which the case updates have to be returned.
```python
def get_country_confirmed_infected(country, start_date, end_date):
    resp = requests.get(f"https://api.covid19api.com/country/{country}/status/confirmed", params={"from": start_date, "to": end_date})
    return resp.json()
```

Using Twilio to send the updates to the respective numbers. Twilio doesn't have any direct method to send WhatsApp messages to multiple numbers. Hence, I created an array to store all the numbers and also a for loop to iterate through all the numbers in the array and send the messages one by one.
```python
#Array to store all the numbers to which update would be sent
numbers_to_message=['whatsapp:<insert_number_with_country_code','whatsapp:<insert_number_with_country_code>']

#Sending Whatsapp messages using Twilio
def send_whatsapp_message(msg):
    account_sid = '<twilio_account_SID>'
    auth_token = '<twilio_account_auth_token>'
    
    #For loop to iterate through all numbers
    for number in numbers_to_message:
    	Client(account_sid, auth_token).messages.create(
        from_='whatsapp:<twilio_whatsappnumber_with_country_code>',
        to= number,
        body=msg
    )
```

The main() function stores the name of the country and the dates, then calls the COVID and Twilio functions. The if-else statement check if the rate of cases is increasing or decreasing and suggests whether it is recommended to travel or not.
```python
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
```
