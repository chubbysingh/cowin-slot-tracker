#!/usr/bin/env python3
import datetime
import time

import json
import requests
from twilio.rest import Client


def get_date(n):
    """
    Function to get the current date

    Returns
    -------
    date : String
        Current date in DD-MM-YYYY format

    """
    current_time = datetime.datetime.now() + datetime.timedelta(days=7 * n)
    day = current_time.day
    month = current_time.month
    year = current_time.year
    date = "{dd}-{mm}-{yyyy}".format(dd=day, mm=month, yyyy=year)
    return date


def ping_cowin(date, district_id):
    """
    Function to ping the COWIN API to get the latest district wise details

    Parameters
    ----------
    date : String
    district_id : String
    
    Returns
    -------
    json

    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}".format(
        district_id=district_id, date=date)

    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def check_availability(payload, age):
    """
    Function to check availability in the hospitals from the json response from the public API

    Parameters
    ----------
    payload : JSON

    Returns
    -------
    available_centers_str : String
        Available hospitals
    unavailable_centers_str : String
        Unavailable hospitals
        :param payload:
        :param age:

    """
    available_centers = set()
    available_centers_str = False

    if 'centers' in payload.keys():
        length = len(payload['centers'])
        if length > 1:
            for i in range(0, length):
                sessions_len = len(payload['centers'][i]['sessions'])
                for j in range(0, sessions_len):
                    center_metadata = payload['centers'][i]['sessions'][j]
                    if center_metadata['available_capacity'] > 5 and center_metadata['min_age_limit'] is age:
                        available_centers.add(
                            '\n' + str(center_metadata['available_capacity']) + " slots available at " +
                            payload['centers'][i]['name'] + " for " + str(center_metadata['date']))
            available_centers_str = ", ".join(available_centers)

    return available_centers_str


def send_message(message):
    client.messages.create(from_=TWILIO_PHONE_NUMBER,
                           to=CELL_PHONE_NUMBER_1,
                           body=message[0:1000])


if __name__ == "__main__":

    SECRET_TOKEN = "<DUMMY_TWILIO AUTH TOKEN>"  #
    ACCOUNT_SID = "<DUMMY_TWILIO ACCOUNT SID>"  #
    TWILIO_PHONE_NUMBER = "<TWILIO PHONE NUMBER>"  #
    CELL_PHONE_NUMBER_1 = "<DUMMY_YOUR PHONE NUMBER>"  #

    DISTRICT_IDS = input("Enter your DistrictId: ")
    AGE = input("Enter your Age: ")

    client = Client(ACCOUNT_SID, SECRET_TOKEN)

    send_message("Polling for messages. You will receive an alert once a slot opens up.")

    if int(AGE) > 45:
        min_age = 45
    else:
        min_age = 18

    print("Checking for " + str(min_age) + "+ age group")

    while True:
        DISTRICT_ID_ARRAY = list(DISTRICT_IDS.split(" "))
        for dist_id in DISTRICT_ID_ARRAY:
            for week in range(0, 3):
                date = get_date(week)
                print("Polling for week of " + date + " for district_id " + str(dist_id))
                data = ping_cowin(date, dist_id)
                available = check_availability(data, min_age)
                if len(available) > 0:
                    msg_body = available + " for " + str(dist_id)
                    print(msg_body)
                    send_message(msg_body)
                time.sleep(2)
        print("\nSleeping for 60 seconds before trying again")
        time.sleep(60)
