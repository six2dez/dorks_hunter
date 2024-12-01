#!/usr/bin/env python3
import sys
import random
import time
import tldextract
import argparse
from googlesearch import search
from fake_useragent import UserAgent

def parseArgs():
    message = "Simple Google dork search"
    parser = argparse.ArgumentParser(description=message)
    parser.add_argument('--domain', '-d', required=True, help='Domain to scan')
    parser.add_argument('--results', '-r', help='Number of results per search, default 10', type=int)
    parser.add_argument('--output', '-o', help='Output file')
    parser.parse_args()
    args = parser.parse_args()
    return args

def save(file, data):
    with open(file, "a") as f:
        f.write(str(data))
        f.write("\n")

def main():
    inputs = parseArgs()
    amount = inputs.results if inputs.results else 10
    requ = 0
    domain = inputs.domain
    target = tldextract.extract(str(domain)).domain

    # Initialize the UserAgent object
    ua = UserAgent()

    dorks = {
    "# .git folders (https://www.google.com/search?q=inurl%3A%22%2F.git%22"+domain+"+-github)": "inurl:\"/.git\" "+domain+" -github",
    "# Backup files (https://www.google.com/search?q=site%3A"+domain+"+ext%3Abkf+%7C+ext%3Abkp+%7C+ext%3Abak+%7C+ext%3Aold+%7C+ext%3Abackup)": "site:"+domain+" ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup",
    "# Exposed documents (https://www.google.com/search?q=site%3A"+domain+"+ext%3Adoc+%7C+ext%3Adocx+%7C+ext%3Aodt+%7C+ext%3Apdf+%7C+ext%3Artf+%7C+ext%3Asxw+%7C+ext%3Apsw+%7C+ext%3Appt+%7C+ext%3Apptx+%7C+ext%3Apps+%7C+ext%3Acsv+%7C+filetype%3Adoc+%7C+filetype%3Adocx+%7C+filetype%3Axls+%7C+filetype%3Axlsx+%7C+filetype%3Appt+%7C+filetype%3Apptx+%7C+filetype%3Amdb+%7C+filetype%3Apdf+%7C+filetype%3Asql+%7C+filetype%3Atxt+%7C+filetype%3Artf+%7C+filetype%3Acsv+%7C+filetype%3Axml+%7C+filetype%3Aconf+%7C+filetype%3Adat+%7C+filetype%3Aini+%7C+filetype%3Alog+%7C+index%2520of%3Aid_rsa%2520id_rsa.pub+%7C+filetype%3Apy+%7C+filetype%3Ahtml+%7C+filetype%3Ash+%7C+filetype%3Aodt+%7C+filetype%3Akey+%7C+filetype%3Asign+%7C+filetype%3Amd+%7C+filetype%3Aold+%7C+filetype%3Abin+%7C+filetype%3Acer+%7C+filetype%3Acrt+%7C+filetype%3Apfx+%7C+filetype%3Acrl+%7C+filetype%3Acrs+%7C+filetype%3Ader)": "site:"+domain+" ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv | filetype:doc | filetype:docx | filetype:xls | filetype:xlsx | filetype:ppt | filetype:pptx | filetype:mdb | filetype:pdf | filetype:sql | filetype:txt | filetype:rtf | filetype:csv | filetype:xml | filetype:conf | filetype:dat | filetype:ini | filetype:log | index%20of:id_rsa%20id_rsa.pub | filetype:py | filetype:html | filetype:sh | filetype:odt | filetype:key | filetype:sign | filetype:md | filetype:old | filetype:bin | filetype:cer | filetype:crt | filetype:pfx | filetype:crl | filetype:crs | filetype:der" ,
    "# Confidential documents (https://www.google.com/search?q=inurl%3A"+target+"+not+for+distribution+%7C+confidential+%7C+%22employee+only%22+%7C+proprietary+%7C+top+secret+%7C+classified+%7C+trade+secret+%7C+internal+%7C+private+filetype%3Axls+OR+filetype%3Acsv+OR+filetype%3Adoc+OR+filetype%3Apdf)": "inurl:"+target+" not for distribution | confidential | \"employee only\" | proprietary | top secret | classified | trade secret | internal | private filetype:xls OR filetype:csv OR filetype:doc OR filetype:pdf",
    "# Config files (https://www.google.com/search?q=site%3A"+domain+"+ext%3Axml+%7C+ext%3Aconf+%7C+ext%3Acnf+%7C+ext%3Areg+%7C+ext%3Ainf+%7C+ext%3Ardp+%7C+ext%3Acfg+%7C+ext%3Atxt+%7C+ext%3Aora+%7C+ext%3Aenv+%7C+ext%3Aini)": "site:"+domain+" ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:env | ext:ini",
    "# Database files (https://www.google.com/search?q=site%3A"+domain+"+ext%3Asql+%7C+ext%3Adbf+%7C+ext%3Amdb)": "site:"+domain+" ext:sql | ext:dbf | ext:mdb",
    "# Other files (https://www.google.com/search?q=site%3A"+domain+"+intitle%3Aindex.of+%7C+ext%3Alog+%7C+ext%3Aphp+intitle%3Aphpinfo+%22published+by+the+PHP+Group%22+%7C+inurl%3Ashell+%7C+inurl%3Abackdoor+%7C+inurl%3Awso+%7C+inurl%3Acmd+%7C+shadow+%7C+passwd+%7C+boot.ini+%7C+inurl%3Abackdoor+%7C+inurl%3Areadme+%7C+inurl%3Alicense+%7C+inurl%3Ainstall+%7C+inurl%3Asetup+%7C+inurl%3Aconfig+%7C+inurl%3A%22%2Fphpinfo.php%22+%7C+inurl%3A%22.htaccess%22+%7C+ext%3Aswf)": "site:"+domain+" intitle:index.of | ext:log | ext:php intitle:phpinfo \"published by the PHP Group\" | inurl:shell | inurl:backdoor | inurl:wso | inurl:cmd | shadow | passwd | boot.ini | inurl:backdoor | inurl:readme | inurl:license | inurl:install | inurl:setup | inurl:config | inurl:\"/phpinfo.php\" | inurl:\".htaccess\" | ext:swf",
    "# SQL errors (https://www.google.com/search?q=site%3A"+domain+"+intext%3A%22sql+syntax+near%22+%7C+intext%3A%22syntax+error+has+occurred%22+%7C+intext%3A%22incorrect+syntax+near%22+%7C+intext%3A%22unexpected+end+of+SQL+command%22+%7C+intext%3A%22Warning%3A+mysql_connect%28%29%22+%7C+intext%3A%22Warning%3A+mysql_query%28%29%22+%7C+intext%3A%22Warning%3A+pg_connect%28%29%22)": "site:"+domain+" intext:\"sql syntax near\" | intext:\"syntax error has occurred\" | intext:\"incorrect syntax near\" | intext:\"unexpected end of SQL command\" | intext:\"Warning: mysql_connect()\" | intext:\"Warning: mysql_query()\" | intext:\"Warning: pg_connect()\"",
    "# PHP errors (https://www.google.com/search?q=site%3A"+domain+"+%22PHP+Parse+error%22+%7C+%22PHP+Warning%22+%7C+%22PHP+Error%22)": "site:"+domain+" \"PHP Parse error\" | \"PHP Warning\" | \"PHP Error\"",
    "# Wordpress files (https://www.google.com/search?q=site%3A"+domain+"+inurl%3Awp-content+%7C+inurl%3Awp-includes)": "site:"+domain+" inurl:wp-content | inurl:wp-includes",
    "# Project management sites (https://www.google.com/search?q=site%3Atrello.com+%7C+site%3A%2A.atlassian.net+%22"+target+"%22)": "site:trello.com | site:*.atlassian.net \""+target+"\"",
    "# Subdomains (https://www.google.com/search?q=site%3A%2A."+domain+")": "site:*."+domain+"",
    "# Sub-subdomains (https://www.google.com/search?q=site%3A%2A.%2A."+domain+")": "site:*.*."+domain+"",
    "# Path traversal (https://www.google.com/search?q=site%3A"+domain+"+intitle%3A%2522index%2520of%2522%2520%2522parent%2520directory%2522+%7C+intitle%3A%2522index%2520of%2522%2520%2522DCIM%2522+%7C+intitle%3A%2522index%2520of%2522%2520%2522ftp%2522+%7C+intitle%3A%2522index%2520of%2522%2520%2522backup%2522+%7C+intitle%3A%2522index%2520of%2522%2520%2522mail%2522+%7C+intitle%3A%2522index%2520of%2522%2520%2522password%2522+%7C+intitle%3A%2522index%2520of%2522%2520%2522pub%2522+%7C+intitle%3A%2522index%2520of%2522%2520%2522.git%2522)": "\""+target+"\" intitle:%22index%20of%22%20%22parent%20directory%22 | intitle:%22index%20of%22%20%22DCIM%22 | intitle:%22index%20of%22%20%22ftp%22 | intitle:%22index%20of%22%20%22backup%22 | intitle:%22index%20of%22%20%22mail%22 | intitle:%22index%20of%22%20%22password%22 | intitle:%22index%20of%22%20%22pub%22 | intitle:%22index%20of%22%20%22.git%22",
    "# GitLab/GitHub/Bitbucket (https://www.google.com/search?q=site%3Agithub.com+%7C+site%3Agitlab.com+%7C+site%3Abitbucket.org+%22"+target+"%22)": "site:github.com | site:gitlab.com | site:bitbucket.org \""+target+"\"",
    "# Cloud buckets S3/GCP (https://www.google.com/search?q=site%3A.s3.amazonaws.com+%7C+site%3Astorage.googleapis.com+%7C+site%3Aamazonaws.com+%22"+target+"%22)": "site:.s3.amazonaws.com | site:storage.googleapis.com | site:amazonaws.com \""+target+"\"",
    "# Traefik (https://www.google.com/search?q=intitle%3Atraefik+inurl%3A8080%2Fdashboard+%22"+target+"%22)": "intitle:traefik inurl:8080/dashboard \""+target+"\"",
    "# Jenkins (https://www.google.com/search?q=intitle%3A%22Dashboard+%5BJenkins%5D%22+%22"+target+"%22)": "intitle:\"Dashboard [Jenkins]\" \""+target+"\"",
    "# Login pages (https://www.google.com/search?q=site%3A"+domain+"+inurl%3Asignup+%7C+inurl%3Aregister+%7C+intitle%3ASignup+%7C+inurl%3Aadmin+%7C+inurl%3Alogin+%7C+inurl%3Aadminlogin+%7C+inurl%3Acplogin+%7C+inurl%3Aweblogin+%7C+inurl%3Aquicklogin+%7C+inurl%3Awp-admin+%7C+inurl%3Awp-login+%7C+inurl%3Aportal+%7C+inurl%3Auserportal+%7C+inurl%3Aloginpanel+%7C+inurl%3Amemberlogin+%7C+inurl%3Aremote+%7C+inurl%3Adashboard+%7C+inurl%3Aauth+%7C+inurl%3Aexchange+%7C+inurl%3AForgotPassword+%7C+inurl%3Atest)": "site:"+domain+" inurl:signup | inurl:register | intitle:Signup | inurl:admin | inurl:login | inurl:adminlogin | inurl:cplogin | inurl:weblogin | inurl:quicklogin | inurl:wp-admin | inurl:wp-login | inurl:portal | inurl:userportal | inurl:loginpanel | inurl:memberlogin | inurl:remote | inurl:dashboard | inurl:auth | inurl:exchange | inurl:ForgotPassword | inurl:test",
    "# Open redirects (https://www.google.com/search?q=site%3A"+domain+"+inurl%3Aredir+%7C+inurl%3Aurl+%7C+inurl%3Aredirect+%7C+inurl%3Areturn+%7C+inurl%3Asrc%3Dhttp+%7C+inurl%3Ar%3Dhttp)": "site:"+domain+" inurl:redir | inurl:url | inurl:redirect | inurl:return | inurl:src=http | inurl:r=http",
    "# Code share sites (https://www.google.com/search?q=site%3Asharecode.io+%7C+site%3Acontrolc.com+%7C+site%3Acodepad.co+%7Csite%3Aideone.com+%7C+site%3Acodebeautify.org+%7C+site%3Ajsdelivr.com+%7C+site%3Acodeshare.io+%7C+site%3Acodepen.io+%7C+site%3Arepl.it+%7C+site%3Ajsfiddle.net+%22"+target+"%22)": "site:sharecode.io | site:controlc.com | site:codepad.co |site:ideone.com | site:codebeautify.org | site:jsdelivr.com | site:codeshare.io | site:codepen.io | site:repl.it | site:jsfiddle.net \""+target+"\"",
    "# Other 3rd parties sites (https://www.google.com/search?q=site%3Agitter.im+%7C+site%3Apapaly.com+%7C+site%3Aproductforums.google.com+%7C+site%3Acoggle.it+%7C+site%3Areplt.it+%7C+site%3Aycombinator.com+%7C+site%3Alibraries.io+%7C+site%3Anpm.runkit.com+%7C+site%3Anpmjs.com+%7C+site%3Ascribd.com+%22"+target+"%22)": "site:gitter.im | site:papaly.com | site:productforums.google.com | site:coggle.it | site:replt.it | site:ycombinator.com | site:libraries.io | site:npm.runkit.com | site:npmjs.com | site:scribd.com \""+target+"\"",
    "# Stackoverflow (https://www.google.com/search?q=site%3Astackoverflow.com+%22"+domain+"%22)": "site:stackoverflow.com \""+domain+"\"",
    "# Pastebin-like sites (https://www.google.com/search?q=site%3Ajustpaste.it+%7C+site%3Aheypasteit.com+%7C+site%3Apastebin.com+%22"+target+"%22)": "site:justpaste.it | site:heypasteit.com | site:pastebin.com \""+target+"\"",
    "# Apache Struts RCE (https://www.google.com/search?q=site%3A"+domain+"+ext%3Aaction+%7C+ext%3Astruts+%7C+ext%3Ado)": "site:"+domain+" ext:action | ext:struts | ext:do",
    "# Linkedin employees (https://www.google.com/search?q=site%3Alinkedin.com+employees+"+domain+")": "site:linkedin.com employees "+domain+"",
    }

    for description, dork in dorks.items():
        print("\n" + description + "\n")
        if inputs.output:
            save(inputs.output, description)
        try:
            for results in search(dork, lang="en", user_agent=ua.random):
                print(results)

                # Randomize sleep time
                time.sleep(random.uniform(1, 15))  # Sleep for a random time between 1 and 5 seconds

                requ += 1
                if inputs.output:
                    save(inputs.output, results)

                # Randomize sleep time again
                time.sleep(random.uniform(1, 15))  # Sleep for a random time between 1 and 5 seconds

                if requ >= amount:
                    break
        except Exception as e:
            print(e)
            
        except KeyboardInterrupt:
            print("\nProcess interrupted by user.")
            sys.exit(0)

if __name__ == '__main__':
    main()
