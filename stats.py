import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# read CSV data
data_csv = pd.read_csv('job_postings_by_sector_US.csv')
data_csv['date'] = pd.to_datetime(data_csv['date'])

categories = data_csv['display_name'].unique()

# print("Available categories: ", categories)

plt.figure(figsize=(14, 6))

for sector in categories:
  subset = data_csv[(data_csv['display_name'] == sector) & (data_csv['variable'] == 'total postings')]
  plt.plot(subset['date'], subset['indeed_job_postings_index'], linewidth=1.5, label=f'{sector}')
  
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))

plt.title('Job postings by sector (US)')
plt.xlabel('Date (X-axis)')
plt.ylabel('Indeed job posting index (Y-axis)')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='x-small', ncol=1)
plt.subplots_adjust(right=0.8)
plt.grid(True)
plt.xticks(rotation=45)

plt.show()

