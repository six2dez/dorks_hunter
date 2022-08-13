#!/usr/bin/env/python3
import sys
import time
import tldextract
import argparse
from googlesearch import search

def parseArgs():
    message = "Simple Google dork search"
    parser = argparse.ArgumentParser(description=message)
    parser.add_argument('--domain', '-d', required=True, help='Domain to scan')
    parser.add_argument('--results', '-r', help='Number of results per search, default 10', type=int)
    parser.add_argument('--output', '-o', help='Output file')
    parser.parse_args()
    args = parser.parse_args()
    return args

def save(file,data):
    file = open((file), "a")
    file.write(str(data))
    file.write("\n")
    file.close()

def main():
    inputs = parseArgs()
    if bool(inputs.results):
        amount = inputs.results
    else:
        amount = 10
    requ = 0
    counter = 0
    domain = inputs.domain
    target = tldextract.extract(str(domain)).domain

    dorks = {
    "# .git folders (https://www.google.com/search?q=inurl%3A%5C%22%2F.git%5C%22%20"+domain+"%20-github)": "inurl:\"/.git\" "+domain+" -github",
    "# Backup files (https://www.google.com/search?q=site%3A"+domain+"%20ext%3Abkf%20%7C%20ext%3Abkp%20%7C%20ext%3Abak%20%7C%20ext%3Aold%20%7C%20ext%3Abackup)": "site:"+domain+" ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup",
    "# Exposed documents (https://www.google.com/search?q=site%3A"+domain+"%20ext%3Adoc%20%7C%20ext%3Adocx%20%7C%20ext%3Aodt%20%7C%20ext%3Apdf%20%7C%20ext%3Artf%20%7C%20ext%3Asxw%20%7C%20ext%3Apsw%20%7C%20ext%3Appt%20%7C%20ext%3Apptx%20%7C%20ext%3Apps%20%7C%20ext%3Acsv)": "site:"+domain+" ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv",
    "# Confidential documents (https://www.google.com/search?q=inurl%3A"+target+"+not+for+distribution+%7C+confidential+%7C+%22employee+only%22+%7C+proprietary+%7C+top+secret+%7C+classified+%7C+trade+secret+%7C+internal+%7C+private+filetype%3Axls+OR+filetype%3Acsv+OR+filetype%3Adoc+OR+filetype%3Apdf)": "inurl:"+target+" not for distribution | confidential | \"employee only\" | proprietary | top secret | classified | trade secret | internal | private filetype:xls OR filetype:csv OR filetype:doc OR filetype:pdf",
    "# Config files (https://www.google.com/search?q=site%3A"+domain+"%20ext%3Axml%20%7C%20ext%3Aconf%20%7C%20ext%3Acnf%20%7C%20ext%3Areg%20%7C%20ext%3Ainf%20%7C%20ext%3Ardp%20%7C%20ext%3Acfg%20%7C%20ext%3Atxt%20%7C%20ext%3Aora%20%7C%20ext%3Aenv%20%7C%20ext%3Aini)": "site:"+domain+" ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:env | ext:ini",
    "# Database files (https://www.google.com/search?q=site%3A"+domain+"%20ext%3Asql%20%7C%20ext%3Adbf%20%7C%20ext%3Amdb)": "site:"+domain+" ext:sql | ext:dbf | ext:mdb",
    "# Other files (https://www.google.com/search?q=site%3A"+domain+"%20intitle%3Aindex.of%20%7C%20ext%3Alog%20%7C%20ext%3Aphp%20intitle%3Aphpinfo%20%5C%22published%20by%20the%20PHP%20Group%5C%22%20%7C%20inurl%3Ashell%20%7C%20inurl%3Abackdoor%20%7C%20inurl%3Awso%20%7C%20inurl%3Acmd%20%7C%20shadow%20%7C%20passwd%20%7C%20boot.ini%20%7C%20inurl%3Abackdoor%20%7C%20inurl%3Areadme%20%7C%20inurl%3Alicense%20%7C%20inurl%3Ainstall%20%7C%20inurl%3Asetup%20%7C%20inurl%3Aconfig%20%7C%20inurl%3A%5C%22%2Fphpinfo.php%5C%22%20%7C%20inurl%3A%5C%22.htaccess%5C%22%20%7C%20ext%3Aswf)": "site:"+domain+" intitle:index.of | ext:log | ext:php intitle:phpinfo \"published by the PHP Group\" | inurl:shell | inurl:backdoor | inurl:wso | inurl:cmd | shadow | passwd | boot.ini | inurl:backdoor | inurl:readme | inurl:license | inurl:install | inurl:setup | inurl:config | inurl:\"/phpinfo.php\" | inurl:\".htaccess\" | ext:swf",
    "# SQL errors (https://www.google.com/search?q=site%3A"+domain+"%20intext%3A%5C%22sql%20syntax%20near%5C%22%20%7C%20intext%3A%5C%22syntax%20error%20has%20occurred%5C%22%20%7C%20intext%3A%5C%22incorrect%20syntax%20near%5C%22%20%7C%20intext%3A%5C%22unexpected%20end%20of%20SQL%20command%5C%22%20%7C%20intext%3A%5C%22Warning%3A%20mysql_connect()%5C%22%20%7C%20intext%3A%5C%22Warning%3A%20mysql_query()%5C%22%20%7C%20intext%3A%5C%22Warning%3A%20pg_connect()%5C%22)": "site:"+domain+" intext:\"sql syntax near\" | intext:\"syntax error has occurred\" | intext:\"incorrect syntax near\" | intext:\"unexpected end of SQL command\" | intext:\"Warning: mysql_connect()\" | intext:\"Warning: mysql_query()\" | intext:\"Warning: pg_connect()\"",
    "# PHP errors (https://www.google.com/search?q=site%3A"+domain+"%20%5C%22PHP%20Parse%20error%5C%22%20%7C%20%5C%22PHP%20Warning%5C%22%20%7C%20%5C%22PHP%20Error%5C%22)": "site:"+domain+" \"PHP Parse error\" | \"PHP Warning\" | \"PHP Error\"",
    "# Wordpress files (https://www.google.com/search?q=site%3A"+domain+"%20inurl%3Awp-content%20%7C%20inurl%3Awp-includes)": "site:"+domain+" inurl:wp-content | inurl:wp-includes",
    "# Project management sites (https://www.google.com/search?q=site%3Atrello.com%20%7C%20site%3A*.atlassian.net%20%22"+target+"%22)": "site:trello.com | site:*.atlassian.net \""+target+"\"",
    "# Subdomains (https://www.google.com/search?q=site%3A*."+domain+")": "site:*."+domain+"",
    "# Sub-subdomains (https://www.google.com/search?q=site%3A*.*."+domain+")": "site:*.*."+domain+"",
    "# GitLab/GitHub/Bitbucket (https://www.google.com/search?q=site%3Agithub.com%20%7C%20site%3Agitlab.com%20%7C%20site%3Abitbucket.org%20%22"+target+"%22)": "site:github.com | site:gitlab.com | site:bitbucket.org \""+target+"\"",
    "# Cloud buckets S3/GCP (https://www.google.com/search?q=site%3A.s3.amazonaws.com%20%7C%20site%3Astorage.googleapis.com%20%7C%20site%3Aamazonaws.com%20%22"+target+"%22)": "site:.s3.amazonaws.com | site:storage.googleapis.com | site:amazonaws.com \""+target+"\"",
    "# Traefik (https://www.google.com/search?q=intitle%3Atraefik%20inurl%3A8080%2Fdashboard%20%22"+target+"%22)": "intitle:traefik inurl:8080/dashboard \""+target+"\"",
    "# Jenkins (https://www.google.com/search?q=intitle%3A%5C%22Dashboard%20%5BJenkins%5D%5C%22%20%22"+target+"%22)": "intitle:\"Dashboard [Jenkins]\" \""+target+"\"",
    "# Login pages (https://www.google.com/search?q=site%3A"+domain+"%20inurl%3Asignup%20%7C%20inurl%3Aregister%20%7C%20intitle%3ASignup)": "site:"+domain+" inurl:signup | inurl:register | intitle:Signup",
    "# Open redirects (https://www.google.com/search?q=site%3A"+domain+"%20inurl%3Aredir%20%7C%20inurl%3Aurl%20%7C%20inurl%3Aredirect%20%7C%20inurl%3Areturn%20%7C%20inurl%3Asrc%3Dhttp%20%7C%20inurl%3Ar%3Dhttp)": "site:"+domain+" inurl:redir | inurl:url | inurl:redirect | inurl:return | inurl:src=http | inurl:r=http",
    "# Code share sites (https://www.google.com/search?q=site%3Asharecode.io%20%7C%20site%3Acontrolc.com%20%7C%20site%3Acodepad.co%20%7Csite%3Aideone.com%20%7C%20site%3Acodebeautify.org%20%7C%20site%3Ajsdelivr.com%20%7C%20site%3Acodeshare.io%20%7C%20site%3Acodepen.io%20%7C%20site%3Arepl.it%20%7C%20site%3Ajsfiddle.net%20%22"+target+"%22)": "site:sharecode.io | site:controlc.com | site:codepad.co |site:ideone.com | site:codebeautify.org | site:jsdelivr.com | site:codeshare.io | site:codepen.io | site:repl.it | site:jsfiddle.net \""+target+"\"",
    "# Other 3rd parties sites (https://www.google.com/search?q=site%3Agitter.im%20%7C%20site%3Apapaly.com%20%7C%20site%3Aproductforums.google.com%20%7C%20site%3Acoggle.it%20%7C%20site%3Areplt.it%20%7C%20site%3Aycombinator.com%20%7C%20site%3Alibraries.io%20%7C%20site%3Anpm.runkit.com%20%7C%20site%3Anpmjs.com%20%7C%20site%3Ascribd.com%20%22"+target+"%22)": "site:gitter.im | site:papaly.com | site:productforums.google.com | site:coggle.it | site:replt.it | site:ycombinator.com | site:libraries.io | site:npm.runkit.com | site:npmjs.com | site:scribd.com \""+target+"\"",
    "# Stackoverflow (https://www.google.com/search?q=site%3Astackoverflow.com%20%22"+domain+"%22)": "site:stackoverflow.com \""+domain+"\"",
    "# Pastebin-like sites (https://www.google.com/search?q=site%3Ajustpaste.it%20%7C%20site%3Aheypasteit.com%20%7C%20site%3Apastebin.com%20%22"+target+"%22)": "site:justpaste.it | site:heypasteit.com | site:pastebin.com \""+target+"\"",
    "# Apache Struts RCE (https://www.google.com/search?q=site%3A"+domain+"%20ext%3Aaction%20%7C%20ext%3Astruts%20%7C%20ext%3Ado)": "site:"+domain+" ext:action | ext:struts | ext:do",
    "# Linkedin employees (https://www.google.com/search?q=site%3Alinkedin.com%20employees%20"+domain+")": "site:linkedin.com employees "+domain+"",
    }

    for description, dork in dorks.items():
        print ("\n"+description+"\n")
        if bool(inputs.output):
            save(inputs.output,description)
        try:
            for results in search(dork, tld="com", lang="en", num=int(amount), start=0, stop=None, pause=2):
                print (results)
                time.sleep(0.1)
                requ += 1
                if bool(inputs.output):
                    save(inputs.output,results)
                time.sleep(0.1)
                if requ >= int(amount):
                    break
        except Exception as e:
            print(e)
if __name__ == '__main__':
    main()
