import operator
import os
import chardet


# 单文件夹下
def get_file():
    filename = [x for x in os.listdir('.')
                if os.path.isfile(x) and (os.path.splitext(x)[1] == '.txt' or os.path.splitext(x)[1] == '.TXT')]
    return filename


# 遍历文件夹下及子文件夹下的所有txt
def get_all_file(file_path):
    txt_files = []
    if file_path == None:
        file_path = '.'
    for dirpath, dirnames, filenames in os.walk(file_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if os.path.isfile(full_path) and (
                    os.path.splitext(full_path)[1] == '.txt' or os.path.splitext(full_path)[1] == '.TXT'):
                txt_files.append({"path": dirpath, "name": filename})

    return txt_files


def trans(filename):
    if operator.contains(filename, "new_"):
        return
    command = 'iconv -c -f GB2312 -t UTF-8 ' + filename + ' >> ' + filename
    p = os.popen(command)
    p.close()
    os.remove(filename)
    print(' [-]成功转换文件>' + filename)


def trans_file(file):
    full_path = os.path.join(file['path'], file['name'])
    if operator.contains(full_path, "new_"):
        return
    new_name = os.path.join(file['path'], 'new_' + file['name']);
    command = 'iconv -c -f GB2312 -t UTF-8 "' + full_path + '" >> "' + new_name + '"'
    p = os.popen(command)
    p.close()
    os.remove(full_path)
    print(' [-]成功转换文件>' + full_path)


# 判断编码
def detect_code(path):
    with open(path, 'rb') as file:
        data = file.read(2000)  # 最多2000个字符
        dicts = chardet.detect(data)
    return dicts


print("[+] 正在侦测操作系统类型...")
file_path = '/Users/kent/books/文学汇总/txt-books/transfer'
if os.name == 'posix':
    file_list = get_all_file('/Users/kent/books/文学汇总/txt-books/transfer')
    for i in file_list:
        code = detect_code(i['path'] + '/' + i['name'])
        if code['encoding'] == 'utf-8':
            print('utf-8编码，无需转换')
            continue
        trans_file(i)
    print("[*] 已完全转换")

else:
    print('抱歉，本脚本暂不支持windows系统...')
