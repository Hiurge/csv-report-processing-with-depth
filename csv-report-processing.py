import pandas as pd 
import os
import shutil
import pycountry
import time



# 1. Specify directories:
# -----------------------
INPUT_FILES_DIR = 'INPUT_FILES'
USED_FILES_DIR = 'USED_FILES'
OUTPUT_FILES_DIR = 'OUTPUT_FILES'

# 2. Set up errors log:
# ---------------------
ERRORS = []
CRITICAL_ERRORS = []

# If don't exists: create.
try:
	os.mkdir(INPUT_FILES_DIR)
	print("Directory " , INPUT_FILES_DIR ,  " Created.") 
except FileExistsError:
	pass

try:
	os.mkdir(USED_FILES_DIR)
	print("Directory " , USED_FILES_DIR ,  " Created.") 
except FileExistsError:
	pass

try:
	os.mkdir(OUTPUT_FILES_DIR)
	print("Directory " , OUTPUT_FILES_DIR ,  " Created.")
except FileExistsError:
	pass


# 2. Get states-to-country-codes data:
# ---------------------------------
states_data = list(pycountry.subdivisions)
STATE_CODES = {state.name : state.country_code for state in states_data}


# 3. Create example input CSV files (demo, testing)
# ----------------------------------------------

example_cols = ['date', 'state name', 'number of impressions', 'CTR percentage']

example_data = [['01/21/2019', 'Mandiana',  883,  '0.38%'],
				['01/21/2019', 'Lola',       76,  '0.78%'],
				['01/21/2019', 'Fāryāb',    919,  '0.67%'],
				['01/22/2019', 'Lola',       34,  '0.82%'],
				['01/22/2019', 'Beroun',    139,  '0.61%'],
				['01/22/2019', 'Mandiana', 1050,  '0.93%'],
				['01/23/2019', ' 🐱 ',      777,  '0.22%'],
				['01/23/2019', 'Gaoual',     72,  '0.7%' ],
				['01/23/2019', 'Lola',      521,  '0.19%'],
				['01/24/2019', 'Beroun',    620,  '0.1%' ],
				['01/24/2019', 'Unknown',   586,  '0.86%'],
				['01/24/2019', ' 🐱 ',     1082,  '0.68%']]


# 4. Propose other testing possibilities.
# ---------------------------------------
# Assumptions:
# 1. Example data is just an example
# 2. Therefore some data could apper in different datatype than specified
#    however not as a mistake but because of a different format:
# 	 a) date could be string but could be a datestamp
#    b) CTR percentage could be string as well as a float 
# 3. It also sound healty to assume colum names are rather exaplatory
# 4. ... as well as colum order may or may not be hold in input data
# 5. However, column contents should remain consistent

test_data_1 = [ ['2343424432',  444,        883,   0.38  ],
				['01/21/2019', 'Lola',       76,  '0.78%'],
				['01/21/2019', 'Fāryāb',    919,  '0.67%'],
				['01/22/2019', 'Lola',      201,  '0.82%'],
				['01/22/2019', 'Beroun',    139,  '0.61%'],
				['01/22/2019', 'Mandiana', 1050,  '0.93%'],
				['01/23/2019', ' 🐱 ',      777,  '0.22%'],
				['01/23/2019', 'Gaoual',     72,  '0.7%' ],
				['01/23/2019', 'Lola',      521,  '0.19%'],
				['01/24/2019', 'Beroun',    620,  '0.1%' ],
				['01/24/2019', 'Unknown',   586,  '0.86%'],
				['01/24/2019', ' 🐱 ',     1082,  '0.68%']]

test_data_2 = [ [ 444,      '883',    0.38  , '2343424432'],
				['Lola',       76,   '0.78%', '01/21/2019'],
				['Fāryāb',    919,   '0.67%', '01/21/2019'],
				['Lola',      201,   '0.82%', '01/22/2019'],
				['Beroun',    139,   '0.61%', '01/22/2019'],
				['Mandiana', 1050,   '0.93%', '01/22/2019'],
				[' 🐱 ',      777,   '0.22%', '01/23/2019'],
				['Gaoual',     72,   '0.7%' , '01/23/2019'],
				['Lola',      521,   '0.19%', '01/23/2019'],
				['Beroun',    620,   '0.1%' , '01/24/2019'],
				['Unknown',   586,   '0.86%', '01/24/2019'],
				[' 🐱 ',     1082,   '0.68%', '01/24/2019']]

