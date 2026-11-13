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
  

def get_averages(data: pd.DataFrame, start_year: int, end_year: int):
  averages = pd.DataFrame(columns=['Year', 'Average value'])
  years = []
  values = []
  
  for year in range(start_year, end_year + 1):
    start_date = pd.to_datetime(f'{year}-01-01')
    end_date = pd.to_datetime(f'{year}-12-31')
    
    mask = (data['date'] >= start_date) & (data['date'] <= end_date)
    filtered_data = data[mask]

    values.append(calculate_averages(filtered_data['indeed_job_postings_index'].to_numpy()))
    years.append(pd.to_datetime(str(year)))
    
  averages['Year'] = np.array(years)
  averages['Average value'] = np.array(values)

  return averages

def calculate_averages(values: np.ndarray):
  # zero division check
  if len(values) > 0:
    return np.mean(values)
  else:
    return 0.0
   
    
def list_in_table(x_values: np.ndarray, y_values: pd.DataFrame, table_title: str, column_names: list[str]):  
  x_column = column_names[0]
  df = pd.DataFrame({x_column: x_values})
  df = pd.concat([df, y_values], axis=1)
    
  # removing standard plot axices
  plt.axis('off')
  plt.axis('tight')
  
  # sort in descending order
  df = df.sort_values(by=column_names[-1], ascending=False)
  df = df.reset_index(drop=True)
  
  # round average values
  for column_name in column_names:
    if pd.api.types.is_numeric_dtype(df[column_name]):
      df[column_name] = df[column_name].round(2)
    
  plt.title(table_title, fontsize=10, pad=60)
          
  the_table = plt.table(
    cellText=df,
    loc='center',
    cellLoc='center'
  )
  
  the_table.auto_set_font_size(False)
  the_table.set_fontsize(8)
  the_table.scale(1.2, 0.7)


def display_statistics(country_code: str):
  #################### prepare data for analysis ####################
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
  
  # slice data by specific year
  df_postings = df_postings[(df_postings['date'] >= pd.to_datetime('2022-02-01'))] 
  df_ai = df_ai[(df_ai['date'] >= pd.to_datetime('2022-02-01'))] 
  
  #################### plot graphs for ai postings on indeed ####################
  
  # # create new figure
  # plt.figure(figsize=(14, 6))
  
  # # plot regular ai postings
  # plot_graph(
  #   df_ai['date'].to_numpy(dtype='datetime64[D]'), 
  #   df_ai['AI_share_postings'].to_numpy(), 
  #   graph_title=f'Percentage of AI postings ({country_code})',
  #   graph_label='AI',
  #   x_label='Date (X-axis)',
  #   y_label='Percentage of AI postings (Y-axis)'
  # )
  
  # plt.show()
  # plt.close()
  
  #################### plot graphs for job postings on indeed ####################
  
  # # create new figure
  # plt.figure(figsize=(14, 6))
    
  for sector in categories:
    subset = df_postings[(df_postings['display_name'] == sector)]
    
    # # plot regular job postings
    # plot_graph(
    #   subset['date'].to_numpy(dtype='datetime64[D]'),
    #   subset['indeed_job_postings_index'].to_numpy(),
    #   graph_title=f'Job postings by sector ({country_code})',
    #   graph_label=sector,
    #   x_label='Date (X-axis)',
    #   y_label='Indeed Job Posting Index (Y-axis)'
    # )

    # # plot average job postings
    # averages = get_averages(subset, 2020, 2026)    
        
    # plot_graph(
    #   averages['Year'].to_numpy(dtype='datetime64[D]'),
    #   averages['Average value'].to_numpy(),
    #   graph_title=f'Average Job Postings by Sector per Year ({country_code})',
    #   graph_label=sector,
    #   x_label='Year (X-axis)',
    #   y_label='Average Indeed Job Posting Index (Y-axis)'
    # )
    
    # # plot 'derivatives' for job postings
    # plot_graph(
    #   subset['date'][:-1].to_numpy(dtype='datetime64[D]'), 
    #   get_derivatives(subset['indeed_job_postings_index'].to_numpy()), 
    #   graph_title=f'Derivatives for job postings by sector ({country_code})',
    #   graph_label=sector,
    #   x_label='Date (X-axis)',
    #   y_label='Derivative value of Indeed Job Posting Index (Y-axis)'
    # )
    
    # # plot linear regressions for job postings
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
    
  # plt.show()
  # plt.close()

  ############### list all average job posting indexes by year for each sector ############### 
  
  all_averages: dict[str, list[float]] = {}
  years = []
  
  start_year = 2022
  end_year = 2026
  
  for i in range(start_year, end_year + 1):
    years.append(str(i))
    all_averages[years[i - start_year]] = []
    
  # create new figure
  plt.figure(figsize=(14, 6))
    
  for sector in categories:
    subset = df_postings[(df_postings['display_name'] == sector)]
    sector_averages = get_averages(subset, start_year, end_year)
    for i in range(start_year, end_year + 1):
      filtered_by_year = sector_averages[(sector_averages['Year'].dt.year == i)]
      all_averages[years[i - start_year]].append(filtered_by_year['Average value'].iloc[0])

  list_in_table(
    categories,
    pd.DataFrame(all_averages, columns=years), 
    table_title=f'Table of Average Indeed Job Postings Index per year ({country_code})',
    column_names=['Sector']+years
  )
      
  # plt.show()
  # plt.close()


display_statistics('US')
display_statistics('DE')
display_statistics('FR')


plt.show()
plt.close()