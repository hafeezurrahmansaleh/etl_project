import os
import pathlib
import shutil
import sqlite3, pandas as pd, numpy as np

# dbname = 'FinanceExplainedDb'
# conn = sqlite3.connect(dbname + '.sqlite')
# cur = conn.cursor()
#
current_dir = pathlib.Path(__file__).parent
output_dir = os.path.join(current_dir, 'output\\')

current_dir = pathlib.Path(__file__).parent
inbound_dir = os.path.join(current_dir, 'inbound_files\\')
processed_dir = os.path.join(current_dir, 'processed_files\\')


# input_dir = os.path.join(current_dir, 'reports\\')
def process_files():
    file_names = os.listdir(inbound_dir)  # Get all report files from inbound_files dir

    for file_name in file_names:
        extracted_df = extract_data(file_name)
        load_into_db(extracted_df)
        if not os.path.isfile(os.path.join(processed_dir, file_name)):  # check if file already exists in  processed_files
            shutil.move(os.path.join(inbound_dir, file_name), processed_dir)  # Move processed file to processed_dir
            # processing
        else:
            os.remove('inbound_files/' + file_name)  # Remove if file is already exists in processed dir


def extract_data(file_name):
    file = os.path.join(inbound_dir, file_name)
    new_names = ['unnecessary', 'unnecessary', 'Name of the Power Station', 'unnecessary', 'Fuel', 'Producer',
                 'Installed Capacity(Unit No. X Capacity)',
                 'Installed Capacity(MW)', 'Present Capacity(MW)', 'Yesterday Day Peak(MW)', 'Yesterday Ev. Peak(MW)', 'Today Day Peak(MW)',
                 'Today Ev. Peak(MW)', 'Ev. Shortage for Fuel(MW)',
                 'Ev. Shortage for plant problem(MW)', 'Remark', 'unnecessary', 'Probable Start up Date', 'unnecessary', ]
    dataset = pd.read_excel(file, sheet_name='Forecast', names=new_names, na_values=['NA'], )

    # get index of start and end rows for relevant data
    row_start = 0
    row_end = 0
    area_total_indexes = []
    for row in range(dataset.shape[0]):
        for col in range(dataset.shape[1]):
            if dataset.iat[row, col] == 'Unit No. X Capacity':
                row_start = row
            if str(dataset.iat[row, col]).replace(' ', '') == 'Total':
                row_end = row
                print(row_end)
                break
            if 'area total' in str(dataset.iat[row, col]).lower():
                print(str(dataset.iat[row, col]).lower())
                area_total_indexes.append(dataset.loc[row:row].index.item())
        if row_start and row_end:
            break
    print(area_total_indexes)
    dataset = dataset.drop(labels=area_total_indexes, axis=0)
    # RPick only relevant rows
    df_required = dataset.loc[row_start + 1:row_end - 1]

    # Remove unnecessary columns
    df_required.drop(df_required.columns[df_required.columns.str.contains('unnecessary', case=False)], axis=1, inplace=True)

    # Remove Area total rows

    # Get report date from the same sheet
    report_date = ''
    for row in range(dataset.shape[0]):
        for col in range(dataset.shape[1]):
            if dataset.iat[row, col] == 'Date (day):':
                date_cell_index = row
                report_date = dataset.iat[row, col + 1]
                print(dataset.iat[row + 1, col - 1])
                break

    # Convert the date from datetime and format it as per requirement
    formatted_report_date = report_date.date().strftime("%m/%d/%Y ")

    # Insert the date in a new column in dataframe
    df_required.insert(0, 'Date', formatted_report_date)

    # Replacing spaces and special characters  with underscores for column names
    df_required.columns = df_required.columns.str.translate({ord(c): "_" for c in " !@#$%^&*()[]{};:,./<>?\|`~-=_+"})

    output_file_name = 'output_' + report_date.date().strftime("%m_%d_%Y ")
    df_required.to_csv('output_files\\' + output_file_name, index=False)
    return df_required


def load_into_db(dataframe):
    dbname = 'report_db'
    conn = sqlite3.connect(dbname + '.sqlite')
    cur = conn.cursor()

    # Create your connection.
    # cnx = sqlite3.connect(':memory:')
    dataframe.to_sql(name='forecast_report', con=conn, if_exists='append', index=False)

    # p2 = pd.read_sql('select * from forecast_report', conn)
    # print(p2)
    #
    cur.execute('SELECT * FROM forecast_report')
    names = list(map(lambda x: x[0], cur.description))  # Returns the column names
    print(names)
    for row in cur:
        print(row)
    cur.close()


if __name__ == "__main__":
    process_files()
