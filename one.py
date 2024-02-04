#coding:utf-8
again_tab = {'111':"0dB",'011':"-3dB",'001':"-9dB",'000':"-15dB"}
sample_rate_tab = {'0000':'96KHz','0001':'88.2KHz','0010':'64KHz','0011':'64KHz','0100':'48KHz','0101':'44.1KHz',
                    '0110':'32KHz','0111':'32KHz','1000':'24KHz','1001':'22.05KHz','1010':'16KHz','1011':'16KHz',
                    '1100':'12KHz','1101':'11.025KHz','1110':'8KHz','1111':'8KHz'}
PA_base_current_tab = {'000':'0u','001':'0.625u','010':'1.25u','011':'1.875u','100':'2.5u','101':'3.125u','110':'3.75u','111':'4.375u'}
vcm_voltage_tab = {'000':'LEVEL1\tVCM=1.2V','001':'LEVEL2\tVCM=1.3V','011':'LEVEL3\tVCM=1.4V','101':'LEVEL4\tVCM=1.5V','111':'LEVEL5\tVCM=1.6V'}
dacldo_voltage_tab = {'00':'LEVEL1\tDACLDO=2.4V','01':'LEVEL2\tDACLDO=2.6V','10':'LEVEL3\tDACLDO=2.8V','11':'LEVEL4\tDACLDO=3.0V'}
register_tab = ('ADC_CFG','DAC_CFG', 'BitWidth','JL_WL_AUD CON0','AUD_CON:','DAC_CON:','DAC_CON1:',
                'ADC_CON:','ADC_CON1','DAC_TM0','DAA_CON','ADA_CON','ADDA_CON','-@')
filename = 'log.txt'  # 替换成实际的文本文件路径
target_audio_string = 'Audio_Config_Trace'  # 替换成实际的特定字符串
target_version_string = '=Version='

#将字符串数据转成32位的二进制形式
def str2bin(data_str):   
    data = bin(int(data_str,16)).split("0b")[1].zfill(32)
    # print(data)
    return data

#打印SDK版本号
def show_version(sdk_version):
    print("芯片型号_SDK版本号: \t"+ sdk_version)

#判断DAC输出方式
def show_dac_out_mode(register1):
    dac_out_mode = ['差分输出','单端输出','None']
    mode = 0
    if register1 == None:
        mode = 2
    else:
        bin_register1 = str2bin(register1)
        if bin_register1[2] == '1':
            mdoe = 0
        else:
            mode = 1
    print(f'DAC输出方式: {dac_out_mode[mode]} ')
#电源档位信息
def show_power_level(register1,register2):
    if (register1 == None) | (register2 == None) :
        print("没有获取到音频供电档位")
    else:
        bin_register1 = str2bin(register1)
        bin_register2 = str2bin(register2)    
        if bin_register1[0] == '1':
            print("VCM 有 外挂电容")
            vcm_voltage = vcm_voltage_tab.get(bin_register1[1:4])
            print("音频供电档位：\t" + vcm_voltage)
        else:
            print("VCM 无 外挂电容")
            dacldo_voltage = dacldo_voltage_tab.get(bin_register2[25:27])
            print("音频供电档位：\t" + dacldo_voltage)

#dac性能模式        
def show_dac_performance_mode(register1,register2):
    if (register1 == None) | (register2 == None) :
        print("没有获取到dac性能模式相关信息")
    else:
        bin_register1 = str2bin(register1)
        bin_register2 = str2bin(register2)
        PA_base_current = PA_base_current_tab.get(bin_register1[5:8])
        PABUF_base_current = PA_base_current_tab.get(bin_register2[0:3])
        print("PA偏置电流:%s"%PA_base_current + "\t\tPABUF偏置电流:%s"%PABUF_base_current)
        PA = int(bin_register1[5:8],2)
        PABUF = int(bin_register2[0:3],2)
        if (PA > 0b100)&(PABUF > 0b100):
            print("性能模式：\t高性能模式")
        else:
            print("性能模式：\t低功耗模式")
    
#采样率
def show_sample_rate(register):
    if register == None:
        global_sample_rate = 'None'
    else:
        # a = str2bin(register)
        # print(a)
        global_sample_rate = sample_rate_tab.get(str2bin(register)[28:])
    print("全局采样率:\t%s"%global_sample_rate)

