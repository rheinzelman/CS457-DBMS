import string
import os
import shutil
import sys

#vTable is a 2d array that temporarily stores the table's data for modification
#after modifications are done, the table file is overwritten with the new data 
vTable = []
vTable2 = []

#need comment here 
joinedTable = []

#tempVTable is used when conditional selection queries are called
tempVTable = []

#append a 2d array with the table values
def createVTable(tableName):
	#clear out old VTable data
	vTable.clear()
	tempVTable.clear()

	#iterate through each line, .split() the lines with a '|' character, and append them to one row per line
	try:
		with open(tableName) as table:
			while(line:=table.readline()):
				x = line.split('|')
				vTable.append(x)
		table.close()
	except Exception as e:
		print('Exception createVTable: %s' %e)

def createSecondVTable(tableName):
	#clear out old VTable data
	vTable2.clear()
	tempVTable.clear()

	#iterate through each line, .split() the lines with a '|' character, and append them to one row per line
	try:
		with open(tableName) as table:
			while(line:=table.readline()):
				x = line.split('|')
				vTable2.append(x)
		table.close()
	except Exception as e:
		print('Exception createVTable: %s' %e)

#this will get rid of trailing newlines. This was the absolute worst.
#create a temp variable, make it the value of the bottom right most element in the 2d array, strip it of newlines, and put it back in
def reformat():
	temp = float(vTable[len(vTable)-1][len(vTable[0])-1])
	vTable[len(vTable)-1][len(vTable[0])-1] = ' ' + str(temp) + ' '

def printTable(table):
	for i in range(len(table)):
		for j in range(len(table[i])):
			if(j < len(table[i])-1):
				print(table[i][j], end="")
				print(' | ', end="")
			else:			
				print(table[i][j])

#delete a table row
#at the row that needs to be deleted, overwrite the row with the one below it, and do that for every line below it until you reach the end
#pop the last row
def deleteVTableRow(rowIndex):
	i = rowIndex
	while(i < len(vTable)-1):
		vTable[i] = vTable[i+1]
		i = i + 1
	vTable.pop()

#update the setAttribute with setValue on the row where whereAttribute = whereValue
def updateVTable(whereAttribute,whereValue,setAttribute,setValue):
	whereCol = 0
	setCol = 0
	row = 0
	#find the column that contains whereAttribute by looking through the metadata
	for j in range(len(vTable[0])):
		if(whereAttribute in vTable[0][j]):
			whereCol = j
	#find the column that we need to update the value of 
	for j in range(len(vTable[0])):
		if(setAttribute in vTable[0][j]):
			setCol = j
	numberOfModifications = 0
	#go through each row, if whereValue is equal to the value contained on that row
	#make value of the row's setAttribute setValue, and make the formatting correct for where it may be inside the table
	for i in range(len(vTable)):
		if(whereValue == vTable[i][whereCol].replace(' ','')):
			numberOfModifications = numberOfModifications+1
			if(setCol != len(vTable[0])-1):
				vTable[i][setCol] = ' ' + setValue + ' '
			elif(setCol == 0):
				vTable[i][setCol] = setValue + ' '
			elif(setCol == len(vTable[0])-1 and i == len(vTable)-1):
				vTable[i][setCol] = ' ' + setValue + ' '
			else:
				vTable[i][setCol] = ' ' + setValue + '\n'
	print('%s record(s) modified' %numberOfModifications)

#write the table data back to disk
def saveVTable(table):
	#open the table file, and write each array element individually with correct formatting for its position in the table
	try:
		newTable = open('%s' %table, 'w')
		for i in range(len(vTable)):
			for j in range(len(vTable[0])):
				if(j != len(vTable[0])-1):
					newTable.write('%s|' %(vTable[i][j]))
				else:
					newTable.write('%s' %(vTable[i][j]))
		newTable.close()
	except Exception as e:
		print('Exception in saveVTable: %s' %e)

#delete a row if it's attribute is equal to value
def deleteEqFromVTable(attribute, value):
	whereCol = 0
	numberOfDeletions = 0
	#find the column we're searching in 
	for j in range(len(vTable[0])):
		if(attribute in vTable[0][j]):
			whereCol = j
	#if the row's attribute equals the value, call the delete function
	for i in range(1,len(vTable)-1):
		reformatted = vTable[i][whereCol].strip()
		if(value == reformatted):
			deleteVTableRow(i)
			numberOfDeletions = numberOfDeletions+1
	reformat()
	print('%s record(s) deleted' %numberOfDeletions)	

#delete a row if it's attribute is greater than a certain value
def deleteGTFromVTable(attribute,value):
	whereCol = 0
	numberOfDeletions = 0
	#find the column we'll be looking in 
	for j in range(len(vTable[0])):
		if(attribute in vTable[0][j]):
			whereCol = j
	i = 1
	length = len(vTable)-1
	#iterate through the rows, if the conditions are met, delete it 
	while(i <= length):
		reformatted = vTable[i][whereCol].strip()
		reformatted = reformatted.replace('\n', '')
		if(float(reformatted) > float(value)):
			deleteVTableRow(i)
			length = length-1
			numberOfDeletions = numberOfDeletions+1
		else:
			i = i+1
	reformat()
	print('%s record(s) deleted' %numberOfDeletions)	

