<h5>The purpose of this project is to download new files from given website in every 24 hours and extract, process the data from downloaded file to load into another output file</h5>
Python version: 3.9
<h3>Guide to run this project:</h3>

1. Install required packages listed in requirements.txt
   <br>run "pip install -r requirements.txt"
2. Python version 3.9
3. Execute 'job_scheduler.py' script<br>
   run "python job_scheduler.py"

   This will run the sub processes from 'scrapper.py' and 'processor.py' to create required folders, download new files from the website, extract data from files, and finally load into a new csv file
4. Find the 'output_files' folder to find processed data
5. This all process will be executed after every 24 hours

<h3>Guide to retrieve processed data using API:</h3>

1. Execute 'api.py' script <br>
   run "python api.py"

2. Open any web browser and go to http://127.0.0.1:5000/api/v1/report/<report_date>
   <br>** you must have to provide the date of the report at the end of the url that you want to retrieve. The format is "mm-dd-yyyy"

   <h4>Example url http://127.0.0.1:5000/api/v1/report/01-15-2021 </h4>
3. You can apply filter on numeric values by giving parameter name and value. it will return the rows that is greater than or equal to your value for that column. You can also apply multiple filters
   at a time
   <br><h5>Numeric columns(also parameters):</h5>
    1. TodayDayPeakMw
    2. TodayEvPeakMw
    3. YesterdayDayPeakMw
    4. YesterdayEvPeakMw
    5. PresentCapacityMw
    6. InstalledCapacityMw
    7. EvShortageForPlantProblemMw
    8. EvShortageForFuelMw
       <h4>Example url: http://127.0.0.1:5000/api/v1/report/01-15-2021?PresentCapacityMw=170 </h4>

4. You can also apply the filter on String columns by giving parameter name and value. In this case, you must have to provide threshold value for filtering string fields (Ex- threshold=80)<br>
   It will return the rows that has the matching score greater than your given threshold (thresh) by matching strings using 'fuzzywuzzy' library
   <br><h5>String columns(also parameters):</h5>
    1. NameOfThePowerStation
    2. Producer
    3. Remark
    4. Fuel
    5. InstalledCapacityUnitNoXCapacity
       <h4>Example url: http://127.0.0.1:5000/api/v1/report/01-15-2021?NameOfThePowerStation=Chattogram&threshold=60 </h4>
    