#4通道模拟增益值
def show_AGain(register):
    if register == None:
        print("没有获取到模拟增益相关信息")
    else:
        # 4通道模拟增益显示值
        FL_AGain = again_tab.get(str2bin(register)[29:])
        FR_AGain = again_tab.get(str2bin(register)[25:28])
        RL_AGain = again_tab.get(str2bin(register)[21:24])
        RR_AGain = again_tab.get(str2bin(register)[17:20])
        print("Analog Gain")
        print("FL Channel:  %s"%FL_AGain + "\tFR Channel:  %s"%FR_AGain + "\tRL Channel:  %s"%RL_AGain + "\tRR Channel:  %s"%RR_AGain)  

#DAC、ADC位宽显示
def show_dac_adc_Bitwidth(register1,register2):
    if register1 == None:
        print("没有DAC位宽信息")
    else:
        print("ADC位宽=" + register1)
    if register2 == None:
        print("没有ADC位宽信息")
    else:
        print("DAC位宽=" + register2)

#显示所有配置信息
def show_config(config_data_dict):
    show_version(config_data_dict['version'])
    show_AGain(config_data_dict['DAA_CON1'])
    show_sample_rate(config_data_dict['DAC_CON'])
    show_dac_performance_mode(config_data_dict['DAA_CON0'],config_data_dict['DAA_CON3'])
    show_power_level(config_data_dict['ADDA_CON0'],config_data_dict['DAA_CON0'])
    show_dac_adc_Bitwidth(config_data_dict['DAC_Bitwidth'],config_data_dict['ADC_Bitwidth'])
    show_dac_out_mode(config_data_dict['DAC_CON1'])

#找到寄存器打印位置
def find_string_position(filename,target_version_string,target_audio_string):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # 找到目标字符串所在行的索引
    target_version_index = -1
    target_audio_index = -1
    for i, line in enumerate(lines):
        if target_version_string in line:
            target_version_index = i
        if target_audio_string in line:
            target_audio_index = i

    if target_version_index == -1:
        return None
    if target_audio_index == -1:
        return None
    version_lines = lines[target_version_index + 1:target_version_index + 2]
    # 截取目标字符串所在行后面的15行
    start_index = target_audio_index + 1
    end_index = min(start_index + 15, len(lines))
    audio_lines = lines[start_index:end_index]
    new_lines = version_lines + audio_lines
    print(new_lines)

    # 保存为新的文本文件
    with open('config.txt', 'w') as f:
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

