import sys
import sqlite3
import os

# retreive.py pull the data from sqlite and write the html file

""" getData( conn, rowid ) """
""" Pull the data from sqlite """
def getData( conn, rowid ):
	arrData = []
	cursor = conn.cursor()

	""" Recursive query to extract recursively the category tree """
	query= 'WITH RECURSIVE '\
			  'under_category(Id,Name, ParentID, Level, BestOfferEnabled, Count) AS ( '\
				'SELECT DISTINCT  Id, Name, ParentID, 1, BestOfferEnabled, '\
					'(SELECT COUNT(*) FROM CATEGORY AS CT WHERE CT.PARENTID = C.ID) AS CN '\
					'FROM CATEGORY AS C WHERE ID = ? '\
				'UNION ALL '\
				'SELECT DISTINCT C.Id, C.Name, C.ParentID, uc.Level+1, C.BestOfferEnabled, '\
					'(SELECT COUNT(*) FROM CATEGORY AS CT WHERE CT.PARENTID = C.ID) AS CN '\
				  'FROM CATEGORY AS C INNER JOIN under_category AS uc ON C.ParentId=uc.Id '\
				 'ORDER BY 4 DESC, c.Name '\
			  ') '\
			'SELECT Id,Name, ParentID, Level, BestOfferEnabled, Count '\
			'FROM under_category;'
	cursor.execute(query, (rowid,))
	#print query

	arrData = cursor.fetchall()
	conn.close()
	if len(arrData) == 0:
		sys.exit("No category with ID: " + str(rowid))
	return arrData 			

""" setHtml( arrData ) """
""" Create the html string """
def setHtml( arrData ):
	iArrNode = []
	iPastLevel = 1;
	sNodeInf = "";
	sInfoHtml = ""
	sBestOffer = ""
	
	sHtmlCategory = "<input type=\"checkbox\" id=\"{@node@}\" checked=\"checked\" /><label><input type=\"checkbox\" /><span></span></label><label for=\"{@node@}\">ID:{@id@}-&nbsp;<b>{@category@}</b>-&nbsp;Level:{@level@}-&nbsp;Best Offer:{@bestoffer@}</label>"
	for row in arrData:
		#print row[0], row[1], row[2], row[3], row[4], row[5]
		
		if len(iArrNode) < row[3]:
			iArrNode.append(0);
		if iPastLevel > row[3]:
			iArrNode[row[3] - 1] += 1 
			iArrNode[iPastLevel - 1] = 0
			
		for x in range(0, row[3]):
			if x == 0:
				sNodeInf = "node-" + str(iArrNode[x])
			else:
				sNodeInf = sNodeInf + "-" + str(iArrNode[x])
				iArrNode[x] += 1
		
		if row[4] == 1:
			sBestOffer = "yes"
		else:
			sBestOffer = "no"
					
		sCloseBase = "</ul></li>"
		sCloseFinal = ""

		if iPastLevel > row[3]:		
			for x in range(0, iPastLevel - row[3]):
				sCloseFinal = sCloseFinal + sCloseBase
			sInfoHtml = sInfoHtml + sCloseFinal + "<li>" + sHtmlCategory.replace("{@node@}", sNodeInf).replace("{@id@}", str(row[0])).replace("{@category@}", row[1]).replace("{@bestoffer@}", sBestOffer).replace("{@level@}", str(row[3]))
		else:
			sInfoHtml = sInfoHtml + "<li>" + sHtmlCategory.replace("{@node@}", sNodeInf).replace("{@id@}", str(row[0])).replace("{@category@}", row[1]).replace("{@bestoffer@}", sBestOffer).replace("{@level@}", str(row[3]))
		if row[5] == 0: 
			sInfoHtml = sInfoHtml + "</li>"
		else:
			sInfoHtml = sInfoHtml + "<ul>"
			
		iPastLevel = int(row[3])
	
	return sInfoHtml
	

if len(sys.argv) == 1:
	sys.exit("The category is missing")
try:
	value=int(sys.argv[1])
except ValueError:
	sys.exit("Your input should be a number")
	
if os.path.exists('Categories'):

	arrData = []
	


	with open('root/template.html', 'r') as rTemplate:
		sData = rTemplate.read()
		
		conn = sqlite3.connect('Categories')
		
		arrData = getData( conn, sys.argv[1] )
		conn.close()
		if len(arrData) > 0:
			sInfoHtml = setHtml(arrData)
			
			sData = sData.replace("{@htmldata@}",sInfoHtml)
			with open('result/' + sys.argv[1] + '.html', 'w') as wResult:
				wResult.write(sData.encode('utf8'))
				wResult.close()
	rTemplate.close()
	
	print "html page \"" + sys.argv[1] + ".html\" created succesfuly" 

else:
	print "The database doesn't exist"



