import sqlite3
import os
import xml.etree.ElementTree as ET
import urllib2

# save.py receive the data from the api and save it in to sqlite

if os.path.exists('Categories'):
    	os.remove('Categories')

conn = sqlite3.connect('Categories')

conn.execute('''CREATE TABLE CATEGORY
       (Id INT	PRIMARY KEY,
       Name           TEXT    NOT NULL,
       Level          INT     NOT NULL,
       BestOfferEnabled        INT	NOT NULL,
       ParentID		INT	NULL REFERENCES CATEGORY) WITHOUT ROWID;''')


req = urllib2.Request('https://api.sandbox.ebay.com/ws/api.dll')
req.add_header('X-EBAY-API-CALL-NAME', 'GetCategories')
req.add_header('X-EBAY-API-APP-NAME', 'EchoBay62-5538-466c-b43b-662768d6841')
req.add_header('X-EBAY-API-CERT-NAME', '00dd08ab-2082-4e3c-9518-5f4298f296db')
req.add_header('X-EBAY-API-DEV-NAME', '16a26b1b-26cf-442d-906d-597b60c41c19')
req.add_header('X-EBAY-API-SITEID', '0') 
req.add_header('X-EBAY-API-COMPATIBILITY-LEVEL', '861')
req.add_data('<?xml version="1.0" encoding="utf-8"?><GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents"><CategoryParent>10542</CategoryParent><CategorySiteID>0</CategorySiteID><ViewAllNodes>True</ViewAllNodes><DetailLevel>ReturnAll</DetailLevel><RequesterCredentials><eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**PMIhVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhCpaCpQWdj6x9nY+seQ**L0MCAA**AAMAAA**IahulXaONmBwi/Pzhx0hMqjHhVAz9/qrFLIkfGH5wFH8Fjwj8+H5FN4NvzHaDPFf0qQtPMFUaOXHpJ8M7c2OFDJ7LBK2+JVlTi5gh0r+g4I0wpNYLtXnq0zgeS8N6KPl8SQiGLr05e9TgLRdxpxkFVS/VTVxejPkXVMs/LCN/Jr1BXrOUmVkT/4Euuo6slGyjaUtoqYMQnmBcRsK4xLiBBDtiow6YHReCJ0u8oxBeVZo3S2jABoDDO9DHLt7cS73vPQyIbdm2nP4w4BvtFsFVuaq6uMJAbFBP4F/v/U5JBZUPMElLrkXLMlkQFAB3aPvqZvpGw7S8SgL7d2s0GxnhVSbh4QAqQrQA0guK7OSqNoV+vl+N0mO24Aw8whOFxQXapTSRcy8wI8IZJynn6vaMpBl5cOuwPgdLMnnE+JvmFtQFrxa+k/9PRoVFm+13iGoue4bMY67Zcbcx65PXDXktoM3V+sSzSGhg5M+R6MXhxlN3xYfwq8vhBQfRlbIq+SU2FhicEmTRHrpaMCk4Gtn8CKNGpEr1GiNlVtbfjQn0LXPp7aYGgh0A/b8ayE1LUMKne02JBQgancNgMGjByCIemi8Dd1oU1NkgICFDbHapDhATTzgKpulY02BToW7kkrt3y6BoESruIGxTjzSVnSAbGk1vfYsQRwjtF6BNbr5Goi52M510DizujC+s+lSpK4P0+RF9AwtrUpVVu2PP8taB6FEpe39h8RWTM+aRDnDny/v7wA/GkkvfGhiioCN0z48</eBayAuthToken></RequesterCredentials></GetCategoriesRequest>')

try:
	resp = urllib2.urlopen(req)
	content = resp.read()
except URLError as e:
	print e.reason
	
tree = ET.fromstring(content)

CategoryArray = tree.findall('{urn:ebay:apis:eBLBaseComponents}CategoryArray')

for Category in CategoryArray[0]:
	CategoryID = Category.find('{urn:ebay:apis:eBLBaseComponents}CategoryID')
	CategoryName = Category.find('{urn:ebay:apis:eBLBaseComponents}CategoryName')
	CategoryLevel = Category.find('{urn:ebay:apis:eBLBaseComponents}CategoryLevel')
	BestOfferEnabled = Category.find('{urn:ebay:apis:eBLBaseComponents}BestOfferEnabled')
	CategoryParentID = Category.find('{urn:ebay:apis:eBLBaseComponents}CategoryParentID')
	if CategoryParentID.text == CategoryID.text:
		conn.execute("INSERT INTO CATEGORY (Id,Name,Level,BestOfferEnabled) \
				VALUES (?,?,?,? )",(CategoryID.text, CategoryName.text, CategoryLevel.text, BestOfferEnabled.text ));	
	else:
		conn.execute("INSERT INTO CATEGORY (Id,Name,Level,BestOfferEnabled,ParentID) \
				VALUES (?,?,?,?,? )",(CategoryID.text, CategoryName.text, CategoryLevel.text, BestOfferEnabled.text, CategoryParentID.text));

conn.commit()
conn.close()

print "database created successfully";
