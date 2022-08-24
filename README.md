# sqlalchemy-challenge
## GA Tech Data Science and Analytics Module 10

This module utilizes a mix of tools such as Python, SQLAlchemy, Pandas, Matplotlib, and Flask to perform a basic analysis and data exploration of a provided SQLite database.

### Description: Part 1: Climate Analysis and Exploration

<b>Precipitation Analysis</b>
<p>For this part, we analyze the precipitation data of the previous 12 months.</p>
<img src="Images/SummaryStatistics.png">

<p>We then plot the data onto a graph:</p>
<img src="Images/PreciptationByDateInPreviousYear.png">

<p>Based on the graph, we can see that the months of August, February, and May appear to see the most rainfall.</p>

<b>Station Analysis</b>
<p>For this part, we analyze the station table by identifying the station with the most activity. To do this, we calculate the total number of rows in the dataset for a given station.</p>

<p>We find that station USC00519281 is the most active station.</p>

<p>Then we calculate the lowest, highest, and average temperatures of the most active station. We find that the lowest temperature is 54.0, the highest temperature is 85.0, and the average temperature is 71.66.</p>

<p>As we continue to analyze the data for the most active station, we identify the temperatures for the previous year and plot this onto a histogram to display the frequency of a given temperature.</p>

<img src="Images/TemperatureFrequencyOfMostActiveStation.png">

<p>Based on the histogram, we can conclude that the distribution of temperatures fall around 75.</p>

### Description: Part 2: Design Your Climate App
<p>For this part, we use Flask to create API calls for the data that we created queries for in Part 1.</p>

<p>Here are the available routes that we needed to create:</p>
* /api/v1.0/precipitation
* /api/v1.0/stations
* /api/v1.0/tobs
* /api/v1.0/[start: yyyy-mm-dd]
* /api/v1.0/[start: yyyy-mm-dd]/[end: yyyy-mm-dd]

<p>The precipitation route lists the dates and precipitation of all results in the database as a dictionary.</p>

<p>The stations route lists the stations from the station table.</p>

<p>The tobs route lists the temperatures of the previous year from the latest year in the dataset.</p>

<p>The start route is a dynamic API that will calculate the temperature min, max, and avg of all results starting from the given date to the end date in the dataset. This route assumes that the input will be in yyyy-mm-dd format.</p>

<p>The start/end route is a dynamic API that will calculate the temperature min, max, and avg of all results starting from the given date to the given end date. This route assumes that the input will be in yyyy-mm-dd format.</p>

<p>The current code will only verify if the end date is after the start date. It will not validate if the date exists in the dataset.</p>

### Submission Requirements:
* Initial data resources provided for module
* Flask app.py file
* Jupyter Notebook with analysis

<p>Though two bonuses are provided as an option to complete, they were not completed at time of module submission.</p>