import os

import constants

file_list = os.listdir(constants.dir_path)

for file in file_list:
    file_path = constants.dir_path + '/' + file
    waybill_list = []
    with open(file_path, 'r') as f:
        file_content = f.read()
        lines = file_content.split('\n')
        for line in lines:
            waybill_list.append(line)
    waybill_list = list(set(waybill_list))

    str = '\n'
    f = open(file_path, "w")
    f.write(str.join(waybill_list))
    f.close()
