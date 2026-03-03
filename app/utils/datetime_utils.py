from datetime import datetime

def get_weekday_start_now():
    today_weekday = datetime.now().weekday()+1

    num_to_weekday = {
        "0": "Mon",
        "1": "Tue",
        "2": "Web",
        "3": "The",
        "4": "Fri",
        "5": "Sat",
        "6": "Sun"
    }

    data = [str((i % 7)) for i in range(today_weekday, today_weekday + 7)]
    name_week_day = "Mon Tue Web The Fri Sat Sun".split()
    weekday = []
    for i in data:
        weekday.append(num_to_weekday[str(i)])

    return weekday