#print a table with only the two specified attributes, where the row's attribute is equal to whereValue
def selectTwoFromWhereNot(attribute1, attribute2, whereAttribute, whereValue):
	appendCount = 1
	whereCol = 0
	#find the column to look for whereValue
	for j in range(len(vTable[0])):
		if(whereAttribute in vTable[0][j]):
			whereCol = j
	#append to the temporary virtual table all the rows that meet our condition
	tempVTable.append(vTable[0])
	for i in range(1,len(vTable)):
		reformatted = vTable[i][whereCol].strip()
		if(whereValue != reformatted):
			tempVTable.append(vTable[i])
			appendCount = appendCount + 1
	#clear the main vtable so we can add the specific columns
	vTable.clear()
	A1Col = 0
	A2Col = 0
	#find the columns we'll need to have in our final vtable
	for j in range(len(tempVTable[0])):
		if(attribute1 in tempVTable[0][j]):
			A1Col = j
		if(attribute2 in tempVTable[0][j]):
			A2Col = j
	#add to the vtable the metadata, and the columns of the temporary vtable that we need
	newRow = [tempVTable[0][A1Col].replace('\n',''), tempVTable[0][A2Col].replace('\n','')]
	vTable.append(newRow)
	for i in range (1, len(tempVTable)):
		newRow = [tempVTable[i][A1Col].replace('\n',''), tempVTable[i][A2Col].replace('\n','')]
		vTable.append(newRow)
	#print the vTable
	printTable(vTable)

#note, this will only work if joining two tables, no more! 
def appendJoinedRow(row1,row2):
		tempRow = []
		for i in range(len(vTable[row1])):
			#this will get rid of the pesky trailing newline
			if(i == len(vTable[row1])-1):
				tempRow.append(vTable[row1][i].replace('\n', ''))
			else:
				tempRow.append(vTable[row1][i])
		for i in range(len(vTable2[row2])):
			tempRow.append(vTable2[row2][i])

		joinedTable.append(tempRow)

def innerJoin(table1, table1Name, table2, table2Name, condition1, condition2):
		#split up the condition strings
		conditionTemp = condition1.split('.')
		condition1 = conditionTemp[1]
		conditionTemp = condition2.split('.')
		condition2 = conditionTemp[1]

		#find the columns we need to be comparing
		whereCol1 = 0
		whereCol2 = 0
		for i in range(len(vTable[0])):
			if(condition1 in vTable[0][i]):
				whereCol1 = i
		for j in range(len(vTable2[0])):
			if(condition2 in vTable2[0][j]):
				whereCol2 = j

		#clear the joinedTable for a new joinedTable
		joinedTable.clear()

		#appendJoinedRow needs to be changed to join two independent rows
		appendJoinedRow(0,0)

		#for each row that meets the join conditions, append them to the joinedTable
		for i in range(1, len(vTable)):
			for j in range(1, len(vTable2)):
				if(vTable[i][whereCol1] == vTable2[j][whereCol2]):
					appendJoinedRow(i,j)

		#get rid of trailing newline
		for i in range(len(joinedTable)):
			reformatted = joinedTable[i][len(joinedTable[i])-1]
			reformatted = reformatted.replace('\n', '')
			joinedTable[i][len(joinedTable[i])-1] = joinedTable[i][len(joinedTable[i])-1].replace('\n', '')

		printTable(joinedTable)
		

def leftOuterJoin(table1, table1Name, table2, table2Name, condition1, condition2):
	try:
		#split up the condition strings
		conditionTemp = condition1.split('.')
		condition1 = conditionTemp[1]
		conditionTemp = condition2.split('.')
		condition2 = conditionTemp[1]

		
		#find the columns we need to be comparing
		whereCol1 = 0
		whereCol2 = 0
		for i in range(len(vTable[0])):
			if(condition1 in vTable[0][i]):
				whereCol1 = i
		for j in range(len(vTable2[0])):
			if(condition2 in vTable2[0][j]):
				whereCol2 = j

		#clear the joinedTable for new joinedTable
		joinedTable.clear()

		#append the metadata to the joinedTable
		appendJoinedRow(0,0)

		#add each row of the first table, and each appropriate row of the second
		tempRow = []
		for i in range(1, len(vTable)):
			alreadyAdded = False
			for j in range(1, len(vTable2)):
				if(vTable[i][whereCol1] == vTable2[j][whereCol2]):
					appendJoinedRow(i,j)
					alreadyAdded = True
			if(vTable[i][whereCol1] != vTable2[j][whereCol2] and alreadyAdded == False):
				joinedTable.append(vTable[i])
		
		#get rid of trailing newline
		for i in range(len(joinedTable)):
			reformatted = joinedTable[i][len(joinedTable[i])-1]
			reformatted = reformatted.replace('\n', '')
			joinedTable[i][len(joinedTable[i])-1] = joinedTable[i][len(joinedTable[i])-1].replace('\n', '')

		printTable(joinedTable)	
		
		
	except:
		exception_type, exception_object, exception_traceback = sys.exc_info()
		filename = exception_traceback.tb_frame.f_code.co_filename
		line_number = exception_traceback.tb_lineno
		print("Exception type: ", exception_type)
		print("File name: ", filename)
		print("Line number: ", line_number)
