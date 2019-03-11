# csv-report-processing-with-validation


# Readme

Program: csv-report-processing.py

# Purpose:

1. Format CSV report (specified):
- Date: MM/XX/DD to YYYY-MM-XX DD.
- Country: recode state name to country code.
- Impressions (views): stays as it is.
- CTR: recode into float and recount it as number of clicks.
2. Sort it.
3. Save it as a new CSV.

# How to use:

$ python3 csv-report-processing.py
 
Put all report files into INPUT_FILES. If dont exist, run program first time to create one.

Run program and gather all processed CSV files from 'OUTPUT_FILES' folder.

INPUT_FILES are archived in USED_FILES folder.

# Logic:

1. Setup:
- Specify directories, if don't exists: create.
- Get states-to-country-codes data:
- Create example input CSV files (demo, testing)
- Propose other testing possibilities.
- Load CSV(s) as dataframe(s)
- CSV Validation
2. Process repport:
- Get input CSV from INPUT_FILES_DIR as dataframe.
- Create a new dataframe.
- Recoding date: MM/XX/DD to YYYY-MM-XX DD format.
- Recode state name into the country code.	
- Clean CTR - if it happens to be in string format.
- Sort rows lexicographically by date followed by the country code.
3. Handle files.
- Move input file to USED_FILES
- Save output file (dataframe as a CSV) in OUTPUT_FILES_DIR 

# Example output:

#### Turns this:

0   01/21/2019   Mandiana                    883          0.38%

1   01/21/2019       Lola                     76          0.78%

2   01/21/2019     Fāryāb                    919          0.67%

3   01/22/2019       Lola                     34          0.82%

4   01/22/2019     Beroun                    139          0.61%

5   01/22/2019   Mandiana                   1050          0.93%

6   01/23/2019         🐱                     777          0.22%

7   01/23/2019     Gaoual                     72           0.7%

8   01/23/2019       Lola                    521          0.19%

9   01/24/2019     Beroun                    620           0.1%

10  01/24/2019    Unknown                    586          0.86%

11  01/24/2019         🐱                    1082          0.68% 


#### ...into this:

2   2019-01-21           AF          919       6

0   2019-01-21           GN          883       3

1   2019-01-21           GN           76       1

4   2019-01-22           CZ          139       1

3   2019-01-22           GN           34       0

5   2019-01-22           GN         1050      10

7   2019-01-23           GN           72       1

8   2019-01-23           GN          521       1

6   2019-01-23          XXX          777       2

9   2019-01-24           CZ          620       1

10  2019-01-24          XXX          586       5

11  2019-01-24          XXX         1082       7 
