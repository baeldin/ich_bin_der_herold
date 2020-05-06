# -*- coding: utf-8 -*-
import urllib2
import csv
from time import sleep
import re
from HTMLParser import HTMLParser
import codecs

# PROXY shit
# proxy = urllib2.ProxyHandler({
#     'http': '54.37.21.29:8811',
#     'https': '54.37.21.29:8811'})
# opener = urllib2.build_opener(proxy)
# urllib2.install_opener(opener)
# print(urllib2)
# res = urllib2.urlopen('https://www.whatsmyip.org/')
# print(res)
# print(res.read())
# exit()

htmlparser = HTMLParser()

def make_url(word):
    # Word = unicode(word)
    # print type(Word)    
    url_Word = urllib2.quote(word, "utf-8")
    # print "\ntype = %s \n" %type(Word)
    print "url_word = %s \n" %url_Word
    return url_Word


def get_entry_url_list(source):
    string_list = source.split('"')
    k = 2
    url_list = []
    for str in string_list:
        if "data-detail-url" in str:
            k = 0
        if k == 1:
            url_list.append(str)
        k += 1
    return(url_list)


def open_url(url):
    # take URL string and return website source code
    res = urllib2.urlopen(url)
    return res.read()


def get_town(source_string):
    string_list = re.split("[<>]", source_string)
    k = 2
    zip_list = []
    for stri in string_list:
        if stri == 'span itemprop="addressRegion"':
            k = 0
        if k == 1:
            return stri
        k += 1


def get_zip(source_string):
    string_list = re.split("[<>]", source_string)
    k = 2
    zip_list = []
    for stri in string_list:
        if stri == 'span itemprop="postalCode"':
            k = 0
        if k == 1:
            return stri
        k += 1


def get_names(source_string):
    string_list = re.split("[<>]", source_string)
    k = 2
    name_list = []
    for stri in string_list:
        if stri == 'span itemprop="name"':
            k = 0
        if k == 1:
            name_list.append(stri)
        k += 1
    return(name_list[3:])


def get_mail(source_string):
    string_list = source_string.split('"')
    for stri in string_list:
        if 'mailto:' in stri:
            if 'herold' not in stri:
                return stri.split(':')[1]


def main():
    npages = 9
    csvfile = open('hotels_niederösterreich0.csv','w')
    wr = csv.writer(csvfile, delimiter=',')
    wr.writerow(['name','PLZ','Ort','E-mail'])
    # ä %C3%A4
    # ö %C3%B6
    # ü %C3%BC
    for pp in range(1,14):
    # for pp in range(14,npages+1):
        url_string = "https://www.herold.at/gelbe-seiten/nieder%C3%B6sterreich/was_hotel/?page="+str(pp)
        source_string = open_url(url_string)
        url_list = get_entry_url_list(source_string)
        name_list = get_names(source_string)
        zip_list = get_zip(source_string)
        for entry, name in zip(url_list, name_list):
            source_string = open_url(entry)
            mail = get_mail(source_string)
            zip_code = get_zip(source_string)
            town = get_town(source_string)
            if mail is None:
                print("omitting "+name+", no mail found")
            else:
                print(name,zip_code,town,mail)
                # print("got: "+name+" "+zip_code+" "+town+" "+mail)
                wr.writerow([name, zip_code, town, mail])
            sleep(1)


if __name__ == "__main__":
    main()