test_data_3 = [ [ 444,      '883',    0.38  , '2343424432'],
				['Lola',        0,   '0.78%', 'abcdefghij'],
				['Fāryāb',  0.919,   '0.67%', '01-21-2019'],
				['Lola',      201,        '', '01/22-2019'],
				['Beroun',   True,   '0.61%', '01/22/2019'],
				['Mandiana', True,   '0.93%', '01/22/2019'],
				[' 🐱 ',     True,   '0.22%', '01/23/2019'],
				['',         True,   '0.7%' , '01/23/2019'],
				['Lola',      521,   '0.19%', '01/23/2019'],
				['Beroun',  620.4,   '0.1%' , '01/24/2019'],
				['Unknown',   586,   '0.86%', '01/24/2019'],
				[' 🐱 ',     1082,   '0.68%', '01/24/2019']]


# 5. Save testing tables to INPUT_FILES_DIR
# --------------------------------------
# This program is validated for example_data only, hence: testing_tables[:1].
for i, table in enumerate([test_data_1, example_data]): #,, test_data_2, test_data_3]
	save_path = os.path.join(INPUT_FILES_DIR, 'example_input_{}.csv'.format(i))
	example_df = pd.DataFrame(table, columns=example_cols) #; print(df)
	example_df.to_csv(save_path, sep=',', index=False)


# Load CSV(s) as dataframe(s).
# -------------------------------
# Assumptions:
# 1. All such CSV files to be processed are gathered in a specific folder INPUT_FILES_DIR
# 2. Each file, after being used (with no error) should be moved to archive USED_FILES_DIR
# 3. New (our) CSV file is saved to the OUTPUT_FILES_DIR
# 4. Folder may contain one or more CSV files


# 6. Validations.
# ---------------
def validate_CSV(df, csv_file):

	print('Validating {} file.\n'.format(csv_file))
	
	for i, date in enumerate(df.iloc[:,0]):
		assert isinstance(date, str), 'Column 0, row %r: date is not of a string type. Checking all data is sugested.' % i
		assert date[2] == '/' and date[5] == '/', 'Column 0, row %r: date in wrong format ("MM/DD/YYYY" format required). Checking all data is sugested.' % i
		assert len(date) == 10, 'Column 0, row %r: date in wrong format ("MM/DD/YYYY" format required). Checking all data is sugested.' % i

	for i, state in enumerate((df.iloc[:,1])):
		assert isinstance(state, str), 'Column 1, row %r: state is not of a string type. Checking all data is sugested.' % i
		if not state in STATE_CODES:
			print('Column 1, row {}: state is outside of our states base. Checking all data is sugested.'.format(i))

	for i, impression in enumerate((df.iloc[:,2])):
		assert isinstance(impression, int), 'Column 2, row %r: impression is not of a integer type. Checking all data is sugested.' % i

	for i, CTR in enumerate((df.iloc[:,3])):
		assert isinstance(CTR, (str, float)), 'Column 3, row %r: CTR is not of a float or a str type (float "0.03" or string format "0.03%" is required). Checking all data is sugested.' % i
		if isinstance(CTR, str):
			assert CTR[-1:] == '%' or isinstance(int(CTR[:-1]), int), 'Column 3, row %r: CTR in wrong format (float "0.03" or string format "0.03%" is required). Checking all data is sugested.' % i
			assert CTR.count('.') <= 1,  'Column 3, row %r: CTR in wrong format (float "0.03" or string format "0.03%" is required). Checking all data is sugested.' % i
			for char in CTR[:-1]:
				if char != '.':
					assert isinstance(int(char), int) , 'Column 3, row %r: CTR in wrong format (float "0.03" or string format "0.03%" is required). Checking all data is sugested.' % i
			
	print('File is valid. Starting processing.\n')

