Raymond Heinzelman
CS 457
Wed oct 20, 2021

1. Overview
2. Design
3. How to run

1. This program is a work in progress database management system. It can create databases that contain tables, which in turn contain rows and columns of whatever kind of data the user would like to store. 

2. How multiple databases are organized:
	Each database is represented as a folder with the same name of the database. Using a database simply involves using the 'chdir' command to change the working directory to the database folder. Inside the database are tables stored as .txt files with the same name. When switching between databases, the program will run a try block to perform a 'chdir' command inside the current working directory, and if that doesn't work, then it will try it again in the parent directory. 
	
How multiple tables are managed
	Tables are represented as .txt files with the same name as the table. Inside, the first line contains the metadata, i.e. the attributes of the table. Subsequent lines are then reserved for the actual table data and tuples. Python functions can accept a varying number of inputs, so the createTable() function definition has the *argv parameter to accept larger inputs (more attributes) in the future.
	
Assignment 1 functionality:

To implement the required funcitonality, I created a set functions to perform actions like:
- creating a database (creating a folder),
- creating a table (creating a txt file),
- using a database (chdir into db folder),
- alter table (write new data to .txt file ), etc

Then later in the program I used the prompt_toolkit library to make accepting user input easier. It is then run through a simple parser, and tested against if statements to then call the corresponding function. In the future I will probably need to modify how the program takes in strings like varchar(20), because the parenthesis may be important down the line. I would also like to learn how to properly use python modules to make my code more modular, as I learned python just for this assignment.

Assignment 2 functionality: 

For this assignment I completely revamped my user_input parser. It now takes multi line input by using a nested loop inside the main user_input loop. This checks for completeness by looking for a terminating character (in this case a semicolon), and if it is not present, then it will continue to take the next line as if it were still being typed on the previous. 

Another thing I've added is a header file, which is to seperate all the user_input function calls from their definition, just to clean things up. Along with this, I've created a file called virtualiztion which serves as a sort of pseudoclass. It's main function is to create a virtual table within the program using the data from the table file. It then is able to modify the data, and save it back to disk when done. I think this is useful because if any bugs happen, then you're not going to mess up the file on disk, but just the virtual one. 

 - tuple insertion: to insert a tuple into a table, the corresponding file is opened, and the data is appended to the end of the file on a new line. Formatting for various edge cases is handled. Fairly straightforward. 
 - deletion: a virtual table (vtable) is created, and modified by the program. The program will determine what columns it needs to be looking inside for the where condition. Once it has figured out the needed column, it iterates through each row, testing the where column, and if it satisfies the condition, it will delete the row. Currently the program only supports equal to and greater than, but will handle more as needed in future assignments. This will be straightforward, because of how modular the vtable process is. 
 - tuple modification: this is very similar to row deletion. The program will note the column it needs to look for to compare the where value, and will note the column that contains the value needing to be modified. Then it will iterate through the rows, testing if the whereColumn meets the whereValue, and changes the appropriate value. 
 - selection query: This was tricky, and a simpler implementation might be warranted in the future. For this process, a two vtables are created, the main vtable, and the temp vtable. The program will find the rows that meed the condition of the query, and add them to the temp vtable. Afterwards, the main vtable has its data cleared, and is then written back onto by the temp vtable, but only with the columns specified in the query. This is convoluted, but it works for now. 

Assignment 3 functionality:

Joins are implemented by again virtualizing the two given tables, and creating a third empty virtual table for the appropriate rows to be added to. 

Inner Join: Parse the input, and create two vTables for each other the tables we will be joining. Append the combined metadata of both the tables, and then go through each of the rows using a nested loop and if they meet the conditions given in the query, add them to the empty vTable. Once the loops exit, print the new vTable with all its appends. 

Outer Left Join: Similar to inner join, but this time have a seperate loop that adds every row of the left table, and then goes through each row of the second table, testing the conditions, and appending them to the appropriate row of the new vTable. 

 3. How to Run
 
 For the program to work these files need to be in a the same directory:
 PA2.py
 header.py
 virtualize.py

 in your console, type python3 PA3.py, afterwards you will be presented with '>' on your console.
 From here you can type in your commands. For the grader, I'm unsure of how to input the test.sql file as input using '<<' in the command line. It may not work due to how my user input is taken. However, I'm confident that the program works with every command in the test.sql file if they are typed in individually.

 NOTE: with how my parser currently works, exiting must be done with 'exit;', 'stop;', or 'quit;' because of the terminating character. Also, piping in a sql file does not work due to how my user input works, which is why I have included a video demonstration of myself performing the commands instructed in the PA3_test.sql file. 
