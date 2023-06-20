from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse

from collections import defaultdict, Counter
from datetime import timedelta, date
import pandas as pd
import csv

from appointments.models import Record

def render_df(request):
    """Retrieves all Records and creates a DataFrame for manager view.
    Converts data frame to HTML format and returns HTTPResponse"""
    records = Record.objects.all()
    data = {
        "Apt ID": [record.id for record in records],
        "Date": [record.dom.strftime("%b %d") for record in records],
        "Type": [record.type for record in records],
        "Time": [record.time for record in records],
        "Customer ID": [record.customer.id for record in records],
        "Earnings": [record.earnings for record in records],
    }
    df = pd.DataFrame(data)
    table_html = df.to_html(index=False, classes="table table-striped custom-table")

    return HttpResponse(table_html)

def export_apt_data(request):
    """Provides a CSV file of all records"""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="appointment_record.csv"'

    writer = csv.writer(response)
    writer.writerow(["Record ID", "Type", "Time", "Date", "Customer ID", "Earnings"])

    users = Record.objects.all().values_list(
        "id", "type", "time", "dom", "customer", "earnings"
    )
    for user in users:
        writer.writerow(user)

    return response

def chart_view(request):
    """Presents Manager's data visualisation page and provides earnings data"""
    today = date.today()
    records = Record.objects.all()
    earnings = 0
    for record in records:
        earnings += record.earnings
    context = {"earnings": earnings, "today": today.strftime("%A, %d %B")}

    return render(request, "chart.html", context)

#Redundant
"""def get_weeks(request):
    year = 2023
    weeks = []
    # Get the first day of the year
    current_date = datetime.date(year, 1, 1)
    # Find the first Monday of the year
    while current_date.weekday() != 0:  # 0 represents Monday
        current_date += timedelta(days=1)
    # Generate the list of weeks
    while current_date.year == year:
        weeks.append(current_date)
        current_date += timedelta(weeks=1)
    data = {"r": 1}
    for d in weeks:
        if Appointment.objects.get(dom=d) != None:
            e = d.strftime("%d:%m:%Y")
            data.update({e: Appointment.objects.get(dom=d)})
        else:
            pass

    return JsonResponse(data, safe=False)"""

#Record info functions provide data to enable graph rendering
def record_info(request):
    return JsonResponse(earnings_by_date())

def record_info_2(request):
    earnings_dict = earnings_by_date()
    # returns dictionary [key = date, value = earnings int]
    dates = list(earnings_dict.keys())
    earnings = list(earnings_dict.values())
    result = {}
    sum_earnings = 0
    for i in range(0, len(dates), 7):
        sum_earnings += sum(earnings[i : i + 7])
        key = dates[i]
        # add the values between index i and index i+7
        value = sum_earnings
        result[key] = value
    res = dict(result)
    return JsonResponse(res)

def record_info_3(request):
    # return json response with dict (keys = apt type, values = number of apts for each)
    records = Record.objects.all().order_by("dom")
    record_types = []
    for rec in records:
        record_types.append(rec.type)

    counts = Counter(record_types)

    result = dict(counts)

    return JsonResponse(result)

def record_info_4(request):
    records = Record.objects.all().order_by("type")
    apt_earnings = []

    for r in records:
        apt_earnings.append(f"{r.type}:{r.earnings}")

    result = {}

    for string in apt_earnings:
        key, value = string.split(":")
        key = key.strip()  # Remove leading/trailing spaces
        value = int(value)
        result[key] = result.get(key, 0) + value

    return JsonResponse(result)

def earnings_by_date():
    """Returns a dict with key=Datestring value=Earnings for that date"""
    
    #get dates for earliest and latest records
    records = Record.objects.all().order_by("dom") 
    first_date = min(record.dom for record in records)
    last_date = max(record.dom for record in records)

    # Generate a range of dates between the first and last date (inclusive)
    date_range = []
    for i in range((last_date - first_date).days + 1):
        date_range.append(first_date + timedelta(days=i))

    # Build the dictionary with the dates and initial earnings of 0.0
    #Defaultdict handles missing dates sets default value of 0.0
    earnings_dict = defaultdict(
        float
    )
    for date in date_range:
        date_str = date.strftime("%d-%b")
        earnings_dict[date_str] = 0.0

    # Aggregate the earnings from the record objects
    # iterate through the records
    # make a date string to serve as dict key
    # for each record with that dict key, append record earnings
    # this will aggregate earnings for each date
    for record in records:
        date_str = record.dom.strftime("%d-%b")
        earnings_dict[date_str] += record.earnings
    # Convert the defaultdict to a regular dictionary
    earnings_dict = dict(earnings_dict)
    return earnings_dict
