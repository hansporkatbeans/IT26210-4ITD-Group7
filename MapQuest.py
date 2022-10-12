from audioop import add
import urllib.parse
import requests
import calendar
from datetime import date, datetime, time, timedelta

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "mvxR2JK4nufhenP6Yc3xjKeBBhFzqGBc" #Replace with your MapQuest key

def realEta(time):
    sec = float(time)
    sec_value = sec % (24 * 3600)
    hour_value = sec_value // 3600
    sec_value %= 3600
    min = sec_value // 60
    sec_value %= 60
    travelTime = (datetime.now().strftime("%H:%M:%S %p"))
    arrivalTime = str(((datetime.now() + timedelta(hours=hour_value, minutes=min, seconds=sec_value)).strftime("%H:%M:%S %p")))
    print("Realtime Trip Duration: " + str("{:g}".format(hour_value)) + " Hours, " + str("{:g}".format(min)) + " Minutes, and " + str("{:g}".format(sec_value)) + " Seconds.")
    print("Time of Travel: " + travelTime)
    print("Time of Arrival: " + arrivalTime)

def estEta(time):
    time = (json_data["route"]["formattedTime"])
    date_time = datetime.strptime(time, "%H:%M:%S")
    a_timedelta = date_time - datetime(1900, 1, 1)
    sec = a_timedelta.total_seconds()
    #sec = int(time%(24*3600))
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    print("Estimated Trip Duration: " + str("{:g}".format(hour)) + " Hours, " + str("{:g}".format(min)) + " Minutes, and " + str("{:g}".format(sec)) + " Seconds.")


while True:
    print("\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = \n")
    print("\tWelcome User! To generate trip details and directions, kindly fill out the needed information below.\n \t\t\t\tOnce done, you may enter \"q\" or \"quit\". Thank you! \n")
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = \n")
    orig = input("Specify Starting Point: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Specify Target Destination: ")
    if dest == "quit" or dest == "q":
        break
    while True:
        met = input("Metric(miles/km): ")
        met = met.lower()
        if met == "miles" or met == "mile" or met == "km" or met == "kilometers" or met == "kilometer":
            break
        else :
            print("Sorry, it seems that the data you have entered is invalid. Please enter either miles, km, or kilometers.")
    if met == "quit" or met == "q":
        break
    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ")
        print()
        print("TRIP DETAILS\n")
        print("Directions from " + (orig) + " to " + (dest))
        estEta(json_data["route"]["formattedTime"])
        realEta(json_data["route"]["realTime"])
        if met == "km" or met == "kilometers" or met == "kilometer" :
            print("Kilometers:      " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
        elif met == "miles" or met == "mile" :
            print("Miles:           " + str("{:.2f}".format((json_data["route"]["distance"]))))
        print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
        print()
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        x=0
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            x+=1
            print()
            if met == "km" or met == "kilometers" or met == "kilometer" :
                print(str(x) + ". " + (each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
            elif met == "miles" or met == "mile" :
                print(str(x) + ". " + (each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])) + " miles)"))
    elif json_status == 402:
        print("******************************************")
        print("Status Code: " + str(json_status) + "; You have entered an invalid data, please try again.")
        print("**********************************************\n")
    elif json_status == 611:
        print("******************************************")
        print("Status Code: " + str(json_status) + "; Incomplete fields, please ensure that all fields are filled.")
        print("**********************************************\n") 
    else:
        print("********************************************************************")
        print("For Staus Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")