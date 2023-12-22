#coding:utf-8
audio_flag = 'Audio_Config_Trace'
version_flag = '=Version='
count = 0       #已读行数
audio_config_begin = False        #开始获取音频配置标记
version_begin = False  
get_len = 0
list_audio_configs = []
string_version = '' 
audio_config_len = {'JL701n':13,'ac703n':12,'JL703n':13,}
again_tab = {'111':"0dB",'011':"-3dB",'001':"-9dB",'000':"-15dB"}
sample_rate_tab = {'0000':'96KHz','0001':'88.2KHz','0010':'64KHz','0011':'64KHz','0100':'48KHz','0101':'44.1KHz',
                    '0110':'32KHz','0111':'32KHz','1000':'24KHz','1001':'22.05KHz','1010':'16KHz','1011':'16KHz',
                    '1100':'12KHz','1101':'11.025KHz','1110':'8KHz','1111':'8KHz'}
PA_base_current_tab = {'000':'0u','001':'0.625u','010':'1.25u','011':'1.875u','100':'2.5u','101':'3.125u','110':'3.75u','111':'4.375u'}
vcm_voltage_tab = {'000':'LEVEL1\tVCM=1.2V','001':'LEVEL2\tVCM=1.3V','011':'LEVEL3\tVCM=1.4V','101':'LEVEL4\tVCM=1.5V','111':'LEVEL5\tVCM=1.6V'}
dacldo_voltage_tab = {'00':'LEVEL1\tDACLDO=2.4V','01':'LEVEL2\tDACLDO=2.6V','10':'LEVEL3\tDACLDO=2.8V','11':'LEVEL4\tDACLDO=3.0V'}

def jl701n_audio_config(lists):
    ADC_Bitwidth = lists[0].split(",")[0].split("Width:")[1]
    ADC_DCC = lists[0].split("DCC:")[1]   
    ADC_MAX_Gain = lists[1].split(")")[0].split("Max:")[1]
    ADC_Gain = lists[1].split("):")[1].split(",6dB")[0]
    ADC_6dB_Boost = lists[1].split("st:")[1]    
    DAC_Bitwidth = lists[2].split(",")[0].split("Width:")[1]
    DAC_DCC = lists[2].split("DCC:")[1]    
    DAC_Max_AGain = lists[3].split(")")[0].split("Max:")[1]
    DAC_AGain = lists[3].split("):")[1].split(",DGain")[0]
    DAC_Max_DGain = lists[3].split("DGain(Max:")[1].split("):")[0]
    DAC_DGain = lists[3].split("DGain(Max:")[1].split("):")[1]    
    JL_WL_AUD_CON0 = lists[4].split("CON0:")[1]   
    AUD_CON = lists[5].split("CON:")[1]   
    DAC_CON = lists[6].split("CON:")[1]    
    ADC_CON = lists[7].split("CON:")[1]   
    ADC_CON1 = lists[8].split("CON1:")[1]   
    DAC_VL0 = lists[9].split("VL0:")[1]    
    DAC_TM0 = lists[10].split("TM0:")[1]    
    DAA_CON0 = lists[11].split("CON 0:")[1].split(" ")[0]
    DAA_CON1 = lists[11].split("\t1:")[1].split(",\t2:")[0]
    DAA_CON2 = lists[11].split("\t2:")[1].split(",\t3")[0]
    DAA_CON3 = lists[11].split("\t3:")[1].split("    ")[0]
    DAA_CON7 = lists[11].split(" 7:")[1]   
    ADA_CON0 = lists[12].split("CON 0:")[1].split("\t1")[0]
    ADA_CON1 = lists[12].split("\t1:")[1].split("\t2")[0]
    ADA_CON2 = lists[12].split("\t2:")[1].split("\t3")[0]
    ADA_CON3 = lists[12].split("\t3:")[1].split("\t4")[0]
    ADA_CON4 = lists[12].split("\t4:")[1].split("\t5")[0]
    ADA_CON5 = lists[12].split("\t5:")[1].split("\t6")[0]
    ADA_CON6 = lists[12].split("\t6:")[1].split("\t7")[0]
    ADA_CON7 = lists[12].split("\t7:")[1].split("\t8")[0]
    ADA_CON8 = lists[12].split("\t8:")[1]
       
    print("ADC位宽=" + ADC_Bitwidth)
    print("ADC_DCC=" + ADC_DCC)
    print("ADC最大增益=" + ADC_MAX_Gain)
    print("DAC位宽=" + DAC_Bitwidth)
    print(DAC_Max_AGain)  
