# This is a sample Python script.
import json
import xlsxwriter

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
filePath = '一号标.har'
requestUrl = 'http://www.fjhyyb.cn/Ocean863Web_MAIN/AjaxHandler/OceanObservation.ashx'
translation = {'YXLG': '有效浪高', 'ZDLG': '最大浪高', 'PJFS': '平均风速', 'ZDFS': '最大风速'}


def string_to_float(st):
    if st == 'null':
        return st
    return float(st)


def time_revise(timestr):
    revised_list = timestr.split(',')
    revised_list[1] = str(int(revised_list[1]) + 1)
    return ','.join(revised_list)


def generate_xlsx(text_type, lists, workbook):
    result_strings = ''
    text_type_list = []
    for item in lists:
        url_strings = item['request']['url']
        if url_strings == requestUrl:
            text_type_list = item['request']['postData']['params']
            if len(text_type_list) >= 4 and text_type_list[3]['value'] == text_type:
                result_strings = item['response']['content']['text']
                break
    result_list = eval(result_strings)
    if text_type == 'YXLG' or text_type == 'PJFS':
        data_list = [result_list[0]["data"][0]["data"], result_list[0]["data"][1]["data"]]
    else:
        data_list = [result_list[0]["data"][0]["data"]]
    for no, list_item in enumerate(data_list):
        worksheet = workbook.add_worksheet(filePath[:-4] + translation.get(text_type_list[3 + no]['value'], 'unset'))
        for n, data in enumerate(list_item):
            time_start = 10
            time_end = data[0].index(')')
            value_start = time_end + 2
            value_end = -1
            worksheet.write('A' + str(n + 1), n)
            worksheet.write('B' + str(n + 1), time_revise(data[0][time_start:time_end]))
            worksheet.write('C' + str(n + 1), string_to_float(data[0][value_start:value_end]))
        print(f'generate sheet"{translation.get(text_type_list[3 + no]["value"], "unset")}" successfully')


def data_processing():
    print('==================================start==================================\n')
    with open(filePath, 'r', encoding='utf-8') as readObj:
        har_dict = json.loads(readObj.read())
        request_list = har_dict['log']['entries']
        request_list.reverse()
    workbook = xlsxwriter.Workbook(filePath[:-4] + '.xlsx')
    print('please wait')
    generate_xlsx("YXLG", request_list, workbook)
    generate_xlsx("PJFS", request_list, workbook)
    workbook.close()
    print('\n===================================end===================================')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data_processing()