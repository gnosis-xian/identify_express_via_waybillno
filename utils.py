
def parse_waybillno(waybillno):
    if waybillno is None or waybillno == '':
        return ''
    length = len(waybillno)
    s_len = '%02d' % length
    return "{}{}".format(s_len, waybillno)

def participles(waybillno):
    lists = []
    lists.append(waybillno[0:4])
    lists.append(waybillno[0:5])
    lists.append(waybillno[0:6])
    lists.append(waybillno[0:7])
    lists.append(waybillno[0:8])
    return lists

def is_blank(str):
    return str == '' or str is None

def not_blank(str):
    return not is_blank(str)

if __name__ == '__main__':
    waybillno = "781357"
    print(parse_waybillno(waybillno))