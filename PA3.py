'''
Raymond Heinzelman
CS457 Assignment 2
For documentation and design description, see README
'''

import fileinput

#header is our file containing all the function definitions that user_input can call, mainly done for modularity and readability purposes
import header

#os library allows us to use shell commands from python
import os

#shutil library is for high level file operations, i.e. remove folders
import shutil

#string library is for the annoyingly complex string manipulation done in the program
import string

#prompt toolkit is a library that is good for command line user interfaces
from prompt_toolkit import prompt

#sys is for error reporting
import sys

#begin user interface implementation
#-------------------------------------------------------------------------------------


# initializing punctuations string
#if any punctuation like this is found in user input, delete it for the parser
punc = '''-[]{}:'"\/?@#$%^&~'''
#if parenthesis are found, make them a space instead
punc_space = '(),'
#used later to designate terminal characters
punc_semicolon = ';'
#if our list of user input words x contains any of these words, we will concatenate it with the next element in x
punc_exceptions = ['varchar']

#user input loop
while 1:
	
	#completeInput will be set to 1 if a terminating character is the last thing input. 
	#after it's set to 1, the program will then continue to call functions based on the content of the user_input
	completeInput = 0
	#multiLineInput is used to store the previous line's input until a terminating character is input
	multiLineInput = ''

	#user_input must be terminated with a semicolon, else the program will continue accepting multiline input
	while(completeInput != 1):

		#user_input is now the last incomplete line's input plus whatever is about to be input
		user_input = multiLineInput
		user_input = user_input + ' ' + prompt('>')

		#get rid of extraneous punctuation for parser
		for punctuation in user_input:
			#if it's punctuation we don't like, delete it 
			if punctuation in punc:
				user_input = user_input.replace(punctuation,'')
			#if it's parenthesis following certain keywords, or a comma, we'll keep it 
			if punctuation in punc_space:
				user_input = user_input.replace(punctuation,' ')
			#if it's a semicolon, lets add a space before it so it becomes its own object to be parsed
			if punctuation in punc_semicolon:
				user_input = user_input.replace(punctuation, ' ;')

		#make input lowercase
		user_input = user_input.lower()

		#split user input into their keywords
		x = user_input.split()

		#punctuation exceptions that will allow the creation of variables like varchar(20) and the like 
		#iterate through every word in our user_input list x
		xLength = len(x)-2
		xIterator=0
		while(xIterator<=xLength):
			#if a word is one that needs punctation exceptions (varchar(20), etc.), then:
			if(x[xIterator] in punc_exceptions):
				#create a temp variable so we know what to delete later 
				deleteThis = x[xIterator+1]
				#create a new string that has the type AND the number inside the parenthesis 
				concatenated = x[xIterator] + '(' + str(x[xIterator+1]) + ')'
				#overwrite the ith element with the new string
				x[xIterator] = concatenated
				#delete the now extraneous number data that was inside the parenthesis
				x.remove(deleteThis)
				xLength = xLength-1
			xIterator = xIterator+1

		#if the last parsed object is not a semicolon, rerun the inner loop to take more user input, otherwise, exit and continue to function calling from user_input
		if(x[len(x)-1] != ';'):
			multiLineInput = user_input
		else:
			completeInput = 1

#begin function calls for user_input
#Here the program will take the .split() up user input and call its respective function
#-------------------------------------------------------------------------------------

	try:
		#createDB
		if(x[0] == 'create' and x[1] == 'database'):
			header.createDB(x[2])
		#dropDB
		elif(x[0] == 'drop' and x[1] == 'database'):
			header.dropDB(x[2])
		#useDB
		elif(x[0] == 'use'):
			header.useDB(x[1])

		#createTable w/ x tuples, if more need to be added they can be but for now it supports 1, 2 and 3 tuples
		elif(x[0] == 'create' and x[1] == 'table'):
			if(len(x) == 6):
				header.createTable(x[2],x[3],x[4])
			if(len(x) == 8):
				header.createTable(x[2],x[3],x[4],x[5],x[6])
			if(len(x) == 10):
				header.createTable(x[2],x[3],x[4],x[5],x[6],x[7],x[8])
			if(len(x) == 12):
				header.createTable(x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10])

		#dropTable
		elif(x[0] == 'drop' and x[1] == 'table'):
			header.dropTable(x[2])

		#selectTable
		elif(x[0] == 'select' and x[1] == '*' and x[2] == 'from' and x[4] == ';'):
			header.selectTable(x[3],x[1])

		#addToTable: adds an attribute to a table 
		elif(x[0] == 'alter' and x[1] == 'table' and x[3] == 'add'):
			header.addToTable(x[2],x[4],x[5])

		#insert into: add an entry to the table using the schema
		elif(x[0] == 'insert' and x[1] == 'into' and x[3] == 'values'):
			if(len(x) == 7):
				header.insertInto(x[2],x[4],x[5])
			if(len(x) == 8):
				header.insertInto(x[2],x[4],x[5],x[6])

		#update x, and set y1 to y2 where z1 equals z2
		#this will be handled by creating a virtual table, modifying the data within it, and then saving over the old file
		elif(x[0] == 'update' and x[2] == 'set' and x[6] == 'where'):
			header.update(x[1],x[3],x[5],x[7],x[9])

		#delete a row where attribute x = value y
		#this also utilizes a virtual table
		elif(x[0] == 'delete' and x[1] == 'from' and x[3] == 'where' and x[5] == '='):
			header.deleteEq(x[2],x[4],x[6])

		#delete a row where attribute x's value is less than y
		#again, this utilizes the virtual table pseudoclass 
		elif(x[0] == 'delete' and x[1] == 'from' and x[3] == 'where' and x[5] == '>'):
			header.deleteGT(x[2],x[4],x[6])

		#print out attributes x and y where attribute z has a certain value
		#another function utilizing vtable
		elif(x[0] == 'select' and x[3] == 'from' and x[5] == 'where' and x[7] == '!='):
			header.selectFromWhereNot(x[1],x[2],x[4],x[6],x[8])

		#inner join syntax 1
		elif(x[0] == 'select' and x[1] == '*' and x[2] == 'from' and x[7] == 'where' and x[9] == '='):
			header.join(x[3],x[4],x[5],x[6],x[8],x[10])

		#inner join syntax 2
		elif(x[0] == 'select' and x[1] == '*' and x[2] == 'from' and x[5] == 'inner' and x[6] == 'join' and x[9] == 'on' and x[11] == '='):
			header.join(x[3],x[4],x[7],x[8],x[10],x[12])

		#left outer join
		elif(x[0] == 'select' and x[1] == '*' and x[2] == 'from' and x[5] == 'left' and x[6] == 'outer' and x[7] == 'join' and x[10] == 'on' and x[12] == '='):
			header.leftOuterJoin(x[3],x[4],x[8],x[9],x[11],x[13])

		#quit
		elif(x[0] == 'quit' or x[0] == 'stop' or x[0] == 'exit'): 
			print('Program is now exiting :^)')
			break
		#error
		else:
			print('invalid input!')
	except Exception as e:
		print('An unknown error occured: %s' %e)