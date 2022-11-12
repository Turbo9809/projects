from subprocess import run
import os
import sys

#调用命令行将fcd.xml转换成fcd.csv
def run_cmd( cmd_str='', echo_print=1):
    if echo_print == 1:
        print('\n执行cmd指令="{}"'.format(cmd_str))
    run(cmd_str, shell=True)
if __name__=="__main__":
    run_cmd('python D:/SUMO/sumo-win64-1.12.0/sumo-1.12.0/tools/xml/xml2csv.py test.tripinfo.xml --output test.tripinfo.csv')
    run_cmd('python D:/code/PaperCode/Tools/plot_trajectories.py fcd.xml -t td -o plot.png -s --filter-route  xye3,xye4,xye5,xywc0')
    os.system('python D:/code/PaperCode/Tools/plot_trajectories.py fcd.xml -t td -o plot.png -s --filter-route  xye3,xye4,xye5,xywc0')#217328056#0,217328056#2
print(sys.argv)