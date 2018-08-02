import requests
from bs4 import BeautifulSoup
import re
from  multiprocessing import Pool
from multiprocessing import cpu_count

url_list = [];


#from a url -> get the time of the film
def from_html_page_get_time(url_film_page):
        a = 0
        source  = requests.get(url_film_page).text
        soup = BeautifulSoup(source,'lxml')
        str_match = str(soup)
        a = str_match.find('text-link text-footer">', 20000)
        a = a + len('text-link text-footer">')
        try:
            return int(''.join(map(str,re.findall('\d*\.?\d+',str_match[a:a+10]))))
        except:
            return 0                  #for film without time

#from https://letterboxd.com/USER/films/page/cnt get all the film
def fill_url_list_(url_table_page):
    a = 0
    b = 0
    url_ltbxd = "https://letterboxd.com/film/"
    helpstring = ""
    source  = requests.get(url_table_page).text
    soup = BeautifulSoup(source,'lxml')
    str_match = str(soup)
    #print(len(str_match))
    #print(str_match)
    while(a <= len(str_match) and b < 72 and str_match.find('data-film-slug="/film/', a) != -1):             #72 film in the table
        a = str_match.find('data-film-slug="/film/', a)
        a=a+len('data-film-slug="/film/')
        helpstring = url_ltbxd
        while str_match[a] != '/':
            helpstring=helpstring+str_match[a]
            a=a+1
        #print(helpstring)
        url_list.append(helpstring)
        helpstring=""
        b = b+1

def login_process():
    print("Hi letterboxd User, i will calculate all the time you have sepend watching film ")
    URL = 'https://letterboxd.com'
    USER = input('Insert Your User-Name: ')

    cnt = 1;
    r  = requests.get((URL+"/"+USER+ "/films/page/" + str(cnt) + "/"))
    soup = BeautifulSoup(r.text, 'lxml')
    str_match = str(soup)

    while str_match.find('poster-container') != -1 :
        cnt=cnt + 1
        r  = requests.get(URL+"/"+USER+ "/films/page/" + str(cnt) + "/")
        soup = BeautifulSoup(r.text, 'lxml')
        str_match = str(soup)


    #print("You have watched  " + str(cnt) + " page of film ")

    for i in range(1,cnt):
        st = str( (URL+"/"+USER+ "/films/page/" + str(i) + "/"))
        print("Scanning page  " + st)
        #print(st)
        fill_url_list_(st)
        i=i+1

    print("You have watched " + str(len(url_list)) + " movies ")





if __name__ == '__main__':
    login_process()
    pool = Pool(cpu_count())
    fat_list = pool.map(func=from_html_page_get_time, iterable=url_list)
    pool.close()
    pool.join()
    print("You have watched ", sum(fat_list) / 60 , " hours of film in total ")
