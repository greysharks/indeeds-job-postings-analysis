import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_graph(x_values: np.ndarray, y_values: np.ndarray, graph_title: str, graph_label: str, x_label: str, y_label: str):
  plt.plot(x_values, y_values, linewidth=1.5, label=graph_label)

  # Modify presentation of plots' X axis
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
  plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
  
  # Modify plots' metadata and presentation
  plt.title(graph_title)
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='x-small', ncol=1)
  plt.subplots_adjust(right=0.8)
  plt.grid(True)
  plt.xticks(rotation=45)

  
def get_derivatives(data: np.ndarray):
  return data[1:] - data[:-1]

  
def get_linear_regressions(x_values: np.ndarray, y_values: np.ndarray):
  # turn datetime into time intervals in form of floats
  x_values = (x_values - x_values.min()).astype('timedelta64[D]').astype('float') 
  
  # normalize data
  y_mean = np.mean(y_values)
  x_mean = np.mean(x_values)
  y_std = np.std(y_values)
  x_std = np.std(x_values)
  
  y_values = (y_values - y_mean) / y_std
  x_values = (x_values - x_mean) / x_std
    
  # calculate linear regression algorithms
  params = linear_regression(x_values, y_values)
  h_func = params[0] + params[1] * x_values
    
  # print(params[1])
  return h_func * y_std + y_mean
  

def plot_average_job_postings_by_sector(data: pd.DataFrame, sectors: np.ndarray, country_code: str):
  ''' Create plots for job postings for each sector from 'sectors' argument, based
      on their average per year. All plots are created on the same figure and show 
      the dynamics of job postings for all sectors provided by 'data' argument.
      
      Args:
        data (pandas.DataFrame) : Data for job postings in all sectors for a specific country 
        sectors (numpy.ndarray) : Sectors that are used to categorize data provided
        country_code (str) : Two-character ISO 3166-1 alpha-2 country code
        
      Returns:
        None
  '''
  list_of_averages = []
  years = list(range(2020, 2027))
  
  for year in years:
    # Saving averages per year
    avg_dict = calculate_averages(data, sectors, year)
    avg_dict['Year'] = str(year) # Adding year for X axis
    list_of_averages.append(avg_dict)
      
  # Creating DataFrame, where rows represent years and columns represent sectors
  df_avg = pd.DataFrame(list_of_averages)
  df_avg.set_index('Year', inplace=True)
  
  # Plotting each sector
  for sector in sectors:
      if sector in df_avg.columns:
          plt.plot(df_avg.index, df_avg[sector], linewidth=1.5, label=sector, marker='o')
          
  plt.title(f'Average Job Postings by Sector per Year ({country_code})')
  plt.xlabel('Year (X-axis)')
  plt.ylabel('Average Indeed Job Posting Index (Y-axis)')


def calculate_averages(data: pd.DataFrame, sectors: np.ndarray, year: int):
  ''' Calculate average values for given sectors per given year.

      Args:
        data (pandas.DataFrame) : Data for job postings in all sectors for a specific country 
        sectors (numpy.ndarray) : Sectors that are used to categorize data provided
        year (int) : Base year for averages
        
      Returns:
        None
  '''
  
  averages = {}
  start_date = f'{year}0101'
  end_date = f'{year}1231'
  
  mask = (data['date'] >= start_date) & (data['date'] <= end_date)
  filtered_data = data[mask]
  
  for sector in sectors:
    subset = filtered_data[(filtered_data['display_name'] == sector)]
    
    # zero division check
    if len(subset) > 0:
      averages[sector] = np.mean(subset['indeed_job_postings_index'])
    else:
      averages[sector] = 0.0
          
  return averages
    
def list_job_postings_by_sector(data: pd.DataFrame, sectors: np.ndarray, country_code: str):
  ''' List job postings by sector in descending order by the average 
      of indeed job postings index (which is a percent change in 
      seasonally-adjusted postings since February 1, 2020). The average
      value is calculated only for the year specified.
  
      Args:
        data (pandas.DataFrame) : Data for job postings in all sectors for a specific country 
        sectors (numpy.ndarray) : Sectors that are used to categorize data provided
        year (int) : Year to calculate the average job postings index over
        country_code (str) : Two-character ISO 3166-1 alpha-2 country code
          
      Returns:
        list: The list of sector names listed in descending order based  
        on their average indeed job posting index over last year 
  '''
  year = 2026
  
  fig, ax = plt.subplots(figsize=(10, 8))
  
  # removing standard plot axices
  ax.axis('off')
  ax.axis('tight')
    
  # convert dictionary to DataFrame type
  table_data = pd.DataFrame(
    list(calculate_averages(data, sectors, year).items()), 
    columns=['Sector', 'Average Indeed Job Postings Index']
  )
  # sort in descending order
  table_data = table_data.sort_values(by='Average Indeed Job Postings Index', ascending=False)
  
  # remove index numbers for the table rows
  table_data = table_data.reset_index(drop=True)

  col_labels = table_data.columns.tolist()
  cell_text = table_data.values.tolist()
  
  # round average values
  for row in cell_text:
    for i in range(len(row)):
      if isinstance(row[i], (int, float)):
        row[i] = round(row[i], 2)
          
  the_table = ax.table(
    cellText=cell_text,
    colLabels=col_labels,
    loc='center',
    cellLoc='center'
  )
  
  the_table.auto_set_font_size(False)
  the_table.set_fontsize(8)
  the_table.scale(0.7, 0.9)
  
  ax.set_title(f'Table of Average Indeed Job Postings Index over year {str(year)} ({country_code})', fontsize=12, pad=50)


