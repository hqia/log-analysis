#coding:utf-8
# Audio_Config_len = {"701":13,"703":12}
# try:
#     chip_model = input("What is the chip model?\n")
#     print(Audio_Config_len[chip_model])
# except EOFError:
#     #print(Audio_Config_len[chip_model])
#     pass
Audio_flag = 'Audio_Config_Trace'
with open('log.txt','r')as f:
    count = 0       #已读行数
    Target = 0      #发现目标数
    flag = False        #开始获取配置标记
    get_len = 0
    list_Audio_Config = [] 
    lines = f.readlines()
    for line in lines:
        count += 1
        if Audio_flag in line:
            flag = True
            get_len = 0        
            Target += 1
            print('第' + str(count) + '行')
            continue
        if (flag):
            list_Audio_Config.append(line.split('\n')[0])
            get_len += 1
            # result = line.split(",")[0]
            # print(result)
            # print(ADC_Bitwidth)
            if(get_len == 13):
                flag = False
    ADC_Bitwidth = list_Audio_Config[0].split(",")[0].split("Width:")[1]
    ADC_DCC = list_Audio_Config[0].split("DCC:")[1]
    print("ADC位宽=" + ADC_Bitwidth)
    print("ADC_DCC=" + ADC_DCC)
    
    ADC_MAX_Gain = list_Audio_Config[1].split(")")[0].split("Max:")[1]
    ADC_Gain = list_Audio_Config[1].split("):")[1].split(",6dB")[0]
    ADC_6dB_Boost = list_Audio_Config[1].split("st:")[1]
    print("ADC最大增益=" + ADC_MAX_Gain)
    DAC_Bitwidth = list_Audio_Config[2].split(",")[0].split("Width:")[1]
    print("DAC位宽=" + DAC_Bitwidth)
    DAC_Max_AGain = list_Audio_Config[3].split(")")[0].split("Max:")[1]
    print(DAC_Max_AGain)
    # print(list_Audio_Config[1])
        # if (get_len == Audio_Config_len[chip_model]):
            # flag = False
            
        
        