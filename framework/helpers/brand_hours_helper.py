from framework.helpers.db_helper import *
import json
import time

def get_hours_for_brand(id):

    days_arr = ["sun", "sat", "mon", "tue", "wed", "thu", "fri"]
    days_map = {"sun": "Sunday", "sat": "Saturday", "mon": "Monday", "tue": "Tuesday", "wed": "Wednesday", "thu": " Thursday", "fri": "Friday"}
    days_dict_refactored ={}

    days_dict = {
                "sun": {"closed": 0},"sat": {"closed": 0},"mon": {"closed": 0},"tue": {"closed": 0},
                "wed": {"closed": 0},"thu": {"closed": 0},"fri": {"closed": 0}}

    days_dict_final = {"sun": {"closed": 0},"sat": {"closed": 0},"mon": {"closed": 0},"tue": {"closed": 0},
                        "wed": {"closed": 0},"thu": {"closed": 0},"fri": {"closed": 0}}

    conn = db_pg_connect()
    cursor = conn.cursor()
    query = """select hours,p."hashKey" from poi p where p."brandId"="""+str(id)+""" and p."hide"=false and p."del"=false and p."hours" is not null and p."country"='US'"""
    cursor.execute(query)
    records = cursor.fetchall()
    records_size = cursor.rowcount

    if records_size > 20:

        for row in records:

            hours = json.loads(json.dumps(row[0]))

            days_found = []
            days_remaining = []

            for ele in hours:
                days1 = ele['days']
                for ele in days1:
                    days_found.append(ele)
            for ele in days_arr:
                if ele not in days_found:
                    days_remaining.append(ele)

            for ele in hours:

                days = ele['days']

                for d in days:

                    start_time = ele['start_time']
                    end_time = ele['end_time']
                    t1 = time.strptime(str(start_time),"%H:%M:%S")
                    t2 = time.strptime(str(end_time),"%H:%M:%S")
                    timevalue1 = time.strftime("%I:%M%p",t1)
                    timevalue2 = time.strftime("%I:%M%p",t2)
                    hours_range = str(timevalue1)+"-"+str(timevalue2)
                    if hours_range in days_dict[d]:
                        days_dict[d][hours_range] += 1
                    else:
                        days_dict[d][hours_range] = 1

                if len(days_remaining) is not 0:
                    for day in days_remaining:
                        hours_range = "Closed"
                        if hours_range in days_dict[day]:
                            days_dict[day][hours_range] += 1
                        else:
                            days_dict[day][hours_range] = 1
    for ele in days_dict:
        max = -1
        val = days_dict[ele]
        for element in val:
            value = val[element]
            if max<value:
                max = value
                days_dict_final[ele]= element

    for key in days_dict_final:
        days_dict_refactored[days_map[key]] = days_dict_final[key]

    return days_dict_refactored









