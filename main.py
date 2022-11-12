import random
import traci
import numpy as np
import xml.etree.ElementTree as ET
import sumolib
from SumoSimulation import Sim
import csv
import sys

#配置调用路径
sys.path.append("D:/APPs/src/sumo-win64-1.12.0/sumo-1.12.0/tools") 
sumoBinary = "D:/APPs/src/sumo-win64-1.12.0/sumo-1.12.0/bin/sumo-gui"
sumo_file = [sumoBinary, "-c", "D:/code/PaperCode/XiangyunRoad_JiulongRoad/test.sumocfg"]

#仿真开始
traci.start(sumo_file)

steps = 0
x_k = []
x = np.zeros(2)
num_nVehContrib = []
T = 1 # T为采样时间

for k in range(3000):
    while steps < 3000:
            traci.simulationStep()
            steps += 1
            ###########################  SFM  ###########################
            '''x(k+1) = x(k) + T[q(k) - s(k) + d(k) + u(k)]''' 

            
            ### 定义 x(k) ###
            x_k.append(traci.edge.getLastStepVehicleNumber('xye5'))
            x_k.append(traci.edge.getLastStepVehicleNumber('xye4'))

            f_xk = open('D:/code/PaperCode/Datas/SFM_Data1.csv', 'w', newline = "")
            csv_write = csv.writer(f_xk)
            csv_write.writerow(['nVehContrib_x_k'])

            # 写入x_k数据
            for veh_step in range(len(x_k)):
                csv_write.writerow([int(x_k[veh_step])])
        
            ### 定义 q(k) ###
            tree1 = ET.parse('D:/code/PaperCode/XiangyunRoad_JiulongRoad/e1output.xml')   #放置路由文件的路径
            root1 = tree1.getroot()

            f_qk = open('D:/code/PaperCode/Datas/SFM_Data.csv', 'w', newline = "")
            csv_write = csv.writer(f_qk)
            csv_write.writerow(['nVehContrib_q_k'])

            # 写入q_k数据
            for e in range(len(root1)):
                    if root1[e].attrib['id'] in ['e1det_xye3_0', 'e1det_xye3_1','e1det_xye3_2','e1det_xye3_3','e1det_xye3_4',]:
                        q_k = int(root1[e].attrib['nVehContrib'])
                        csv_write.writerow([q_k])

            ### 定义 s(k) ###
            s_k =  random.sample(range(0,10),3000)  

            ### 定义 d(k) ###
            d_k = random.sample(range(0,10),3000)

            ### 定义u(k) ###
            class u_k():
                def cycle_time(tls_id):
                    tls_logic = traci.trafficlight.getAllProgramLogics(tls_id)  #获取下一信号交叉口的控制方案
                    current_phase = tls_logic[0].currentPhaseIndex  #获取信号相位
                    cycle_time = 0  #周期时长初始化
                    for i in  range(len(tls_logic[0].phases)):
                            cycle_time += tls_logic[0].phases[i].duration  #将控制方案中各相位的控制方案累加获得周期长
                    return cycle_time

                def incoming_lane(tls_id):
                    logic = traci.trafficlight.getAllProgramLogics(tls_id)  #获取控制方案
                    in_lane = traci.trafficlight.getControlledLanes(tls_id)
                    program = logic[0]
                    phase = {}  #定义空相位
                    for i in range(len(program.phases)):     #遍历信号相位
                        phase[i] = program.phases[i].state   #信号为logic格式，.state是其中的具体信号控制方案
                    incoming_lanes_all = {}  #定义进口车道集
                    for i in phase:   #遍历相位
                        incoming_lanes = []   #定义进口空车道
                        p = 0   #控制相位数
                        #print(phase[i])
                        for j in phase[i]:
                            if j =='G':   #将‘G’对应的车道记录下来
                                #print(k)
                                p += 1
                                incoming_lanes.append(in_lane[p])
                                #print(incoming_lanes)
                            # k += 1
                        incoming_lanes_all[i] = incoming_lanes    #将每一相位的车道保存

                        for east_lane in incoming_lanes_all[i]:
                            east_lane_all = ['xye5_0', 'xye5_1', 'xye5_2', 'xye5_3', 'xye5_4',]
                            if east_lane in east_lane_all:
                                print('right!!')
                                tree = ET.parse('D:/code/PaperCode/XiangyunRoad_JiulongRoad/e1output.xml')
                                root = tree.getroot()
                                # print('tree: ', tree)
                                # print('root: ', root)
                                for num_veh in range(len(root)):
                                    num_nVehContrib.append(int(root[num_veh].attrib['nVehContrib']))
                                    print('数据：', num_nVehContrib)
                                    # print('u_k =', traci.lane.getLastStepVehicleNumber())#改：E1检测器输出某车道流量
                    return num_nVehContrib
                incoming_lane('cluster_4539962409_8796741377_cluster_4539962407_4539962408_4539962410_4539962411_4539962412_4539962413')
                print('数据据：', num_nVehContrib)

                def write_datas(num_nVehContrib):

                    f_uk = open('D:/code/PaperCode/Datas/csv_file.csv', 'w', newline = "")
                    csv_write = csv.writer(f_uk)
                    csv_write.writerow(['nVehContrib'])
                    
                    # 写入u(k)数据
                    for data in range(len(num_nVehContrib)):
                        print('数据据据：', int(num_nVehContrib[data]))
                        csv_write.writerow([int(num_nVehContrib[data])])

                write_datas(num_nVehContrib)
                print("写入成功")

    x[k+1]= x_k + T*(q_k - s_k + d_k + u_k())
        
    traci.close() # 关闭仿真