# 
def ac703n_audio_config(lists):
    ADC_CFG_PGA = lists[0].split("PGA:")[1].split(",6dB")[0]
    ADC_CFG_6dB_Boost = lists[0].split("st:")[1]    
    DAC_CFG_AGain = lists[1].split("AGain:")[1].split(",DGain")[0]
    DAC_CFG_DGain = lists[1].split("DGain:")[1] 
    ADC_Bitwidth = lists[2].split("ADC = ")[1]
    DAC_Bitwidth = lists[2].split("DAC = ")[1].split(",ADC")[0]  
    JL_WL_AUD_CON0 = lists[3].split("CON0:")[1]    
    AUD_CON = lists[4].split("CON:")[1]   
    DAC_CON = lists[5].split("CON:")[1]    
    ADC_CON = lists[6].split("CON:")[1]    
    ADC_CON1 = lists[7].split("CON1:")[1]   
    DAC_TM0 = lists[8].split("TM0:")[1]    
    DAA_CON0 = lists[9].split("CON 0:")[1].split(" ")[0]
    DAA_CON1 = lists[9].split("\t1:")[1].split(",\t2:")[0]   
    DAA_CON2 = lists[9].split("\t2:")[1].split(",\t3")[0]
    DAA_CON3 = lists[9].split("\t3:")[1].split("    ")[0]
    # DAA_CON4 = lists[9].split("    4:")[1].split(",7:")[0]
    DAA_CON7 = lists[9].split(",7:")[1]    
    ADA_CON0 = lists[10].split("CON 0:")[1].split("\t1")[0]
    ADA_CON1 = lists[10].split("\t1:")[1].split("\t2")[0]
    ADA_CON2 = lists[10].split("\t2:")[1].split("\t3")[0]
    ADA_CON3 = lists[10].split("\t3:")[1].split("\t4")[0]
    ADA_CON4 = lists[10].split("\t4:")[1].split("\t5")[0]
    ADA_CON5 = lists[10].split("\t5:")[1].split("  6:")[0]
    ADA_CON6 = lists[10].split("  6:")[1].split(" 7:")[0]
    ADA_CON7 = lists[10].split(" 7:")[1].split(" 8:")[0] 
    ADA_CON8 = lists[10].split(" 8:")[1]   
    ADDA_CON0 = lists[11].split("CON 0:")[1].split("\t1:")[0]
    ADDA_CON1 = lists[11].split("\t1:")[1]
    
    
    str2bin(JL_WL_AUD_CON0)
    str2bin(AUD_CON)
    str2bin(DAC_CON)
    str2bin(ADC_CON)
    str2bin(ADC_CON1)
    str2bin(DAC_TM0)
    str2bin(DAA_CON0)
    str2bin(DAA_CON1)
    str2bin(DAA_CON2)
    str2bin(DAA_CON3)
    # str2bin(DAA_CON4)
    str2bin(DAA_CON7)
    str2bin(ADA_CON0)
    str2bin(ADA_CON1)
    str2bin(ADA_CON2)
    str2bin(ADA_CON3)
    str2bin(ADA_CON4)
    str2bin(ADA_CON5)
    str2bin(ADA_CON6)
    str2bin(ADA_CON7)
    str2bin(ADA_CON8)
    str2bin(ADDA_CON0)
    str2bin(ADDA_CON1)
    
    # print("============ac703n=============")
    # show_AGain(DAA_CON1)
    # show_sample_rate(DAC_CON)
    # show_dac_performance_mode(DAA_CON0,DAA_CON3)
    # show_power_level(ADDA_CON0,DAA_CON0)
    # print("ADC位宽=" + ADC_Bitwidth)
    # print("DAC位宽=" + DAC_Bitwidth)
    
#

def str2bin(data_str):
    data = bin(int(data_str,16)).split("0b")[1].zfill(32)
    print(data)
    return data

def show_power_level(register1,register2):
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
    
    
def show_dac_performance_mode(register1,register2):
    bin_register1 = str2bin(register1)
    bin_register2 = str2bin(register2)
    # PA_base_current = PA_base_current_tab.get(bin_register1[5:8])
    # PABUF_base_current = PA_base_current_tab.get(bin_register2[0:3])
    # print("PA偏置电流：%s"%PA_base_current + "\tPABUF偏置电流：%s"%PABUF_base_current)
    PA = int(bin_register1[5:8],2)
    PABUF = int(bin_register2[0:3],2)
    if (PA > 0b100)&(PABUF > 0b100):
        print("性能模式：\t高性能模式")
    else:
        print("性能模式：\t低功耗模式")
    
    

def show_sample_rate(register):
    a = str2bin(register)
    print(a)
    global_sample_rate = sample_rate_tab.get(str2bin(register)[28:])
    print("全局采样率:\t%s"%global_sample_rate)

def show_AGain(again):
    # 4通道模拟增益显示值
    FL_AGain = again_tab.get(str2bin(again)[29:])
    FR_AGain = again_tab.get(str2bin(again)[25:28])
    RL_AGain = again_tab.get(str2bin(again)[21:24])
    RR_AGain = again_tab.get(str2bin(again)[17:20])
    print("Analog Gain")
    print("FL Channel:  %s"%FL_AGain + "\tFR Channel:  %s"%FR_AGain + "\tRL Channel:  %s"%RL_AGain + "\tRR Channel:  %s"%RR_AGain)    
  
def get_config(chip_version):
    if '701' in chip_version:
        jl701n_audio_config(list_audio_configs)
        return
    elif '703' in chip_version:
        ac703n_audio_config(list_audio_configs)
        return
    else:
        print("目前还不知道%s的配置信息"%chip_version)
    

with open('log.txt','r')as f:
    lines = f.readlines()
    for line in lines:
        count += 1
        if version_flag in line:
            version_begin = True
            continue
        if version_begin:
            string_version = line.split("]")[1].split("_V")[0]
            len_max = audio_config_len.get(string_version)
            version_begin = False
        if audio_flag in line:
            audio_config_begin = True       
            # print('第' + str(count) + '行')
            continue
        if audio_config_begin:
            if get_len >= len_max:
                get_len = 0
                list_audio_configs.clear()
            list_audio_configs.append(line.split('\n')[0])
            
            get_len += 1
            if(get_len == len_max):
                audio_config_begin = False


get_config(string_version)
# input("")