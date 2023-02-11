from os.path import isfile
from threading import Thread
from time import sleep
import requests , sys
from webbrowser import open as op_w
def dorks(domain , enable_op):
    if domain.startswith("https://www.") or domain.startswith("http://www.") or domain.startswith("www."):
        domain_ = domain.split('.')[1]
    else:
        domain_ = domain
    if isfile("dorks_github.txt"):
        f_r = open(f"{domain_}_dorks_github.txt" , 'w')
        with open("dorks_github.txt" , 'r')as ff:
            for dork in ff.readlines():
                dork = dork.rstrip()
                f_r.write(f"https://github.com/search?q={domain_}+{dork}\n")
                if enable_op == 'y' or enable_op =='yes':
                    op_w(f"https://github.com/search?q={domain_}+{dork}")
                    op_w(f"https://gist.github.com/search?q={domain_}+{dork}&ref=searchresults")
                    sleep(10)
        f_r.close()
        print ("[+] Done")
    else:
        exit("[!] dorks_github.txt Not Found !")
if sys.argv[1] == '':exit("pass argument to enable_open\nexample: python3 dork_github.py y")
t = Thread(target=dorks, args=(sys.argv[1],sys.argv[2].lower(),))
t.start()