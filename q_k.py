import xml.etree.ElementTree as ET
import csv

tree1 = ET.parse('D:/code/PaperCode/XiangyunRoad_JiulongRoad/e1output.xml')   ##放置路由文件的路径
root1 = tree1.getroot()

# 创建文件
f = open('D:/code/PaperCode/Datas/SFM_Data.csv', 'w', newline = "")

# 写入对象
csv_write = csv.writer(f)

# 构建列表头
csv_write.writerow(['nVehContrib_q_k'])

# 写入csv文件
for e in range(len(root1)):
    if root1[e].attrib['id'] in ['e1det_xye3_0', 'e1det_xye3_1','e1det_xye3_2','e1det_xye3_3','e1det_xye3_4',]:
        csv_write.writerow([int(root1[e].attrib['nVehContrib'])])
        

