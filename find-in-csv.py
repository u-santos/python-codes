import os
import pandas as pd

def check_files(file_path, csv_folder, chunksize=10000):
    founds = 0
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for filename in os.listdir(csv_folder):
            if filename.endswith('.csv'):
                csv_path = os.path.join(csv_folder, filename)
                print(f'Checking on {csv_path}.')
                for chunk in pd.read_csv(csv_path, usecols=['video_id'], chunksize=chunksize):
                    chunk_str = chunk.to_string()
                    for line in lines:
                        search_text = line.strip()
                        count = chunk_str.count(search_text)
                        if count > 0:
                            print(f'A linha "{search_text}" foi encontrada {count} vezes em {csv_path}!')
                            founds += count
    print(f'Total encontrado: {founds}')

def main():
    files_txt_path = '/home/ec2-user/file'
    csv_folder_path = '/home/ec2-user/csv'

    check_files(files_txt_path, csv_folder_path)

if __name__ == '__main__':
    main()