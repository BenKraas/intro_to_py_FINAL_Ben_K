# -*- coding: utf-8 -*-
"""
Introduction to Programming and Applied Statistics

======================
Final Project - TASK 7
======================


Use the air-quality-covid19-response data from Lecture 10
(available on moodle) to address the following subtasks:

Subtask 7.1
-----------
Create a new dataframe with the 2015-2019 daily NO2 and
O3 concetrations for Athens. Add a new column with
the season (i.e., winter, spring, summer, and autumn).

Hint: Use the Path class from the pathlib module to point to 
      the folder with air-quality-covid19-response data (see Lecture 10).


Subtask 7.2
-----------
Randomly select 7000 rows from the dataframe of subtask 7.1. Use seaborn
to create a scatterplot presenting the randomly selected NO2 and O3 values.
Your figure should also include a linear regression line.

Hint: https://seaborn.pydata.org/generated/seaborn.lmplot.html#seaborn.lmplot (See example 1)


Subtask 7.2
-----------
Randomly select 28000 rows from the dataframe of subtask 7.1. Use seaborn
to create a scatterplot presenting the randomly selected NO2 and O3 values
per season. Each subplot should also include a linear regression line.

Hint: https://seaborn.pydata.org/generated/seaborn.lmplot.html#seaborn.lmplot (See example 7)


Subtask 7.4
-----------
Use seaborn to create a figure that presents Athens' NO2 and O3 distributions
per season. The figure should include 8 subplots arranged in 2 rows and 4 columns.
Each row should include 4 histrogramms (one per season). The first row should present
the NO2 distribution and the the second the O3.

Hint: https://seaborn.pydata.org/examples/faceted_histogram.html


Subtask 7.5
-----------
Calculate the mean NO2 concentration per month and year (for Athens) and
use seaborn to plot the result as a heatmap.

Hint: https://seaborn.pydata.org/generated/seaborn.heatmap.html#seaborn.heatmap


Subtask 7.6
-----------
What format codes should be used for coverting the
following datestrings to datetime objects? 

    Datestrings                                      Format Code
-----------------------------------------------------------------------------
   24-March-2014                    |           Type your answer HERE.
   24.03.2014 15:23 CEST            |           Type your answer HERE.
   Oct 24, 2020                     |           Type your answer HERE.
   20210430                         |           Type your answer HERE.
   Sunday, September 8, 2013        |           Type your answer HERE.
   
Hint: https://strftime.org/

"""

