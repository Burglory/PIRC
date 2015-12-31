import src.configs
import src.logger
import urllib.request, subprocess, zipfile, os, sys

def update():
	url = ""
	url = src.configs.Config.configDict["SOFTWARE_SRC_URL"]
	url = url + "/archive/master.zip"
		
	urllib.request.urlretrieve(url, "_PIRC.zip")
	
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

if __name__ == "__main__":
	update()
