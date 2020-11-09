import local_config

import os
import datetime


def get_date(file_name: str) -> datetime.date:
    date_string = file_name.replace(local_config.prefix, '').replace(local_config.postfix, '')
    return datetime.datetime.strptime(date_string, '%Y%m%d').date()

def main():
    header = True
    with open(local_config.output_file, 'w', encoding='utf-8') as f:
        for _, _, files in os.walk(local_config.root):
            for file_name in files:
                file_path = os.path.join(local_config.root, file_name)
                file_date = get_date(file_name)
                with open(file_path, 'r', encoding='utf-8') as f_day:
                    lines = f_day.readlines()
                    if header:
                        f.write(lines[0])
                        header = False
                    lines = lines[1:]
                    for line in lines:
                        line = line.rstrip('\n')
                        f.write(f'{line}, {file_date}\n')
                    


if __name__ == "__main__":
    main()
