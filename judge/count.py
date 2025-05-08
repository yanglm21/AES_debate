import os

def count_a_b_in_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        count_a = content.count('A')
        count_b = content.count('B')
        return count_a, count_b

def count_a_b_in_directory(directory):
    total_a = 0
    total_b = 0
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            count_a, count_b = count_a_b_in_file(file_path)
            total_a += count_a
            total_b += count_b
    print(f"总计 A 的数量: {total_a}, B 的数量: {total_b}")

# 替换为你的txt文件所在的目录路径
directory_path = '/Users/ylm/THU/code/exp/data/win/rubric_vs_baseline'
count_a_b_in_directory(directory_path)