import re

def modify_text(input_file_path, output_file_path):

    f = open(input_file_path, 'r', encoding='utf-8')
    content = f.read()
    f.close()

    modified_content = content.replace('[name="', '').replace('"] ', ' : ')
    modified_content = re.sub(r'\[.*?\]', '', modified_content)

    f = open(output_file_path, 'w', encoding='utf-8')
    f.write(modified_content)
    f.close()

input_file_path = 'D:\\GitHub\\ArknightsGameData_YoStar\\ja_JP\\gamedata\\story\\activities\\act11d0\\'
output_file_path = 'D:\\GitHub\\AnimeGPT\\Scripts\\JP\\'

file_names = ['level_act11d0_01_beg.txt', 'level_act11d0_01_end.txt','level_act11d0_02_beg.txt', 'level_act11d0_02_end.txt',
              'level_act11d0_03_beg.txt', 'level_act11d0_03_end.txt','level_act11d0_04_beg.txt', 'level_act11d0_04_end.txt',
              'level_act11d0_05_beg.txt', 'level_act11d0_05_end.txt','level_act11d0_06_beg.txt', 'level_act11d0_06_end.txt',
              'level_act11d0_07_beg.txt', 'level_act11d0_07_end.txt','level_act11d0_08_beg.txt', 'level_act11d0_08_end.txt',
              'level_act11d0_st01.txt', 'level_act11d0_st02.txt', 'level_act11d0_sub-1-1_end.txt', 'level_act11d0_sub-1-2_end.txt'
              ]

for file_name in file_names:
    print(output_file_path + file_name)
    modify_text(input_file_path + file_name, output_file_path + file_name)