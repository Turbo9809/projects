import traci
import openpyxl
import xml.etree.ElementTree as ET
import csv
import os, sys
# from SumoSimulation import Sim
# sumo_sim = Sim(sumo_config='D:/code/PaperCode/XiangyunRoad_JiulongRoad/test.sumocfg')  
# sumo_sim.launchEnv() # 开启仿真

#配置调用路径
sys.path.append("D:/APPs/src/sumo-win64-1.12.0/sumo-1.12.0/tools") 
sumoBinary = "D:/APPs/src/sumo-win64-1.12.0/sumo-1.12.0/bin/sumo-gui"
sumo_file = [sumoBinary, "-c", "D:/code/PaperCode/XiangyunRoad_JiulongRoad/test.sumocfg"]

 
#仿真开始
traci.start(sumo_file)
steps = 0
num_nVehContrib = []
while steps < 300:
        traci.simulationStep()
        steps += 1

        class u_k():
            def cycle_time(tls_id):
                tls_logic = traci.trafficlight.getAllProgramLogics(tls_id)  #获取下一信号交叉口的控制方案
                current_phase = tls_logic[0].currentPhaseIndex  #获取信号相位
                cycle_time = 0  #周期时长初始化
                for i in  range(len(tls_logic[0].phases)):
                        cycle_time += tls_logic[0].phases[i].duration  #将控制方案中各相位的控制方案累加获得周期长
                return cycle_time

            def incoming_lane(tls_id):
                logic = traci.trafficlight.getAllProgramLogics(tls_id)#获取控制方案
                in_lane = traci.trafficlight.getControlledLanes(tls_id)
                program = logic[0]
                phase = {}#定义空相位
                for i in range(len(program.phases)):#遍历信号相位
                    phase[i] = program.phases[i].state#信号为logic格式，.state是其中的具体信号控制方案
                incoming_lanes_all = {}#定义进口车道集
                for i in phase:#遍历相位
                    incoming_lanes = []#定义进口空车道
                    k = 0#控制相位数
                    #print(phase[i])
                    for j in phase[i]:
                        if j =='G':#将‘G’对应的车道记录下来
                            #print(k)
                            k += 1
                            incoming_lanes.append(in_lane[k])
                            #print(incoming_lanes)
                        # k += 1
                    incoming_lanes_all[i] = incoming_lanes#将每一相位的车道保存
                    # print('incoming lanes: ', incoming_lanes_all)
                    # print('incoming 1 :', incoming_lanes_all[0])
                    # print('incoming 11: ', incoming_lanes_all[0][0])

                    for east_lane in incoming_lanes_all[i]:
                        print('1111111111', east_lane)#ID字母拆分incoming_lanes_all[i][0]


                        east_lane_all = ['xye5_0', 'xye5_1', 'xye5_2', 'xye5_3', 'xye5_4',]
                        if east_lane in east_lane_all:
                            print('right！！')
                            # num_nVehContrib = []
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

                # 1.创建文件对象
                f = open('D:/code/PaperCode/Datas/csv_file.csv', 'w', newline = "")
                
                # 2.构建csv写入对象
                csv_write = csv.writer(f)
                
                # 3.构建列表头
                csv_write.writerow(['nVehContrib'])
                
                # 4.写入csv文件
                for data in range(len(num_nVehContrib)):
                    print('数据据据：', int(num_nVehContrib[data]))
                    csv_write.writerow([int(num_nVehContrib[data])])
            
                # 5.关闭文件
                f.close()

            write_datas(num_nVehContrib)
            print("写入成功")

traci.close() # 关闭仿真