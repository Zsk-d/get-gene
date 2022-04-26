from openpyxl import load_workbook

def load_data(path):
    # res = []
    # firstLine = True
    work_book = load_workbook(path)

    sheet = work_book.worksheets[0]
    rows = sheet.rows
    # for row in rows:
    #     if firstLine:
    #         firstLine = False
    #         continue
    #     res.append({
    #         "isbn":str(row[0].value),
    #         "price":float(row[1].value),
    #         "name":row[2].value,
    #         "cnp":row[3].value,
    #         "auth":row[4].value,
    #         "datetime":row[5].value,
    #         "stock_count":row[6].value,
    #         "stock_no":row[7].value
    #     })
    return rows,work_book