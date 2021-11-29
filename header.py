#virtualize is a sort of pseudoclass, but is a file. I'm not too sure how to make proper classes in python but this suffices for one for now
import virtualize

import os
import shutil
import string
import sys

#create a database named dbName if one does not already exist
def createDB(dbName):
	while True:
		try:
			os.mkdir(dbName)
			print('Database named %s was created' %dbName)
			break
		except:	
			print('Database named %s already exists' %dbName)
			break

#drop database named dbName if possible
def dropDB(dbName):
	while True:
			try:
				shutil.rmtree(dbName)
				print('Database named %s was dropped' %dbName)
				break
			except:	
				print('Database named %s does not exist' %dbName)
				break

#change working directory into database dbName
def useDB(dbName):
	while True:
		try:
			if(os.path.exists(dbName)):
				os.chdir(dbName)
			else:
				os.chdir(os.path.dirname(os.getcwd()))
				os.chdir(dbName)
			print('Successfully opened %s' %dbName)
			break
		except:
			print('No database named %s found' %dbName)
			break

#create a table named tableName
def createTable(tableName, *argv):

	#this variable will keep track of each type and attribute name pair
	numberOfAttributes = len(argv)/2

	while True:
		try:
			#if the table with that name exists, sorry
			if(os.path.exists(tableName)):
				print('A table with the name %s already exists' %tableName)
				break
			#otherwise create a new file with the name tableName
			newTable = open('%s' %tableName, 'w')
			#write the attribute name and type pair to the file, iterating as many times as there are pairs of attribute types and their names
			i = 0
			while(i<=len(argv)-1):
				#if it's the last pair, then don't add the pipe character so it will look pretty
				if(i == len(argv)-2):
					#write the attribute name (argv[i]) and the attribute type (argv[i+1])
					newTable.write('%s %s' %(argv[i], argv[i+1]))
				else:
					newTable.write('%s %s | ' %(argv[i], argv[i+1]))
				#iterate i by two because we are printing in pairs
				i += 2
			print('Successfully created new table named %s' %tableName)
			newTable.close()
			break
		except Exception as e: 
			print('Unable to create table %s, exception: ' %tableName)
			print(e)
			break;

#delete a table named tableName
def dropTable(tableName):
	while True:
		try:
			os.remove(tableName)
			print('Successfully removed the table named %s' %tableName)
			break
		except FileNotFoundError:
			print('A table with the name %s does not exist' %tableName)
			break

#select table 
def selectTable(where, what):
	#simply print the contents of the table file line by line
	try:
		selectedFile = open(('%s') %(where), 'r')
		print(selectedFile.read())
		selectedFile.close()
	except:
		print('Table %s does not exist' %where)

#add an attribute to a table
def addToTable(where, attName, attType):
	#append to the end of the file a new attribute pair. This currently can only be done before values are added
	try:
		table = open('%s' %where, 'a')
		table.write('%s %s,' %(attName, attType))
		print('Successfully added to table')
		table.close()
	except:
		print('Unable to add to table')

#insert a row of data into a table
def insertInto(where, *argv):
	#write on a new line the values given, *argv is used to support multiple record additions in the future
	try:
		table = open('%s' %where, 'a')
		table.write('\n')
		i=0
		while(i<len(argv)):
			if(i == len(argv)-1):
				table.write('%s' %argv[i])
			else:
				table.write('%s | ' %argv[i])
			i+=1
		print('Successfully inserted 1 record into table')
	except Exception as e:
		print('Exception: ')
		print(e)

#all functions hereafter will utilize the table virtualization process documented in the readme

#update a given table's attribute where another attribute equals a condition
def update(table, setAttribute, setValue, whereAttribute, whereValue):
	try:
		virtualize.createVTable(table)
		virtualize.updateVTable(whereAttribute,whereValue,setAttribute,setValue)
		virtualize.saveVTable(table)
	except Exception as e:
		print('Unable to update table, exception: %s' %e)

#delete a table's row that equals a certain value
def deleteEq(table, attribute, value):
	try:
		virtualize.createVTable(table)
		virtualize.deleteEqFromVTable(attribute, value)
		virtualize.saveVTable(table)
	except Exception as e:
		print('Unable to delete from table, exception: %s' %e)

#delete a table's row that has a value greater than the given condition
def deleteGT(table, attribute, value):
	try:
		virtualize.createVTable(table)
		virtualize.deleteGTFromVTable(attribute, value)
		virtualize.saveVTable(table)
	except Exception as e:
		print('Unable to delete from table, exception: %s' %e)

#print a table with the two provided attributes on rows that meet the given condition
def selectFromWhereNot(attribute1, attribute2, table, whereAttribute, whereValue):
	try:
		virtualize.createVTable(table)
		virtualize.selectTwoFromWhereNot(attribute1, attribute2, whereAttribute, whereValue)
	except Exception as e:
		print('Unable to show data from table %s' %e)

def join(table1, table1Name, table2, table2Name, condition1, condition2):
	try:
		virtualize.createVTable(table1)
		virtualize.createSecondVTable(table2)
		virtualize.innerJoin(table1, table1Name, table2, table2Name, condition1, condition2)
	except Exception as e:
		print('Unable to perform inner join, %s' %e)

def leftOuterJoin(table1, table1Name, table2, table2Name, condition1, condition2):
	try:
		virtualize.createVTable(table1)
		virtualize.createSecondVTable(table2)
		virtualize.leftOuterJoin(table1, table1Name, table2, table2Name, condition1, condition2)
	except Exception as e:
		print('Unable to perform left outer join, %s' %e)