#利用寄存器打印位置从log中提取寄存器数据
def get_register_data(location_list):
    register_name_tab = ('ADC_CFG_PGA','ADC_CFG_6dB_Boost','DAC_CFG_AGain','DAC_CFG_DGain','ADC_Bitwidth',
                 'DAC_Bitwidth','JL_WL_AUD_CON0','AUD_CON','DAC_CON','DAC_CON1','ADC_CON','ADC_CON1','DAC_TM0',
                 'DAA_CON0','DAA_CON1','DAA_CON2','DAA_CON3','DAA_CON4','DAA_CON7','ADA_CON0','ADA_CON1',
                 'ADA_CON2','ADA_CON3','ADA_CON4','ADA_CON5','ADA_CON6','ADA_CON7','ADA_CON8','ADDA_CON0','ADDA_CON1','version')
    register_data_dict = dict.fromkeys(register_name_tab,None)
    with open('config.txt', 'r') as f:
        lines = f.readlines()
    for register_name, location in location_list:
        if location == "Not Found":
            continue
        if register_name == register_tab[13]:
            register_data_dict['version'] = lines[location].split('\n')[0].split("]")[1]
        if register_name == register_tab[0]:
            register_data_dict['ADC_CFG_PGA'] = lines[location].split('\n')[0].split("PGA:")[1].split(",6dB")[0]
            register_data_dict['ADC_CFG_6dB_Boost'] = lines[location].split('\n')[0].split("st:")[1]
        elif register_name == register_tab[1]:
            register_data_dict['DAC_CFG_AGain'] = lines[location].split('\n')[0].split("AGain:")[1].split(",DGain")[0]
            register_data_dict['DAC_CFG_DGain'] = lines[location].split('\n')[0].split("DGain:")[1] 
        elif register_name == register_tab[2]:
            register_data_dict['ADC_Bitwidth'] = lines[location].split('\n')[0].split("ADC = ")[1]
            register_data_dict['DAC_Bitwidth'] = lines[location].split('\n')[0].split("DAC = ")[1].split(",ADC")[0] 
        elif register_name == register_tab[3]:
            register_data_dict['JL_WL_AUD_CON0'] = lines[location].split('\n')[0].split("CON0:")[1]
        elif register_name == register_tab[4]:
            register_data_dict['AUD_CON'] = lines[location].split('\n')[0].split("CON:")[1]
        elif register_name == register_tab[5]:
            register_data_dict['DAC_CON'] = lines[location].split('\n')[0].split("CON:")[1]
        elif register_name == register_tab[6]:
            register_data_dict['DAC_CON1'] = lines[location].split('\n')[0].split("CON1:")[1]
        elif register_name == register_tab[7]:
            register_data_dict['ADC_CON'] = lines[location].split('\n')[0].split("CON:")[1]
        elif register_name == register_tab[8]:
            register_data_dict['ADC_CON1'] = lines[location].split('\n')[0].split("CON1:")[1]
        elif register_name == register_tab[9]:
            register_data_dict['DAC_TM0'] = lines[location].split('\n')[0].split("TM0:")[1]
        elif register_name == register_tab[10]:
            register_data_dict['DAA_CON0'] = lines[location].split('\n')[0].split("CON 0:")[1].split(" ")[0]
            register_data_dict['DAA_CON1'] = lines[location].split('\n')[0].split("\t1:")[1].split(",\t2:")[0]
            register_data_dict['DAA_CON2'] = lines[location].split('\n')[0].split("\t2:")[1].split(",\t3")[0]
            register_data_dict['DAA_CON3'] = lines[location].split('\n')[0].split("\t3:")[1].split("    ")[0]
            register_data_dict['DAA_CON4'] = lines[location].split('\n')[0].split("    4:")[1].split(",7:")[0]
            register_data_dict['DAA_CON7'] = lines[location].split('\n')[0].split(",7:")[1]
        elif register_name == register_tab[11]:
            register_data_dict['ADA_CON0'] = lines[location].split('\n')[0].split("CON 0:")[1].split("\t1")[0]
            register_data_dict['ADA_CON1'] = lines[location].split('\n')[0].split("\t1:")[1].split("\t2")[0]
            register_data_dict['ADA_CON2'] = lines[location].split('\n')[0].split("\t2:")[1].split("\t3")[0]
            register_data_dict['ADA_CON3'] = lines[location].split('\n')[0].split("\t3:")[1].split("\t4")[0]
            register_data_dict['ADA_CON4'] = lines[location].split('\n')[0].split("\t4:")[1].split("\t5")[0]
            register_data_dict['ADA_CON5'] = lines[location].split('\n')[0].split("\t5:")[1].split("  6:")[0]
            register_data_dict['ADA_CON6'] = lines[location].split('\n')[0].split("  6:")[1].split(" 7:")[0]
            register_data_dict['ADA_CON7'] = lines[location].split('\n')[0].split(" 7:")[1].split(" 8:")[0] 
            register_data_dict['ADA_CON8'] = lines[location].split('\n')[0].split(" 8:")[1]
        elif register_name == register_tab[12]:
            register_data_dict['ADDA_CON0'] = lines[location].split('\n')[0].split("CON 0:")[1].split("\t1:")[0]
            register_data_dict['ADDA_CON1'] = lines[location].split('\n')[0].split("\t1:")[1]
        else: 
            # print('err')
            pass
    return register_data_dict

result = find_string_position(filename, target_version_string, target_audio_string)
if result:
    for elem, line_number in result:
        if line_number == "Not Found":
            print(f'缺少 {elem} 相关信息')
        else:
            print(f'元素 {elem} 在config.txt中的行号为: {line_number}')
else:
    print('请打开DAC寄存器打印')
register_name_data = get_register_data(result)
show_config(register_name_data)
