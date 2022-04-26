import export_data
import requests,json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
proxies={
'http':'http://127.0.0.1:10809',
'https':'http://127.0.0.1:10809'
}

BASE_URL = r'https://alphafold.com/search/text/Arabidopsis%20thaliana?organismScientificName=Arabidopsis%20thaliana&page={}'
MAX_PAGE = 1375

GET_FUNCTION_URL = r"https://www.ebi.ac.uk/proteins/api/proteins/{}"

chr = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=options)
wait=WebDriverWait(chr,10)
# document.getElementsByClassName("medium-9")[0].getElementsByClassName("resultCard")
IS_OPEN_FIRST = True

def get_page_data(page):
    global IS_OPEN_FIRST
    if IS_OPEN_FIRST:
        chr.get(BASE_URL.format(page))
        IS_OPEN_FIRST = False
    else:
        js = "window.location.href = '{}'".format(BASE_URL.format(page))
        chr.execute_script(js)
    wait.until(lambda chr:chr.find_element_by_class_name("medium-9"))
    resultCards = chr.find_element_by_class_name("medium-9").find_elements_by_class_name("resultCard")
    items = []
    for rc in resultCards:
        row = {}
        # resultRow 
        a = rc.find_element_by_class_name("vf-link")
        url = a.get_attribute("href")
        row["Url"] = url
        # print("url= " + url)
        rrs = rc.find_elements_by_class_name("resultRow")
        for rr in rrs:
            divs = rr.find_elements_by_tag_name("div")
            # divs[0] - 标题
            rr_title = divs[0].text
            # divs[1] - 值
            rr_value = divs[1].text.replace("go to UniProt","").replace("search this organism","").replace("go to PDBe-KB","")
            # print("{} - {}".format(rr_title,rr_value))
            row[rr_title] = rr_value
        items.append(row)
    # for resItem in items:
        # url = resItem["Url"]
        # js = "window.location.href = '{}'".format(url)
        # chr.execute_script(js)
        # # print(url)
        # # time.sleep(5)
        # # document.getElementsByClassName("row entryInfoRow")[5].getElementsByTagName("div")[0].innerText
        # while True:
        #     try:
        #         wait.until(lambda chr:chr.find_elements_by_class_name("entryInfoRow"))
        #         break
        #     except: 
        #         print("no page!")
        #         chr.refresh()
        # for item in chr.find_elements_by_class_name("entryInfoRow"):
        #     el = item.find_elements_by_tag_name("div")
        #     if(el[0].text == "Biological function"):
        #         resItem['Biological function'] = el[1].text.replace("go to UniProt","")
        #         # print("bf - {}".format(el[1].text.replace("go to UniProt","")))


        # uni_prot = resItem['UniProt']
        # try:
        #     res = requests.get(GET_FUNCTION_URL.format(uni_prot),proxies=proxies)
        # except Exception as e:
        #     pass
        # obj = json.loads(res.text)
        # if "comments" in obj:
        #     for c in obj['comments']:
        #         if c['type'] == 'FUNCTION':
        #             resItem['Biological function'] = c['text'][0]['value']
        # print()
    return items
page_start = 1375
page_end = 1375
index = page_start
all_page_data = []
while(index <= page_end):
    try:
        res = get_page_data(index)
        print("第{}页完".format(index))
        all_page_data += res
    except:
        index += 1
        break
    index += 1
export_data.export_data(all_page_data,page_start,index - 1)
chr.quit()