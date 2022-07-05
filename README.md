# ERP System Management

ERPs ideally involve complex databases that are carefully managed by a host of database operators or admins. We need to use database systems, because if we use Excel files to maintain the data, then the amount of time needed to make updates to the different related tables will be really complicated and would consume a lot of man-hours, which is expensive. If the number of tables/files is large, then the cost of maintaining the excel files will be prohibitive. This is excluding human error because human maintenance is not the perfect way to deal with large amounts of data. A simple “0” error would cause massive disruptions in the operations and would take a lot of time to correct, which would again mean deploying excess resources for mitigating such issues. A database management system would be a perfect system to maintain an ERP. By defining relations, we would be enforcing integrity and reducing the number of errors present in the data. This is apart from the efficiency gains in CRUD operations, which would lead to a drastic improvement in resource planning and a reduction in cost for mitigating issues.

## Target User
- **The User**: Anyone who needs to manage the resources in their organization, such as orders, inventory, supplier information, etc. would be a user.
- **The Administer**: Anyone who needs to do control checks (such as supplier and purchaser is not the same person), or maintain the database characteristics (Integrity, tables, backups, etc) would be an administrator.
- **Real-life scenario description**: Our goal is to simulate a simple system for entering data into an ERP and allow users to do basic querying.

## Run the Project
This file contains the steps to follow in order to run the code.
1. **Installations**
    - First, unzip the DMQL_Project.zip file
    - Next we need to install all the dependencies required to run the website
    - To avoid installing packages globally we will do all the steps in a virutal env
    - If you don't have `virtualenv` installed, then run the following command:
                        pip3 install virtualenv

    - Now, we will create and activate our environment and name the environment as `dmql2` as follows:
    
      `virtualenv -p python3 dmql2`

      For Mac users:
      `source dmql2/bin/activate`

      For Windows users:
      `dmql2\Scripts\activate`
                        
    - After activating the environment, we will install all the packages required.
    - Make sure you are in `DMQL_Project` directory to run the command. This directory contains the file `requirements.txt` which holds all the packages list
                        pip3 install -r requirements.txt

2. **Create the DATABASE**, keep the name as `DMQL_Project`.

3. Next, run the `create.sql` file located in SQL_Files directory in pgAdmin. This will create the whole database schema. Next, we need to load the data in the database.

4. Before loading, we would need to configure the database parameters such as HOST, DATABASE, USER, and PASSWORD based on the setting on your system. Example below, <br>
`HOST = "localhost"`<br>
`DATABASE = "DMQL_Project"`<br>
`USER = "postgres"`<br>
`PASSWORD = "<Your-Password>"`<br>

Perform this step in both `config.py` (located in ERP_Sysmtem directory) and `load.py` (located in Python_Files directory)

5. **Run** the `load.py` file to load the data using the command while being in the Python_Files directory:
                        python3 load.py

6. **Run the web app**
    - To run the web app, make sure you are in the `DMQL_Project` directory.
    - Enter the below command in your terminal/command prompt (cmd) as follows:
                        streamlit run app.py

    - This will start the server and automatically open the page in the browswer or you may have to copy the link from the terminal/cmd and paste and go in our browswer to run the web app.

Note:
    - Based on the python and pip version installed on your machine, you may need to try the above commands using `python` or `python3` and `pip` or `pip3`.

## ERP Diagram of our system:
![ER_Diagram_DMQL](https://user-images.githubusercontent.com/24275587/177432290-19e00b4f-bf84-4805-9aa7-4e8649227654.png)

## Sample Screenshots of our web-app:
1. **Home Page**
This page is responsible for displaying each table and an option to perform insert, update, and delete for that respective table. User can navigate different tables using the drop down in the app navigation panel to view different tables. We have also implemented pagination feature for huge tables. To view each table and perform DML commands we have handled different SQL commands in the backend.
<img width="1391" alt="Home_insert_new" src="https://user-images.githubusercontent.com/24275587/177432865-0df8fb9f-8149-4270-a7ff-4c0fa8b1d501.png">

2. **Filter Table Page**
This page provides a lot of flexibility to the user to slice through different tables based on different filters. In simple terms, user can play with SELECT statement in SQL using the UI components. Again, here the user has the freedom to choose table, choice of attribute to view and apply different algebraic, boolean, logical, and operators like BETWEEN, LIKE. Based on the filter values and attributes the appropriate SQL command is executed to fetch the results from the database.
<img width="569" alt="Filter_table_new" src="https://user-images.githubusercontent.com/24275587/177432902-1040b95d-e955-4992-8b60-fe6418783f14.png">

3. **Advanced Queries Page**
In this page we have defined various use cases related to our ERP system. Each use cases captures various database concepts such as joins over multiple tables, order by, group by and having operations; along with various other filtering options based on where clause. User can choose values for each filters/fields and based on those values each time a SQL query is executed in the backend and the result is displayed in the form of a table.
<img width="1386" alt="Advance_queries_new" src="https://user-images.githubusercontent.com/24275587/177432921-85df26b5-f068-426d-908a-46abc25fb499.png">

We have also performed query optimization for our system; all the metrics and query can be observed in the report (`CSE560_Milestone2_DCoderz.pdf`).

### Collaborators:
- Anup Thakkar
- Pushkaraj Joshi
- Sagar Thacker