# 7. Recoding date: MM/XX/DD to YYYY-MM-XX DD format.
# ---------------------------------------------------
def date_recode(date):

	# try:
	# 	date = str(date)
	# 	date = date
	# 	break
	# except ValueError:
	# 	print("No valid integer! Please try again ...")
	MM, DD, YYYY = str(date).split('/')
	return '-'.join([YYYY, MM, DD])


# 8. Recode state name into the country code.	 
# -------------------------------------------
def state_name_to_country_code(state):
	if state in STATE_CODES.keys():
		return STATE_CODES[state]
	else:
		return 'XXX'


# 9. leal CTR - if it happens to be in string format.
# ---------------------------------------------------
def clean_CTR(CTR):
	if '%' in CTR:
		CTR = CTR[:-1]
	return float(CTR) / 100


# 10. Process repport using the above functions.
# ----------------------------------------------
def report_processing(df, new_df):
	new_df['date'] = df.iloc[:,0].apply(date_recode)
	new_df['country code'] = df.iloc[:,1].apply(state_name_to_country_code)
	new_df['impressions'] = df.iloc[:,2]
	new_df['clicks'] = df.iloc[:,3].apply(clean_CTR)
	new_df['clicks'] = new_df['clicks'] * new_df['impressions']
	new_df['clicks'] = new_df['clicks'].round(0).astype(int)
	return new_df


# 11. Handle files.
# -----------------
def move_input_file(csv_file):
	fp = os.path.join(INPUT_FILES_DIR, csv_file)
	if not os.path.isfile(fp):
		shutil.move(fp, USED_FILES_DIR)
	else:
		fp2 = ''.join([fp[:-4],'_COPY_',time.strftime("%H%M%S"),'.csv'])
		os.rename(fp, fp2)
		shutil.move(fp2, USED_FILES_DIR)


# MAIN LOGIC.
# -----------
def run_csv_report_processing():

	NEW_COLUMNS = ['date', 'country code', 'impressions', 'clicks']

	# LOGIC:
	for i, csv_file in enumerate(os.listdir(INPUT_FILES_DIR)):
		
		# File name
		print('\nProcessing file: {}\n'.format(csv_file))

		# Mesure timings:
		start_time = time.time()

		# Get input CSV from INPUT_FILES_DIR as dataframe
		df = pd.read_csv(os.path.join(INPUT_FILES_DIR, csv_file), sep=',')
		
		# Inspect:
		print('\nInspect:', df.head(15), '\n')
		
		# Validate CSV:
		validate_CSV(df, csv_file)

		# Create a new dataframe
		new_df = pd.DataFrame([], columns=NEW_COLUMNS)

		# Processing data
		new_df = report_processing(df, new_df)

		# Rows sorted lexicographically by date followed by the country code
		new_df.sort_values(['date', 'country code'], ascending=[True, True], inplace=True)

		# Inspect:
		print('\nInspect:', new_df.head(15), '\n')

		# New CSV path
		save_path = '{}/{}_processed.csv'.format(OUTPUT_FILES_DIR, csv_file[:-4])

		# Save dataframe as CSV in OUTPUT_FILES_DIR 
		new_df.to_csv(save_path, sep=',', index=False, encoding='utf-8')

		# Move input file to USED_FILES_DIR
		move_input_file(csv_file)

		# Mini-report:
		timing = round((time.time()-start_time), 2)
		print('\nFile {} done, saved to {}'.format((i+1), save_path))
		print('Processing took: {} seconds.\n'.format(timing))


# RUN.
# ----
if __name__ == "__main__":
	run_csv_report_processing()



# Readme
# ------

# Program: csv-report-processing.py
# ---------------------------------

# Purpose:
# --------
# 1. Format CSV report (specified):
# - Date: MM/XX/DD to YYYY-MM-XX DD.
# - Country: recode state name to country code.
# - Impressions (views): stays as it is.
# - CTR: recode into float and recount it as number of clicks.
# 2. Sort it.
# 3. Save it as a new CSV.

# How to use:
# -----------
# $ python3 csv-report-processing.py
# 
# Put all report files into INPUT_FILES. If dont exist, run program first time to create one.
# Run program and gather all processed CSV files from 'OUTPUT_FILES' folder.
# INPUT_FILES are archived in USED_FILES folder.

