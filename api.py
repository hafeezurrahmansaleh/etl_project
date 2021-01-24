import json
import os
import pathlib
import datetime

import pandas as pd
import flask
from flask import request, jsonify
from fuzzywuzzy import fuzz

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/api/v1/report/<report_date>', methods=['GET'])
def api_filter(report_date):
    date_time_obj = datetime.datetime.strptime(report_date, '%m-%d-%Y')
    print(date_time_obj)
    file_name = 'output_' + date_time_obj.date().strftime("%m_%d_%Y ") + '.csv'

    current_dir = pathlib.Path(__file__).parent
    output_dir = os.path.join(current_dir, 'output_files\\')

    file = os.path.join(output_dir, file_name)
    report_df = pd.read_csv(file)

    query_parameters = request.args
    EvShortageForFuelMw = query_parameters.get("EvShortageForFuelMw")
    EvShortageForPlantProblemMw = query_parameters.get("EvShortageForPlantProblemMw")
    Fuel = query_parameters.get("Fuel")
    InstalledCapacityMw = query_parameters.get("InstalledCapacityMw")
    InstalledCapacityUnitNoXCapacity = query_parameters.get("InstalledCapacityUnitNoXCapacity")
    NameOfThePowerStation = query_parameters.get("NameOfThePowerStation")
    PresentCapacityMw = query_parameters.get("PresentCapacityMw")
    ProbableStartUpDate = query_parameters.get("ProbableStartUpDate")
    Producer = query_parameters.get("Producer")
    Remark = query_parameters.get("Remark")
    TodayDayPeakMw = query_parameters.get("TodayDayPeakMw")
    TodayEvPeakMw = query_parameters.get("TodayEvPeakMw")
    YesterdayDayPeakMw = query_parameters.get("YesterdayDayPeakMw")
    YesterdayEvPeakMw = query_parameters.get('YesterdayEvPeakMw')
    threshold = query_parameters.get('threshold')

    """Numeric columns filter"""
    if EvShortageForFuelMw:
        report_df = report_df[(report_df['EvShortageForFuelMw'].fillna(0).astype(int) >= int(EvShortageForFuelMw))]
    if EvShortageForPlantProblemMw:
        report_df = report_df[(report_df['EvShortageForPlantProblemMw'].fillna(0).astype(int) >= int(EvShortageForPlantProblemMw))]
    if InstalledCapacityMw:
        report_df = report_df[(report_df['InstalledCapacityMw'].fillna(0).astype(int) >= int(InstalledCapacityMw))]
    if PresentCapacityMw:
        report_df = report_df[(report_df['PresentCapacityMw'].fillna(0).astype(int) >= int(PresentCapacityMw))]
    if TodayDayPeakMw:
        report_df = report_df[(report_df['TodayDayPeakMw'].fillna(0).astype(int) >= int(TodayDayPeakMw))]
    if TodayEvPeakMw:
        report_df = report_df[(report_df['TodayEvPeakMw'].fillna(0).astype(int) >= int(TodayEvPeakMw))]
    if YesterdayDayPeakMw:
        report_df = report_df[(report_df['YesterdayDayPeakMw'].fillna(0).astype(int) >= int(YesterdayDayPeakMw))]
    if YesterdayEvPeakMw:
        report_df = report_df[(report_df['YesterdayEvPeakMw'].fillna(0).astype(int) >= int(YesterdayEvPeakMw))]

    """String columns filter"""
    if not threshold and (Producer or Remark or Fuel or InstalledCapacityUnitNoXCapacity):
        JSONP_data = [
            {
                "Status":  "Failed to get data",
                "message": 'You must have to provide threshold value for filtering string fields (Ex- threshold=80)',

            },
        ]
        return jsonify(JSONP_data)
    else:
        report_df[['NameOfThePowerStation', 'Producer', 'Remark', 'Fuel', 'InstalledCapacityUnitNoXCapacity']] = report_df[
            ['NameOfThePowerStation', 'Producer', 'Remark', 'Fuel',
             'InstalledCapacityUnitNoXCapacity']].fillna(value='')
        if NameOfThePowerStation:
            report_df = report_df[
                report_df.apply(lambda row: fuzz.ratio(row['NameOfThePowerStation'], NameOfThePowerStation), axis=1) > int(threshold)
                ]
        if Producer:
            report_df = report_df[report_df.apply(lambda row: fuzz.ratio(row['Producer'], Producer), axis=1) > int(threshold)]
        if Remark:
            report_df = report_df[report_df.apply(lambda row: fuzz.ratio(row['Remark'], Remark), axis=1) > int(threshold)]
        if Fuel:
            report_df = report_df[report_df.apply(lambda row: fuzz.ratio(row['Fuel'], Fuel), axis=1) > int(threshold)]
        if InstalledCapacityUnitNoXCapacity:
            report_df = report_df[
                report_df.apply(lambda row: fuzz.token_sort_ratio(row['InstalledCapacityUnitNoXCapacity'], InstalledCapacityUnitNoXCapacity),
                    axis=1) > int(threshold)
                ]

    # df_list = report_df.values.tolist()
    JSONP_data = jsonify(json.loads(report_df.to_json(orient='records')))  #
    return JSONP_data


app.run()
