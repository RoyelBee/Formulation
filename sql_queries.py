import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyodbc as db
import calendar
import datetime

now = datetime.datetime.now()
days_in_month = calendar.monthrange(now.year, now.month)[1]
covered_day = now.day - 1
remaining_day = days_in_month - covered_day

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=137.116.139.217;'
                        'DATABASE=ARCHIVESKF;'
                        'UID=sa;PWD=erp@123')


def money_converter(taka):
    if len(str(taka)) >= 8:
        val = str(round(taka / 10000000, 2)) + ' Cr'

    elif len(str(taka)) >= 6:
        val = str(round(taka / 100000, 2)) + ' Lac'

    elif len(str(taka)) >= 4:
        val = str(round(taka / 1000, 2)) + ' Th'

    else:
        val = taka
    return val


monthly_trg = """select sum(target) as TodaysTarget
from RfieldForce
where YEARMONTH = convert(varchar(6),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112)
"""
monthly_trgdf = pd.read_sql_query(monthly_trg, connection)
monthly_trg = int(monthly_trgdf.TodaysTarget)

monthly_sales = """select right(transdate, 2) as date, sum(extinvmisc) as sales
                from OESalesDetails
                where left(TRANSDATE, 6) =  convert(varchar(6),DATEADD(D,0,GETDATE()-1),112)
                group by TRANSDATE
                order by TRANSDATE desc
                 """
monthly_day_wise_current_sales = pd.read_sql_query(monthly_sales, connection)
mtd_sales = monthly_day_wise_current_sales.sales.tolist()
todays_sales = monthly_day_wise_current_sales.sales[0]

remaining_target = monthly_trg - sum(mtd_sales)
todays_target = round(remaining_target / remaining_day)

# print('Todays Target = ', money_converter(todays_target))
# print('Todays Sales  = ', money_converter(todays_sales))

todays_achv = str(round(((todays_sales / todays_target) * 100), 2)) + ' %'
# print('Todays Achiv  = ', todays_achv)

