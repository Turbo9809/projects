import traci
import openpyxl
import xml.etree.ElementTree as ET
import csv
import os, sys
import pandas as pd
import numpy as np
# from SumoSimulation import Sim
# sumo_sim = Sim(sumo_config='D:/code/PaperCode/XiangyunRoad_JiulongRoad/test.sumocfg')
# sumo_sim.launchEnv() # 开启仿真

#配置调用路径
sys.path.append("D:/APPs/src/sumo-win64-1.12.0/sumo-1.12.0/tools") 
sumoBinary = "D:/APPs/src/sumo-win64-1.12.0/sumo-1.12.0/bin/sumo-gui"
sumo_file = [sumoBinary, "-c", "D:/code/PaperCode/XiangyunRoad_JiulongRoad/test.sumocfg"]

 
#仿真开始
traci.start(sumo_file)
x_k = []
steps = 0
while steps < 3000:
        traci.simulationStep()
        steps += 1
        ###########################  SFM  ###########################
        '''x(k+1) = x(k) + T[q(k) - s(k) + d(k) + u(k)]''' 

        T = 100 # T为采样时间

        ## 定义x(k)
        
        x_k.append(traci.edge.getLastStepVehicleNumber('xye5'))
        # num_nVehSeen = []
        # tree = ET.parse('D:/code/PaperCode/XiangyunRoad_JiulongRoad/e2output.xml')
        # root = tree.getroot()

        # for i in range(len(root)):
        #         num_nVehSeen.append(int(root[i].attrib['nVehSeen']))
        # x_k = sum(num_nVehSeen)
        # print(x_k)


        # 创建文件
        f = open('D:/code/PaperCode/Datas/SFM_Data1.csv', 'w', newline = "")

        # 写入对象
        csv_write = csv.writer(f)

        # 构建列表头
        csv_write.writerow(['nVehContrib_x_k'])

        # 写入csv文件
        for veh_step in range(len(x_k)):
            csv_write.writerow([int(x_k[veh_step])])


