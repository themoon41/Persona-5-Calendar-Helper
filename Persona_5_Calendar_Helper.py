import json

months = []

settingsFiles = ["SeptemberSettings.json", "OctoberSettings.json", "NovemberSettings.json", "DecemberSettings.json"]

for settings in settingsFiles:
    with open(settings, "r") as f:
        data = json.load(f)

    startingDate = data["startingDate"]
    startingOutOfMonth = data["startingOutOfMonth"]
    lastOutOfMonthDate = data["lastOutOfMonthDate"]
    previousMonth = data["previousMonth"]
    previousMonthNum = data["previousMonthNum"]
    currentMonth = data["currentMonth"]
    currentMonthNum = data["currentMonthNum"]
    currentMonthEndDate = data["currentMonthEndDate"]
    nextMonth = data["nextMonth"]
    nextMonthNum = data["nextMonthNum"]
    year = data["year"]

    dayToEvents = data["dayToEvents"]
    dayToWeather = data["dayToWeather"]
    dayToFreeTime = data["dayToFreeTime"]


    dateIndex = startingDate
    beforeMonth = startingOutOfMonth
    afterMonth = False
    weeks = []
    weekDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    while not afterMonth:
        currentWeek = []
        for weekDay in weekDays:
            if beforeMonth:
                currentWeek.append({
                        "WeekDay": weekDay,
                        "Date": dateIndex,
                        "OutOfMonth": previousMonth,
                        "OutOfMonthNum": previousMonthNum
                    })
            elif afterMonth:
                currentWeek.append({
                        "WeekDay": weekDay,
                        "Date": dateIndex,
                        "OutOfMonth": nextMonth,
                        "OutOfMonthNum": nextMonthNum
                    })
            else:
                currentDay = {
                        "WeekDay": weekDay,
                        "Date": dateIndex,
                    }

                events = []
                dateIndexKey = str(dateIndex)

                if dateIndexKey in dayToEvents:
                    for event in dayToEvents[dateIndexKey]:
                        if event["Type"] == "Jazz Club":
                            event["Details"] = f"Taking a party member to the Jazz Club will teach them '{event['Title']}.'"
                        if event["Type"] == "Puzzle":
                            event["Details"] = f"New crossword at Leblanc! The solution is: '{event['Footnote']}.'"
                        events.append(event)

                if dateIndexKey in dayToWeather:
                    currentDay["WeatherDay"] = dayToWeather[dateIndexKey]["WeatherDay"]
                    currentDay["WeatherNight"] = dayToWeather[dateIndexKey]["WeatherNight"]
            
                if dateIndexKey in dayToFreeTime:
                    currentDay["DaySlot"] = dayToFreeTime[dateIndexKey]["DaySlot"]
                    currentDay["NightSlot"] = dayToFreeTime[dateIndexKey]["NightSlot"]
                else:
                    currentDay["DaySlot"] = "Free"
                    currentDay["NightSlot"] = "Free"

                currentDay["Events"] = events
                currentWeek.append(currentDay)
            dateIndex += 1
            if(dateIndex > lastOutOfMonthDate and beforeMonth):
                beforeMonth = False
                dateIndex = 1
            if(dateIndex > currentMonthEndDate and not beforeMonth):
                afterMonth = True
                dateIndex = 1
        weeks.append(currentWeek)

    months.append({
          "Year": year,
          "Month": currentMonth,
          "Number": currentMonthNum,
          "Weeks": weeks
    })

calendarInfo = {
    "Months": months    
}

with open(r"C:\Users\socks_w0giu8c\Documents\GitHub\Persona 5 Calendar\persona5calendar.client\src\Persona5RoyalCalendarInfo.json", "w") as f:
    json.dump(calendarInfo, f)