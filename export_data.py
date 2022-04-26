import openpyxl,time,os

def export_data(res,page_start,page_end):
    wb = openpyxl.Workbook()
    sheet = wb.create_sheet(title="result", index=0)
    header = ["Protein","Gene","UniProt","PDBe-KB","Biological function","Url"]
    
    sheet.append(header)
    for item in res:
        for h in header:
            if h not in item:
                item[h] = ''
        sheet.append(
            [item['Protein'],
            item['Gene'],
            item['UniProt'],
            item['PDBe-KB'],
            item['Biological function'],
            item['Url'],
        ])
    out_path = "out/out_{}_{}_{}.xlsx".format(page_start,page_end,str(time.time()* 1000))
    wb.save(out_path)
    openFilePath = 'explorer /e,/select,{}'.format(os.path.abspath(out_path))
    os.popen(openFilePath)
    return os.path.abspath(out_path)