import sys
import traci
import os

# 确保 traci 在系统环境变量中
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    print('SUMO_HOME is In Environment!')
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

    
class Sim(object):
    def __init__(self, sumo_config, GUI=False):
        self.sumo_config = sumo_config # sumo config 文件
        self.launch_env_flag = False
        self.GUI = GUI
    def launchEnv(self):
        """开始模拟(通过traci来获得其中数据)
        """
        if self.GUI:
            sumo_gui = 'D:/APPs/src/sumo-win64-1.12.0/sumo-1.12.0/bin/sumo-gui'
        else:
            sumo_gui = 'D:/APPs/src/sumo-win64-1.12.0/sumo-1.12.0/bin/sumo'
        traci.start([
            sumo_gui,
            "-c", self.sumo_config,
            "--no-warnings",
            "--seed", "2"])
        self.launch_env_flag = True
        # sys.path.append("D:/APPs/src/sumo-win64-1.12.0/sumo-1.12.0/tools") 
        # sumoBinary = "D:/APPs/src/sumo-win64-1.12.0/sumo-1.12.0/bin/sumo-gui"
        # sumo_file = [sumoBinary, "-c", "D:/code/PaperCode/XiangyunRoad_JiulongRoad/test.sumocfg"]
        # traci.start(sumo_file)
        # self.launch_env_flag = True
    def close(self):
        """关闭实验环境
        """
        traci.close()
        self.launch_env_flag = False
        sys.stdout.flush()
    def reset(self):
        """关闭当前环境, 并开启一个新的环境
        """
        self.close()
        self.launchEnv()
    def step(self):
        steps = 0
        assert self.launch_env_flag
        while traci.simulation.getMinExpectedNumber() > 0: # 当路网里面还有车
        # while steps < 3000:
            traci.simulationStep()
            steps += 1
    def runSim(self):
        """开始模拟
        """
        self.launchEnv()  # 初始化环境
        self.step()  # 进行模拟
        self.close()  # 关闭环境
if __name__ == '__main__':
    sumo_sim = Sim(sumo_config='D:/code/PaperCode/XiangyunRoad_JiulongRoad/test.sumocfg')
    sumo_sim.runSim()

