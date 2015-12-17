import src.configs
import urllib.request, subprocess, zipfile, os

c = src.configs.Config("default.conf")

url = c.configdictionary["software_source_url"]
ziplink = url + "/archive/master.zip"
urllib.request.urlretrieve(ziplink, "_PIRC.zip")

#subprocess.call(["unzip","PIRC.zip","-d","..", "-o"])
zipf = zipfile.ZipFile("_PIRC.zip",'r')
newzipf = zipfile.ZipFile("PIRC.zip",'w')
for name in zipf.namelist():
	data = zipf.read(name)
	if len(data) > 0:
		newzipf.writestr(name.replace("PIRC-master/",""), data)

newzipf.extractall()
zipf.close()
newzipf.close()
os.remove("_PIRC.zip")
