#-*- coding: utf8 -*-

#
# Założenia:
#		* http://whatismyipaddress.com/proxy-check działa 24/7/365
#

import urllib2
import re
import sys

# MAXIPNUM - ilość IP które mają być sprawdzone
# TIMEOUT - maksymalny czas oczekiwania na odpowiedź proxy
# proxylist_urls - adresy stron list proxy w formacie ip:port
MAXIPNUM = 50;
TIMEOUT = 5;
proxylist_urls = [ "http://elite-proxies.blogspot.com/",
					"http://eliteproxy.blogspot.com/search/label/elite%20proxy",
					"http://www.samair.ru/proxy/",
					"http://www.samair.ru/proxy/proxy-02.htm",
					"http://www.samair.ru/proxy/proxy-03.htm",
					"http://www.samair.ru/proxy/proxy-04.htm",
					"http://www.samair.ru/proxy/proxy-05.htm" ];

content = "";
for proxylist in proxylist_urls:
	www = urllib2.urlopen(proxylist);
	content += www.read();

preg = re.compile('([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}):([0-9]+)');
ipaddrs = preg.findall(content);

print("Number of proxies: " + str(len(ipaddrs)));

i = 0;
for ip in ipaddrs:
	if i == MAXIPNUM:
		break;
	i += 1;

	sys.stdout.flush();

	# sprawdzenie czy proxy wykrywalne + działające
	proxy = urllib2.ProxyHandler( {'http' : ip[0]+':'+ip[1]} );
	opr = urllib2.build_opener(proxy);
	urllib2.install_opener(opr);

	try:
		pcheck = urllib2.urlopen("http://whatismyipaddress.com/proxy-check", None, TIMEOUT);
		pch_content = pcheck.read();
	except:
		if i % 10 != 0:	# wodotryski
			sys.stdout.write(".")
		else:
			sys.stdout.write("\r           \r");
		continue;

	mobj = re.findall('<span style="color:#FF0000;">TRUE</span>', pch_content)
	if len(mobj) != 0:
		sys.stdout.write("\r" + ip[0] + " : " + ip[1] + "\t[ PROXY DETECTED ("+ str(len(mobj)) +" / 6) ]\n");
	else:
		sys.stdout.write("\r" + ip[0] + " : " + ip[1] + "\n");
		
print("\n - ende - ");
