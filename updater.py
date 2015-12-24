import src.configs
import urllib.request, subprocess, zipfile, os, sys

def extractConfigFileArgument():
	if len(sys.argv) > 1:
		return sys.arv[1]
	return ""

if __name__ == "__main__":
	if extractConfigFileArgument():
		src.configs.Config(extractConfigFileArgument())
	else:
		pass
		#src.configs.Config("default.conf")
	
	url = ""
	if src.configs.Config.isloaded:
		url = src.configs.Config.configdictionary["SOFTWARE_SRC_URL"]
		url = url + "/archive/master.zip"
	else:
		print("Error: Config file has not been properly loaded. Cannot read download URL.")
		url = raw_input("\tPlease enter download URL for the zip file manually:")
		
	urllib.request.urlretrieve(url, "_PIRC.zip")
	
	#subprocess.call(["unzip","PIRC.zip","-d","..", "-o"])
	zipf = zipfile.ZipFile("_PIRC.zip",'r')
	newzipf = zipfile.ZipFile("PIRC.zip",'w')
	for name in zipf.namelist():
		data = zipf.read(name)
		if len(data) > 0:
			newzipf.writestr(name.replace("PIRC-master/",""), data)
	
	#newzipf.extractall()
	zipf.close()
	newzipf.close()
	os.remove("_PIRC.zip")
