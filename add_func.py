import requests,json,time
import load_data
proxies={
'http':'http://127.0.0.1:10809',
'https':'http://127.0.0.1:10809'
}
def save_excel(row_num):
    out_path = "out/add_out_{}_{}.xlsx".format(row_num,str(time.time()* 1000))
    work_book.save(out_path)

GET_FUNCTION_URL = r"https://www.ebi.ac.uk/proteins/api/proteins/{}"
data_dir = "out/out_1_1375_1650870453239.1196.xlsx"

start_row = 1
index = 1
firstLine = True
rows,work_book = load_data.load_data(data_dir)
print("data loaded!")
try:
    for row in rows:
        if firstLine:
            firstLine = False
            continue
        if index < start_row:
            continue
        uni_prot = str(row[2].value)
        try:
            res = requests.get(GET_FUNCTION_URL.format(uni_prot),proxies=proxies)
        except Exception as e:
            pass
        obj = json.loads(res.text)
        if "comments" in obj:
            for c in obj['comments']:
                if c['type'] == 'FUNCTION':
                    row[4].value = c['text'][0]['value']
        print(str(index) + " ok!")
        if index > 200 and index % 200 == 0: 
            save_excel(index)
        index += 1
except Exception as e:
    print(str(e))
save_excel(index-1)