from datetime import date


d = date.today().strftime('%Y%m%d')
csv_file = f'path/housing_{d}.csv'
txt_file = f'path/failed_{d}.txt'