import os

def count_a_b_c_in_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        count_a = content.count('A')
        count_b = content.count('B')
        count_c = content.count('C')
        return count_a, count_b, count_c

def count_a_b_c_in_directory(directory):
    total_a = 0
    total_b = 0
    total_c = 0
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            count_a, count_b, count_c = count_a_b_c_in_file(file_path)
            total_a += count_a
            total_b += count_b
            total_c += count_c
    print(f"总计 A 的数量: {total_a}, B 的数量: {total_b}, C 的数量: {total_c}")

# 替换为你的txt文件所在的目录路径
directory_path = '/Users/ylm/THU/code/AES_debate/output/ivypanda/win'
count_a_b_c_in_directory(directory_path)