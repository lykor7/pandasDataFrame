import pandas as pd
import numpy as np

flexible_time = input("是否为连续数据（是：1，否：0）:")
period = []
def check_flexible(s):
    if s == '0':
        start_date = input('输入开始日期：')
        end_date = input('输入结束日期：')
        period.append(pd.date_range(start=start_date, end= end_date))
        flexible_again = input("下面的数据是否连续（是：1，否：0）:")
        return check_flexible(flexible_again)
    elif s == '1':
        start_date = input('输入开始日期：')
        end_date = input('输入结束日期：')
        period.append(pd.date_range(start=start_date, end= end_date))
        return period
result = check_flexible(flexible_time)
combined_data_range = period[0]
for r in result:
    combined_data_range = combined_data_range.union(r)

df = pd.DataFrame(combined_data_range, columns=['日期'])
    
# Add columns based on the given requirements
df['周几(1~7)'] = df['日期'].dt.weekday + 1  # Monday=1, Sunday=7
df['是否是周初(0/1)'] = np.where(df['周几(1~7)'] == 1, 1, 0)
df['是否是周末(0/1)'] = np.where(df['周几(1~7)'] == 7, 1, 0)
df['是当前月的第几天(1~31)'] = df['日期'].dt.day
df['是否是月初(0/1)'] = np.where(df['日期'].dt.is_month_start, 1, 0)
df['是否是月末(0/1)'] = np.where(df['日期'].dt.is_month_end, 1, 0)
    
# Calculate the start of the quarter and the day of the quarter
df['Quarter_Start'] = df['日期'].dt.to_period('Q').apply(lambda r: r.start_time)
df['是当前季度的第几天(1~93)'] = (df['日期'] - df['Quarter_Start']).dt.days + 1
    
# Add columns for first and last day of the quarter
df['是否是季初(0/1)'] = np.where(df['日期'].dt.is_quarter_start, 1, 0)
df['是否是季末(0/1)'] = np.where(df['日期'].dt.is_quarter_end, 1, 0)
    
# Add columns for the day of the year
df['是当前年度的第几天(1~366)'] = df['日期'].dt.dayofyear
df['是否是年初(0/1)'] = np.where(df['日期'].dt.is_year_start, 1, 0)
df['是否是年末(0/1)'] = np.where(df['日期'].dt.is_year_end, 1, 0)
    
# Drop the temporary Quarter_Start column
df.drop(columns=['Quarter_Start'], inplace=True)

file_name = input('输入想要存储的文件名称: ')
    
df.to_csv(file_name + '.csv', index=False)
    
# Display the resulting DataFrame
print(df)

    
    
   