# Logic:
# ------
# 1. Setup:
# - Specify directories, if don't exists: create.
# - Get states-to-country-codes data:
# - Create example input CSV files (demo, testing)
# - Propose other testing possibilities.
# - Load CSV(s) as dataframe(s)
# 2. Process repport:
# - Get input CSV from INPUT_FILES_DIR as dataframe.
# - Create a new dataframe.
# - Recoding date: MM/XX/DD to YYYY-MM-XX DD format.
# - Recode state name into the country code.	
# - Clean CTR - if it happens to be in string format.
# - Sort rows lexicographically by date followed by the country code.
# 3. Handle files.
# - Move input file to USED_FILES
# - Save output file (dataframe as a CSV) in OUTPUT_FILES_DIR 

# Example output:
# ---------------
# ~/csv-report-processing$ python3 csv-report-processing.py

# Processing file: example_input_1.csv


# Inspect:           date state name  number of impressions CTR percentage
# 0   01/21/2019   Mandiana                    883          0.38%
# 1   01/21/2019       Lola                     76          0.78%
# 2   01/21/2019     Fāryāb                    919          0.67%
# 3   01/22/2019       Lola                     34          0.82%
# 4   01/22/2019     Beroun                    139          0.61%
# 5   01/22/2019   Mandiana                   1050          0.93%
# 6   01/23/2019         🐱                     777          0.22%
# 7   01/23/2019     Gaoual                     72           0.7%
# 8   01/23/2019       Lola                    521          0.19%
# 9   01/24/2019     Beroun                    620           0.1%
# 10  01/24/2019    Unknown                    586          0.86%
# 11  01/24/2019         🐱                    1082          0.68% 

# Validating example_input_1.csv file.

# Column 1, row 6: state is outside of our states base. Checking all data is sugested.
# Column 1, row 10: state is outside of our states base. Checking all data is sugested.
# Column 1, row 11: state is outside of our states base. Checking all data is sugested.
# File is valid. Starting processing.


# Inspect:           date country code  impressions  clicks
# 2   2019-01-21           AF          919       6
# 0   2019-01-21           GN          883       3
# 1   2019-01-21           GN           76       1
# 4   2019-01-22           CZ          139       1
# 3   2019-01-22           GN           34       0
# 5   2019-01-22           GN         1050      10
# 7   2019-01-23           GN           72       1
# 8   2019-01-23           GN          521       1
# 6   2019-01-23          XXX          777       2
# 9   2019-01-24           CZ          620       1
# 10  2019-01-24          XXX          586       5
# 11  2019-01-24          XXX         1082       7 


# File 1 done, saved to OUTPUT_FILES/example_input_1_processed.csv
# Processing took: 0.03 seconds.


# Processing file: example_input_0.csv


# Inspect:           date state name  number of impressions CTR percentage
# 0   2343424432        444                    883           0.38
# 1   01/21/2019       Lola                     76          0.78%
# 2   01/21/2019     Fāryāb                    919          0.67%
# 3   01/22/2019       Lola                    201          0.82%
# 4   01/22/2019     Beroun                    139          0.61%
# 5   01/22/2019   Mandiana                   1050          0.93%
# 6   01/23/2019         🐱                     777          0.22%
# 7   01/23/2019     Gaoual                     72           0.7%
# 8   01/23/2019       Lola                    521          0.19%
# 9   01/24/2019     Beroun                    620           0.1%
# 10  01/24/2019    Unknown                    586          0.86%
# 11  01/24/2019         🐱                    1082          0.68% 

# Validating example_input_0.csv file.

# Traceback (most recent call last):
#   File "csv-report-processing.py", line 274, in <module>
#     run_csv_report_processing()
#   File "csv-report-processing.py", line 242, in run_csv_report_processing
#     validate_CSV(df, csv_file)
#   File "csv-report-processing.py", line 143, in validate_CSV
#     assert date[2] == '/' and date[5] == '/', 'Column 0, row %r: date in wrong format ("MM/DD/YYYY" format required). Checking all data is sugested.' % i
# AssertionError: Column 0, row 0: date in wrong format ("MM/DD/YYYY" format required). Checking all data is sugested.
