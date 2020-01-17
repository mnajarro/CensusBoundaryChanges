import requests, zipfile, io
import os
import lxml.html as lh

# this script will download all census tract and subcountry tiger file zips and extract them to a folder
tigerType = ['COUSUB', 'COUNTY', 'TRACT', 'ZCTA5']
tigerYear = ['TIGER2012', 'TIGER2013', 'TIGER2014','TIGER2015','TIGER2016','TIGER2016','TIGER2017','TIGER2018']
fileNames = []
baseUrl = "https://www2.census.gov/geo/tiger/"
decision = input("Do you want to download and save or download and extract? Enter download or extract: ")

for year in tigerYear:
    for tType in tigerType:
        # Create a handle, page, to handle the contents of the website
        print(baseUrl+year+'/'+tType)
        page = requests.get(baseUrl+year+'/'+tType)
        # Store the contents of the website under doc
        doc = lh.fromstring(page.content)
        # Parse data that are stored between <tr>..</tr> of HTML
        tr_elements = doc.xpath('//td//a')
        for t in tr_elements:
            # print(t.text_content())
            names = t.text_content()
            if ".zip" in names:
                fileNames.append(names)

        # print(fileNames)
        # Downloads and unzips
        for zips in fileNames:
            try:
                r = requests.get(baseUrl+year+'/'+tType+'/'+zips)
                path = os.getcwd()
                print(path)
                # if simply trying to download use this code else use other
                if decision == 'download':
                    # os.makedirs(os.path.dirname(path+zips), exist_ok=True)
                    # with open(path+zips, "w") as f:
                    #     f.write(r.content)
                    #     f.close()
                    zfile = open(zips, 'wb')
                    zfile.write(r.content)
                    zfile.close()
                    print(zips + " downloaded")
                elif decision == 'extract':
                    z = zipfile.ZipFile(io.BytesIO(r.content))
                    if not os.path.exists(os.path.dirname(path+tType)):
                        os.makedirs(path+tType)
                    z.extractall(path=path+'/'+tType) #change depending on which boundary type you are downloading
                    print(zips +" downloaded and extracted")
                else:
                    print("didn't enter download or extract. Rerun and enter either download or extract ")
            except OSError as err:
                print("OS error: {0}".format(err))
            except:
                print("*** "+zips + " file not working")

                continue

print("done!")