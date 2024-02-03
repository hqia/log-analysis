#coding:utf-8
'''
VS写的第一个Python程序
'''
again_tab = {'111':"0dB",'011':"-3dB",'001':"-9dB",'000':"-15dB"}
#将字符串数据转成32位的二进制形式
def str2bin(data_str):   
    data = bin(int(data_str,16)).split("0b")[1].zfill(32)
    # print(data)
    return data
#4通道模拟增益值
def show_AGain(again):
    # 4通道模拟增益显示值
    FL_AGain = again_tab.get(str2bin(again)[29:])
    FR_AGain = again_tab.get(str2bin(again)[25:28])
    RL_AGain = again_tab.get(str2bin(again)[21:24])
    RR_AGain = again_tab.get(str2bin(again)[17:20])
    print("Analog Gain")
    print("FL Channel:  %s"%FL_AGain + "\tFR Channel:  %s"%FR_AGain + "\tRL Channel:  %s"%RL_AGain + "\tRR Channel:  %s"%RR_AGain)  

#找到寄存器打印位置
def find_string_position(filename, target_string):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # 找到目标字符串所在行的索引
    target_index = -1
    for i, line in enumerate(lines):
        if target_string in line:
            target_index = i

    if target_index == -1:
        return None

    # 截取目标字符串所在行后面的15行
    start_index = target_index + 1
    end_index = min(start_index + 15, len(lines))
    new_lines = lines[start_index:end_index]
    print(new_lines)

    # 保存为新的文本文件
    with open('new.txt', 'w') as f:
        f.writelines(new_lines)

    # 判断元组元素是否在new文本中，并返回行号
    result = []
    for i, elem in enumerate(register_tab):
        found = False
        for j, line in enumerate(new_lines):
            if elem in line:
                result.append((elem, j))
                found = True
        if not found:
            result.append((elem, "Not Found"))
    return result

#利用寄存器打印位置从log中提取寄存器信息
def get_register_data(location_list):
    with open('new.txt', 'r') as f:
        lines = f.readlines()
    for register_name, location in location_list:
        if location == "Not Found":
            continue
        if register_name == register_tab[0]:
            ADC_CFG_PGA = lines[location].split("PGA:")[1].split(",6dB")[0]
            ADC_CFG_6dB_Boost = lines[location].split("st:")[1]
        elif register_name == register_tab[1]:
            DAC_CFG_AGain = lines[location].split("AGain:")[1].split(",DGain")[0]
            DAC_CFG_DGain = lines[location].split("DGain:")[1] 
        elif register_name == register_tab[2]:
            ADC_Bitwidth = lines[location].split("ADC = ")[1]
            DAC_Bitwidth = lines[location].split("DAC = ")[1].split(",ADC")[0] 
        elif register_name == register_tab[10]:
            DAA_COM1 = lines[location].split('\n')[0].split("\t1:")[1].split(",\t2:")[0]
            # DAC_Bitwidth = lines[2].split("DAC = ")[1].split(",ADC")[0]
        # elif register_name == register_tab[4]:
        #     ADC_CFG_6dB_Boost = lines[location].split("st:")[1]
        # elif register_name == register_tab[5]:
        #     ADC_CFG_6dB_Boost = lines[location].split("st:")[1]
        # elif register_name == register_tab[6]:
        #     ADC_CFG_6dB_Boost = lines[location].split("st:")[1]
        # elif register_name == register_tab[7]:
        #     ADC_CFG_6dB_Boost = lines[location].split("st:")[1]
        else: 
            pass
    show_AGain(DAA_COM1)


register_tab = ('ADC_CFG','DAC_CFG', 'BitWidth','JL_WL_AUD CON0','AUD_CON:','DAC_CON:','DAC_CON1:','ADC_CON:','ADC_CON1','DAC_TM0','DAA_CON','ADA_CON','ADDA_CON')
filename = 'log.txt'  # 替换成实际的文本文件路径
target_string = 'Audio_Config_Trace'  # 替换成实际的特定字符串

result = find_string_position(filename, target_string)
if result:
    for elem, line_number in result:
        if line_number == "Not Found":
            print(f'缺少 {elem} 相关信息')
        else:
            print(f'元素 {elem} 在新文本中的行号为: {line_number}')
else:
    print('目标字符串未找到')
print(result)
get_register_data(result)
