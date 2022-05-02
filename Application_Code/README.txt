ERP Project

This file contains the steps to follow in order to run the code.
1. Installations
    - First, unzip the DMQL_Project.zip file
    - Next we need to install all the dependencies required to run the website
    - To avoid installing packages globally we will do all the steps in a virutal env
    - If you don't have `virtualenv` installed, then run the following command:
                        pip3 install virtualenv

    - Now, we will create and activate our environment and name the environment as `dmql2` as follows:
                        virtualenv -p python3 dmql2

                        For Mac users:
                        source dmql2/bin/activate

                        For Windows users:
                        dmql2\Scripts\activate
                        
    - After activating the environment, we will install all the packages required.
    - Make sure you are in `DMQL_Project` directory to run the command. This directory contains the file `requirements.txt` which holds all the packages list
                        pip3 install -r requirements.txt

2. Create the DATABASE, keep the name as `DMQL_Project`.

3. Next, run the `create.sql` file located in SQL_Files directory in pgAdmin. This will create the whole database schema. Next, we need to load the data in the database.

4. Before loading, we would need to configure the database parameters such as HOST, DATABASE, USER, and PASSWORD based on the setting on your system. Example below, 
HOST = "localhost"
DATABASE = "DMQL_Project"
USER = "postgres"
PASSWORD = "<Your-Password>"

Perform this step in both `config.py` (located in ERP_Sysmtem directory) and `load.py` (located in Python_Files directory)

5. Run the `load.py` file to load the data using the command while being in the Python_Files directory:
                        python3 load.py

6. Run the web app
    - To run the web app, make sure you are in the `DMQL_Project` directory.
    - Enter the below command in your terminal/command prompt (cmd) as follows:
                        streamlit run app.py

    - This will start the server and automatically open the page in the browswer or you may have to copy the link from the terminal/cmd and paste and go in our browswer to run the web app.

Note:
    - Based on the python and pip version installed on your machine, you may need to try the above commands using `python` or `python3` and `pip` or `pip3`.
