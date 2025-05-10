import pandas as pd

def filter_and_sample_essays(input_file, output_file, essay_sets, sample_size=200):
    """
    从输入文件中筛选特定essay_set的行，随机抽取指定数量，并写入输出文件
    
    参数:
    input_file (str): 输入CSV文件路径
    output_file (str): 输出CSV文件路径
    essay_sets (list): 要筛选的essay_set列表
    sample_size (int): 要抽取的样本数量
    """
    try:
        # 读取CSV文件
        df = pd.read_csv(input_file, sep='\t', encoding='utf-8', on_bad_lines='skip')
        
        # 筛选特定essay_set的行
        filtered_df = df[df['essay_set'].isin(essay_sets)]
        
        # 检查筛选后的行数是否足够
        if len(filtered_df) < sample_size:
            print(f"警告: 筛选后只有{len(filtered_df)}行，少于请求的{sample_size}行。")
            print(f"将使用所有{len(filtered_df)}行。")
            sampled_df = filtered_df
        else:
            # 随机抽取样本
            sampled_df = filtered_df.sample(n=sample_size, random_state=42)
        
        # 按essay id从小到大排序
        sampled_df = sampled_df.sort_values(by='essay_id')
        # 写入新的CSV文件
        sampled_df.to_csv(output_file, sep='\t', index=False)
        
        print(f"成功从{len(filtered_df)}行中抽取{len(sampled_df)}行，并写入 {output_file}")
        
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    # 设置输入和输出文件路径
    size = 50 # 样本量
    input_file = "../data/training_set_rel3.csv"  
    output_file = f"../data/random_essays_{size}.csv" 
    
    # 设置要筛选的essay_set
    essay_sets = [1, 2, 7, 8]
    
    # 执行筛选和抽样
    filter_and_sample_essays(input_file, output_file, essay_sets, size)