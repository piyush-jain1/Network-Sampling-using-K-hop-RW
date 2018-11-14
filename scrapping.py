import urllib2

url = "http://dl.acm.org/events.cfm"

text = ["SIGMOD","PODS","VLDB","ICDE","EDBT","ICDT","SSDBM","CIDR","DASFAA","ADBIS", "DEXA","DaWaK","KDD","ICDM","CIKM","PKDD","PAKDD","SDM","ASONAM","CHI","IUI","CSCW","NIPS","ICML","ICLR","AAAI","IJCAI","UAI","AISTATS","ECAI", "WWW","WSDM","Hypertext","ISWC","ESWC","WI","KSEM","iiWAS","ICWSM","JIST","WebSci", "SocInfo", "SIGIR","ECIR","RecSys","AIRS","CHIIR","ICTIR", "ICSE","FSE","ASE","MSR","ICST", "COMPSAC", "ACM MM","ICMR","MoMM", "MMSys","ACL","NAACL","COLING","EACL","CoNLL","EMNLP", "IJCNLP", "LREC","JCDL","ICADL", "TPDL","FOCS","SODA","SAC","AINA","MEDES", "IEEE BigData","DSAA"]

# read = urllib2.urlopen(url).read()
req = urllib2.build_opener()
req.addheaders = [('User-Agent', 'Google Chrome')]
response = req.open(url).read()

for word in text:
	if word in response:
		print word
