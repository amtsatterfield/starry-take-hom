# starry-take-home
Contains scripts for the starry internet take home exercise

## Installation
This script was written using Python version 3.9.12. A virtual environment is recommended for running these this script, however, these scripts use Python's standard libraries (sqlite3, pandas, os, sys). Anaconda is recommended for creating your environment.

To set up your virtual environment:
1. Clone this repo locally
2. Open your anaconda prompt
3. Change the directory to the Scripts folder of this repo: <br/><br/> ~~~ cd (your parent directory path)\take-home-assignment\scripts ~~~
5. Type the following:  <br/><br/> ~~~ conda env create --name starry --file requirements.txt ~~~

## Run the load_data script
1. Open your anaconda prompt
2. Activate the environment you created in the Installation section: <br/><br/> ~~~ activate starry ~~~
3. Change your directory to the scripts folder of this repo (see earlier steps)
4. Execute the script in your anaconda prompt:  <br/><br/> ~~~ python load_data.py ~~~
### Results
The script should return a total row count. You should see a starry.db under the scripts folder.
