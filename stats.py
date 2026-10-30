import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_job_postings_by_sector(data: pd.DataFrame, sectors: np.ndarray, country_code: str):
  ''' Create plots for job postings for each sector from 'sectors' argument.
      All plots are created on the same figure and show the dynamics of job
      postings for all sectors provided by 'data' argument.
      
      Args:
        data (pandas.DataFrame) : Data for job postings in all sectors for a specific country 
        sectors (numpy.ndarray) : Sectors that are used to categorize data provided
        country_code (str) : Two-character ISO 3166-1 alpha-2 country code
        
      Returns:
        None
  '''
  # create new figure
  plt.figure(figsize=(14, 6))
    
  # plot job postings for every sector present in data file
  for sector in sectors:
    # extract the subset of data defined by sector, including only the number of total postings for the plot
    subset = data[(data['display_name'] == sector) & (data['variable'] == 'total postings')]
    plt.plot(subset['date'], subset['indeed_job_postings_index'], linewidth=1.5, label=f'{sector}')
    
  # Modify presentation of plots' X axis
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
  plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))

  # Modify plots' metadata and presentation
  plt.title(f'Job postings by sector ({country_code})')
  plt.xlabel('Date (X-axis)')
  plt.ylabel('Indeed job posting index (Y-axis)')
  plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='x-small', ncol=1)
  plt.subplots_adjust(right=0.8)
  plt.grid(True)
  plt.xticks(rotation=45)
  
  
def list_job_postings_by_sector(data: pd.DataFrame, sectors: np.ndarray):
  ''' List job postings by sector in descending order by the average 
      of indeed job postings index (which is a percent change in 
      seasonally-adjusted postings since February 1, 2020). The average
      value is calculated only for the last year.
  
      Args:
        data (pandas.DataFrame) : Data for job postings in all sectors for a specific country 
        sectors (numpy.ndarray) : Sectors that are used to categorize data provided
          
      Returns:
        list: The list of sector names listed in descending order based  
        on their average indeed job posting index over last year 
  '''
  
  
  
  return []

def display_statistics(country_code: str):
  ''' Display statistics on job postings by sector for a country,
      specified by a given country code. Achieve this by creating 
      plots for dynamics of job postings by sector using data provided
      by indeed. Then print list of sectors in descending order of their 
      average values of indeed job postings index over last year. 
      The x-axis for all plots is presented in year-month format, once
      per three months. The legend shows each sector of plots present on 
      figure.
      
      Args:
        country_code (str) : Two-character ISO 3166-1 alpha-2 country code
        
      Returns:
        None
  '''
  data_csv = pd.read_csv(f'job_postings_by_sector_{country_code}.csv')
  data_csv['date'] = pd.to_datetime(data_csv['date']) # change format (strings -> datetime objects)
  categories = data_csv['display_name'].unique()
  
  plot_job_postings_by_sector(data_csv, categories, country_code)
  sectors_list = list_job_postings_by_sector(data_csv, categories)
  
  print(f'List of average job posting index in {country_code}:')
  for item in sectors_list:
    print(item)
    
  print('\n')


display_statistics('US')
display_statistics('DE')
display_statistics('FR')

plt.show()

