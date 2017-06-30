from framework.helpers.db_helper import *
import json
import time

def get_hours_for_brand(id):

    days_arr = ["sun", "sat", "mon", "tue", "wed", "thu", "fri"]

    days_dict = {
                "sun": {
                    "start_time": {"closed": 0},
                    "end_time": {"closed": 0}
                },
                "sat": {
                    "start_time": {"closed": 0},
                    "end_time": {"closed": 0}
                },
                "mon": {
                    "start_time": {"closed": 0},
                    "end_time": {"closed": 0}
                },
                "tue": {
                    "start_time": {"closed": 0},
                    "end_time": {"closed": 0}
                },
                "wed": {
                    "start_time": {"closed": 0},
                    "end_time": {"closed": 0}
                },
                "thu": {
                    "start_time": {"closed": 0},
                    "end_time": {"closed": 0}
                },
                "fri": {
                    "start_time": {"closed": 0},
                    "end_time": {"closed": 0}
                }
                }

    conn = db_pg_connect()
    cursor = conn.cursor()
    query = """select hours,p."hashKey" from poi p where p."brandId"="""+str(id)+""" and p."hide"=false and p."del"=false and p."hours" is not null and p."country"='US' """
    cursor.execute(query)
    records = cursor.fetchall()
    records_size = cursor.rowcount

    if records_size > 20:

        for row in records:
            arr = json.dumps(row[0])
            days = json.loads(arr)
            days_present = []

            for i in range(len(days)):
                if days[i]['days'] is not None:
                    days_final = days[i]['days']
                    for ele in days_final:
                        days_present.append(ele)

            for i in range(len(days)):

                if days[i]['days'] is not None:

                    days_final = days[i]['days']

                    for x in days_arr:

                        if str(x) in days_final:

                           # start time
                           if days_dict[str(x)]['start_time'] is None:

                               days_dict[str(x)]['start_time'] = dict()
                               days_dict[str(x)]['start_time'][str(days[i]['start_time'])] = 1
                           else:

                               dict = days_dict[str(x)]['start_time']
                               if days[i]['start_time'] in dict:
                                   days_dict[str(x)]['start_time'][days[i]['start_time']] = days_dict[str(x)]['start_time'][days[i]['start_time']]+1

                               else:
                                   days_dict[str(x)]['start_time'][days[i]['start_time']] = 1

                           # end time
                           if days_dict[str(x)]['end_time'] is None:

                               days_dict[str(x)]['end_time'] = dict()
                               days_dict[str(x)]['end_time'][str(days[i]['end_time'])] = 1
                           else:

                               dict = days_dict[str(x)]['end_time']
                               if days[i]['end_time'] in dict:
                                   days_dict[str(x)]['end_time'][days[i]['end_time']] = days_dict[str(x)]['end_time'][days[i]['end_time']]+1

                               else:
                                   days_dict[str(x)]['end_time'][days[i]['end_time']] = 1

            days_absent=[]
            for ele in days_arr:
                if ele not in days_present:
                    days_absent.append(ele)

            for ele in days_absent:

               days_dict[str(ele)]['start_time']['closed'] += 1
               days_dict[str(ele)]['end_time']['closed'] += 1


        time_final = {}
        for ele in days_arr:
            start_key = ele+"_start_time"
            end_key = ele+"_end_time"
            max = -1
            max1 = -1
            val = days_dict[ele]
            start_time = val['start_time']
            end_time = val['end_time']
            for x in start_time:
                if max < int(start_time[x]):
                    max = int(start_time[x])
                    time_final[start_key] = x
            for y in end_time:
                if max1 < int(end_time[y]):
                    max1 = int(end_time[y])
                    time_final[end_key] = y

    for key in time_final:
        if time_final[key] is not "closed":
            t = time.strptime(str(time_final[key]),"%H:%M:%S")
            timevalue = time.strftime("%I:%M%p",t)
            time_final[key] = timevalue
        else:
            time_final[key] = "Closed"

    formatted_days = {}
    formatted_days['Monday'] = str(time_final['mon_start_time'])+"-"+str(time_final['mon_end_time'])
    formatted_days['Tuesday'] = str(time_final['tue_start_time'])+"-"+str(time_final['tue_end_time'])
    formatted_days['Wednesday'] = str(time_final['wed_start_time'])+"-"+str(time_final['wed_end_time'])
    formatted_days['Thursday'] = str(time_final['thu_start_time'])+"-"+str(time_final['thu_end_time'])
    formatted_days['Friday'] = str(time_final['fri_start_time'])+"-"+str(time_final['fri_end_time'])
    formatted_days['Saturday'] = str(time_final['sat_start_time'])+"-"+str(time_final['sat_end_time'])
    formatted_days['Sunday'] = str(time_final['sun_start_time'])+"-"+str(time_final['sun_end_time'])

    for keys in formatted_days:
        val = formatted_days[keys]
        if "Closed" in str(val):
            formatted_days[keys]= "Closed"


    db_close_connection(conn)
    return formatted_days


