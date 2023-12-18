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

# 
def jl701n_audio_config(lists):
    ADC_Bitwidth = lists[0].split(",")[0].split("Width:")[1]
    ADC_DCC = lists[0].split("DCC:")[1]
    
    ADC_MAX_Gain = lists[1].split(")")[0].split("Max:")[1]
    ADC_Gain = lists[1].split("):")[1].split(",6dB")[0]
    ADC_6dB_Boost = lists[1].split("st:")[1].split(",")[0:4]
    
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
    ADA_CON1 = lists[12].split("\t1")[1].split("\t2")[0]
    ADA_CON2 = lists[12].split("\t2")[1].split("\t3")[0]
    ADA_CON3 = lists[12].split("\t3")[1].split("\t4")[0]
    ADA_CON4 = lists[12].split("\t4")[1].split("\t5")[0]
    ADA_CON5 = lists[12].split("\t5")[1].split("\t6")[0]
    ADA_CON6 = lists[12].split("\t6")[1].split("\t7")[0]
    ADA_CON7 = lists[12].split("\t7")[1].split("\t8")[0]
    ADA_CON8 = lists[12].split("\t8:")[1]
    
    print("ADC位宽=" + ADC_Bitwidth)
    print("ADC_DCC=" + ADC_DCC)
    print("ADC最大增益=" + ADC_MAX_Gain)
    print("DAC位宽=" + DAC_Bitwidth)
    print(DAC_Max_AGain)  
# 
#audio_config_print = {'JL701n':jl701n_audio_config(list_audio_configs),'ac703n':12,'JL703n':13,}

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
            print('第' + str(count) + '行')
            continue
        if audio_config_begin:
            if get_len == len_max:
                get_len = 0
                list_audio_configs.clear()
            list_audio_configs.append(line.split('\n')[0])
            get_len += 1
            if(get_len == len_max):
                audio_config_begin = False

# audio_config_print.get(string_version)
jl701n_audio_config(list_audio_configs)