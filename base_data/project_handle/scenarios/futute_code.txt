# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
from scenario_forecast import main

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
f_df, fc_df = main.run()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
scenario_future_schedule = dataiku.Dataset("scenario_future_schedule")
scenario_future_schedule.write_with_schema(f_df)

scenario_future_schedule_cleansed = dataiku.Dataset("scenario_future_schedule_cleansed")
scenario_future_schedule_cleansed.write_with_schema(fc_df)


import dataiku
import pandas as pd
from scenario_forecast import get_future_schedule


def run():
    client = dataiku.api_client()
    project_keys = client.list_project_keys()

    schedule_data = []
    for key in project_keys:
        project_handle = client.get_project(project_key=key)
        for scenario in project_handle.list_scenarios():
            if not scenario["active"]:
                continue
            scenario_handle = project_handle.get_scenario(scenario_id=scenario["id"])
            settings_settings = scenario_handle.get_settings()
            for trigger in settings_settings.raw_triggers:
                if trigger['type'] != "temporal":
                    continue
                params = trigger['params']
                data = get_future_schedule.run(key, scenario["id"], params)
                schedule_data += data

    future_schedule_raw_df = pd.DataFrame(schedule_data, columns=["project_key", "scenario_id", "next_run"])
    
    # Lets data cleanse this for charting
    df = future_schedule_raw_df.copy(deep=True)
    df['year']   = df['next_run'].dt.year
    df['month']  = df['next_run'].dt.month
    df['day']    = df['next_run'].dt.day
    df['hour']   = df['next_run'].dt.hour
    df['minute'] = df['next_run'].dt.minute
    df = df.groupby(by=['year', 'month', 'day', 'hour']).count().reset_index()
    del df['project_key']
    del df['scenario_id']
    del df['next_run']
    df['time_series'] = df['year'].astype(str) + '/' + df['month'].astype(str) + '/' + df['day'].astype(str) + ' ' + df['hour'].astype(str) + ':00'
    df['time_series'] = pd.to_datetime(df['time_series'])
    df.rename(columns={'minute':'number_of_scenarios'}, inplace=True)
    future_schedule_cleansed_df = df[['time_series', 'year', 'month', 'day', 'hour', 'number_of_scenarios']]

    # Return both DF
    return future_schedule_raw_df, future_schedule_cleansed_df


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar


def rel_month(start_dt, week_num, dow):
    # fix for correct day
    year, month = start_dt.year, start_dt.month
    c = calendar.Calendar(firstweekday=calendar.SUNDAY)
    monthcal = c.monthdatescalendar(year, month)
    day = [
        day for week in monthcal for day in week if \
        day.weekday() == dow and \
        day.month == month
    ][week_num]
    start_dt = start_dt.replace(day = day.day)
    return start_dt


def run(key, scenario_id, params):
    # get initial start, and a rough ending
    start_dt   = f"{params['startingFrom']} {params['hour']}:{params['minute']:02d}"
    start_dt   = datetime.strptime(start_dt, "%Y-%m-%d %H:%M")
    current_dt = datetime.now()
    one_yr_dt  = current_dt + relativedelta(years=1)

    # Minute, Hour, Day, Week, Month
    data = []
    freq = params['repeatFrequency']

    if params['frequency']   == "Minutely":
        while current_dt >= start_dt:
            start_dt += timedelta(minutes=freq)
        start_dt -= timedelta(minutes=freq)
            
        while one_yr_dt > start_dt:
            data.append([key, scenario_id, start_dt])
            start_dt += timedelta(minutes=freq)

    elif params['frequency'] == "Hourly":
        while current_dt >= start_dt:
            start_dt += timedelta(hours=freq)
        start_dt -= timedelta(hours=freq)
        
        while one_yr_dt > start_dt:
            data.append([key, scenario_id, start_dt])
            start_dt += timedelta(hours=freq)

    elif params['frequency'] == "Daily":
        while current_dt >= start_dt:
            start_dt += timedelta(days=freq)
        start_dt -= timedelta(days=freq)
        
        while one_yr_dt > start_dt:
            data.append([key, scenario_id, start_dt])
            start_dt += timedelta(days=freq)

    elif params['frequency'] == "Weekly":
        while current_dt >= start_dt:
            start_dt += timedelta(weeks=freq)
        start_dt -= timedelta(weeks=freq)
        
        while one_yr_dt > start_dt:
            if "Monday" in params['daysOfWeek']:
                delta = 0 - start_dt.weekday()
                t = start_dt + timedelta(days=delta)
                data.append([key, scenario_id, t])
            if "Tuesday" in params['daysOfWeek']:
                delta = 1 - start_dt.weekday()
                t = start_dt + timedelta(days=delta)
                data.append([key, scenario_id, t])
            if "Wednesday" in params['daysOfWeek']:
                delta = 2 - start_dt.weekday()
                t = start_dt + timedelta(days=delta)
                data.append([key, scenario_id, t])
            if "Thursday" in params['daysOfWeek']:
                delta = 3 - start_dt.weekday()
                t = start_dt + timedelta(days=delta)
                data.append([key, scenario_id, t])
            if "Friday" in params['daysOfWeek']:
                delta = 4 - start_dt.weekday()
                t = start_dt + timedelta(days=delta)
                data.append([key, scenario_id, t])
            if "Saturday" in params['daysOfWeek']:
                delta = 5 - start_dt.weekday()
                t = start_dt + timedelta(days=delta)
                data.append([key, scenario_id, t])
            if "Sunday" in params['daysOfWeek']:
                delta = 6 - start_dt.weekday()
                t = start_dt + timedelta(days=delta)
                data.append([key, scenario_id, t])
            start_dt += timedelta(weeks=freq)

    elif params['frequency'] == "Monthly":
        if params["monthlyRunOn"] == 'ON_THE_DAY':
            while current_dt >= start_dt:
                start_dt += relativedelta(months=freq)
            start_dt -= relativedelta(months=freq)
        
            while one_yr_dt > start_dt:
                data.append([key, scenario_id, start_dt])
                start_dt += relativedelta(months=freq)
        else:
            dow = start_dt.weekday()
            c = calendar.Calendar(firstweekday=calendar.SUNDAY)
            year, month = start_dt.year, start_dt.month            
            monthcal = c.monthdatescalendar(year, month)
            weeks = [
                day for week in monthcal for day in week if \
                day.weekday() == dow and \
                day.month == month
            ]
            week_num = weeks.index(start_dt.date())
            if weeks[-1] == weeks[week_num]:
                week_num = -1
                
            while current_dt >= start_dt:
                start_dt += relativedelta(months=freq)
                start_dt = rel_month(start_dt, week_num, dow)
                
            # Lets go back 1
            start_dt -= relativedelta(months=freq)
            start_dt = rel_month(start_dt, week_num, dow)

            while one_yr_dt > start_dt:
                data.append([key, scenario_id, start_dt])
                start_dt += relativedelta(months=freq)
                start_dt = rel_month(start_dt, week_num, dow)
    else:
        raise Exception()

    return data