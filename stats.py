import pandas as pd
import matplotlib.pyplot as plt

# read CSV data
data_csv = pd.read_csv('job_postings_by_sector_US.csv')

filtered_data = data_csv[(data_csv['display_name'] == 'Accounting') & (data_csv['variable'] == 'total postings')]

# print(filtered_data)

filtered_data.plot(x='date', y='indeed_job_postings_index', kind='line', marker='o', color='b')

plt.title('Job postings for Accounting sector')
plt.xlabel('Date (X-axis)')
plt.ylabel('Indeed job posting index (Y-axis)')
plt.grid(True)
plt.xticks(rotation=45)

plt.show()

