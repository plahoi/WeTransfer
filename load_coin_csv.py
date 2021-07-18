import components

start_date, end_date = components.dates_threshold()
# Let's get the data we need!
data = components.get_coin_data(start_date, end_date)
data = components.trim_dataframe(data, start_date, end_date)

data.to_csv('output/wetransfer_out.csv')