def display_statistics(country_code: str):
  ''' Display statistics on job postings by sector for a country,
      specified by a given country code. Achieve this by creating 
      plots for dynamics of job postings by sector using data provided
      by indeed. Then print list of sectors in descending order of their 
      average values of indeed job postings index over specified year. 
      The x-axis for all plots is presented in year-month format, once
      per three months. The legend shows each sector of plots present on 
      figure.
      
      Args:
        country_code (str) : Two-character ISO 3166-1 alpha-2 country code
        
      Returns:
        None
  '''
  # read data
  df_ai = pd.read_csv('AI_posting.csv')
  df_postings = pd.read_csv(f'job_postings_by_sector_{country_code}.csv')
  
  # change format (strings -> datetime objects)
  df_ai['date'] = pd.to_datetime(df_ai['date'])
  df_postings['date'] = pd.to_datetime(df_postings['date']) 
  
  # include only total postings
  df_postings = df_postings[(df_postings['variable'] == 'total postings')]
  
  # specify country for ai postings   
  df_ai = df_ai[(df_ai['jobcountry'] == country_code)]
  
  categories = df_postings['display_name'].unique() 
  # print(categories)
  
  # # slice data
  # df_postings = df_postings[df_postings['date'] >= pd.to_datetime('2022-01-01')]
  
  # create new figure
  plt.figure(figsize=(14, 6))
  
  # plot ai postings
  
  plot_graph(
    df_ai['date'].to_numpy(dtype='datetime64[D]'), 
    df_ai['AI_share_postings'].to_numpy(), 
    graph_title=f'Percentage of AI postings ({country_code})',
    graph_label='AI',
    x_label='Date (X-axis)',
    y_label='Percentage of AI postings (Y-axis)'
  )
  
  plt.show()
  
  # create new figure
  plt.figure(figsize=(14, 6))
  
  for sector in categories:
    subset = df_postings[(df_postings['display_name'] == sector)]
    
    plot_graph(
      subset['date'].to_numpy(dtype='datetime64[D]'),
      subset['indeed_job_postings_index'].to_numpy(),
      graph_title=f'Job postings by sector ({country_code})',
      graph_label=sector,
      x_label='Date (X-axis)',
      y_label='Indeed Job Posting Index (Y-axis)'
    )
    
    # plot_graph(
    #   subset['date'][:-1].to_numpy(dtype='datetime64[D]'), 
    #   get_derivatives(subset['indeed_job_postings_index'].to_numpy()), 
    #   graph_title=f'Derivatives for job postings by sector ({country_code})',
    #   graph_label=sector,
    #   x_label='Date (X-axis)',
    #   y_label='Derivative value of Indeed Job Posting Index (Y-axis)'
    # )
    
    # plot_graph(
    #   subset['date'].to_numpy(dtype='datetime64[D]'), 
    #   get_linear_regressions(
    #     subset['date'].to_numpy(dtype='datetime64[D]'), 
    #     subset['indeed_job_postings_index'].to_numpy()
    #   ), 
    #   graph_title=f'Linear regressions for job postings by sector ({country_code})',
    #   graph_label=sector,
    #   x_label='Date (X-axis)',
    #   y_label='Indeed Job Posting Index (Y-axis)'
    # )

  plt.show()
  
  # list_job_postings_by_sector(df_postings, categories, country_code)
  # plot_average_job_postings_by_sector(df_postings, categories, country_code)
  

  
def linear_regression(x_values: np.ndarray, y_values: np.ndarray):
  theta = np.random.randn(2)
  alpha = 0.01 # learning rate
  
  J_theta = sum((theta[0] + theta[1] * x_values - y_values)**2) / 2
  # print(J_theta)
  
  for i in range(0, 1000):
    partial_drv = (theta[0] + theta[1] * x_values) - y_values
    theta[0] -= alpha * 2 * np.mean(partial_drv)
    theta[1] -= alpha * 2 * np.mean(x_values * partial_drv)
    
  J_theta = sum((theta[0] + theta[1] * x_values - y_values)**2) / 2
  # print(J_theta)
  
  return theta

display_statistics('US')
# display_statistics('DE')
# display_statistics('FR')
