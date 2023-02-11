from os.path import isfile
from sys import argv

def add_( name_f , name_f2):
    
    if not isfile(name_f):exit("[!] File Not Exists")
    fx = open(name_f2 , 'a')
    with open(name_f , 'rb')as f:
            for dork in f.readlines():
                try:
                    dork = dork.rstrip()
                    fx.write(f"site:$ {dork.decode()}\n")
                except Exception as e:continue
    fx.close()
    
add_(argv[1] , argv[2])