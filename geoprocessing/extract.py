import requests, zipfile, io
import lxml.html as lh



#this script will download all census tract and subcountry tiger file zips and extract them to a folder

fileNames = []
baseUrl = "https://www2.census.gov/geo/tiger/TIGER2012/COUSUB/" #change depending on which boundary type you are downloading
#Create a handle, page, to handle the contents of the website
page = requests.get(baseUrl)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//td//a')
for t in tr_elements:
    #print(t.text_content())
    names = t.text_content()
    if ".zip" in names:
        fileNames.append(names)

#print(fileNames)
for zips in fileNames:
    try:
        r = requests.get(baseUrl+zips)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path="Boundaries/comparison/subcounties") #change depending on which boundary type you are downloading
        print(zips +" downloaded")
    except:
        print("*** "+zips + " file not working")
        
        continue

print("done!")