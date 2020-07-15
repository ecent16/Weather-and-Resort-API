# Weather Tracker and Resort Finder
# Ervin Centeno
# December 3, 2018

import csv
import requests

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

totalAccu = 0
snowFall = []


while True:
    try:
        resortFile = input('Please type in the csv file that contains the ski resort names: ')

        csvResort = open(resortFile)
        fileReader = csv.reader(csvResort)
        ResortData = list(fileReader)
        break

    except FileNotFoundError:
        print('Try again')
        continue

phoneNum = input('Enter a phone number: ')

for i in range(len(ResortData)):
    resortName = ResortData[i][0]
    city = ResortData[i][1]
    state = ResortData[i][2]
    while True:
        try:
            r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + city + ',' +
                             state + '&key=AIzaSyCYIen_c3ag0CZix5eFcaiGNnm1gNspj7w')
            data = r.json()
            longitude = data['results'][0]['geometry']['location']['lng']
            latitude = data['results'][0]['geometry']['location']['lat']

            break
        except IndexError:
            print('Try again')
            continue

    fr = requests.get('https://api.darksky.net/forecast/66b058fe292988f7486dcbb4b45da132/' +
                      str(latitude) + ',' + str(longitude))
    fdata = fr.json()

    print('Fetching data for ' + resortName + '...')

    snow = []
    for i in range(8):
        precip = fdata['daily']['data'][i]
        precipAccu = str(precip.get('precipAccumulation', 0))   # Only works as on str data type values.

        snow.append(float(precipAccu))  # Converts precipAccu into a float data type.

    totalAccu = sum(snow)
    snowFall.append(totalAccu)
    print('%.3f' % totalAccu + ' inches')  # Prints only 3 decimal places out.

# Creates a new file with appended with snowFall.
with open('ResortSnow.csv', 'w', newline='') as outFile:
    outWrite = csv.writer(outFile)
    for i in range(len(ResortData)):

        snow = [ResortData[i][0], ResortData[i][1], ResortData[i][2], str(snowFall[i])]

        outWrite.writerow(snow)
outFile.close()

maxSnow = max(snowFall)
# Opens the new CSV file to get the max snowfall and resort name.
TopResort = ''
ResortSnow = open('ResortSnow.csv')
fileReader = csv.reader(ResortSnow)
NewResortData = list(fileReader)

for i in range(len(NewResortData)):
    if float(NewResortData[i][3]) == maxSnow:
        print(NewResortData[i][0], 'has the most snow of', '%.3f' % maxSnow, 'inches.')
        TopResort = str(NewResortData[i][0])

body = (TopResort + ' has the most snow of ' + '%.3f' % maxSnow + ' inches.')

acc_sid = 'ACb278c9c8eb247cb3ae66018f162207ba'
auth_token = 'd6f542d504f6c6fe7429b4966ac76aa0'
client = Client(acc_sid, auth_token)
while True:
    try:
        message = client.messages \
            .create(from_='+13472897803',
                body= body,
                to='+1' + phoneNum)
        break
    except TwilioRestException as e:
        if e.code == 20404:
            break


















