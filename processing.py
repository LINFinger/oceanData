import json
import xlsxwriter

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
    return_strings = ''
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
        worksheet = workbook.add_worksheet(translation.get(text_type_list[3 + no]['value'], 'unset'))
        for n, data in enumerate(list_item):
            time_start = 10
            time_end = data[0].index(')')
            value_start = time_end + 2
            value_end = -1
            worksheet.write('A' + str(n + 1), n)
            worksheet.write('B' + str(n + 1), time_revise(data[0][time_start:time_end]))
            worksheet.write('C' + str(n + 1), string_to_float(data[0][value_start:value_end]))
        strings = f'generate sheet"{translation.get(text_type_list[3 + no]["value"], "unset")}" successfully'
        print(strings)
        return_strings += (strings + '\n')
    return return_strings


class OceanData:

    def __init__(self, filepath, filetype):
        self.file_path = filepath
        self.file_type = filetype
        self.file_name = filepath.split('/')[-1]
        self.output = ''

    def dataProcessing(self):
        self.output = ''
        print('==================================start==================================\n')
        with open(self.file_path, 'r', encoding='utf-8') as readObj:
            har_dict = json.loads(readObj.read())
            request_list = har_dict['log']['entries']
            request_list.reverse()
        workbook = xlsxwriter.Workbook(self.file_path[:-4] + '.' + self.file_type)
        print('please wait')
        self.output += generate_xlsx("YXLG", request_list, workbook)
        self.output += generate_xlsx("PJFS", request_list, workbook)
        workbook.close()
        print('\n===================================end===================================')

    def getOutput(self):
        return self.output

