#Song Gao, Mingxiao Li, Jinmeng Rao, Gengchen Mai, Timothy Prestby, Joseph Marks, Yingjie Hu. (2020) Automatic Urban Road Map Generation from Massive GPS Trajectories of Taxis. In Martin Werner, Yao-Yi Chiang et al.(Eds): Handbook of Big Geospatial Data, Springer.
#Gengchen Mai, Krzysztof Janowicz, Yingjie Hu, Song Gao. (2018) ADCN: An Anisotropic Density-Based Clustering Algorithm for Discovering Spatial Point Patterns with Noise. Transactions in GIS, 22(2018), 348-369.

import numpy as np
import matplotlib.pyplot as plt
import random
import shapefile
import math
from scipy.spatial import KDTree
    
class visitlist:
    def __init__(self, count):
        self.unvisitedlist=[i for i in range(count)]
        self.visitedlist=list()
        self.unvisitednum=count

    def visit(self, pointId):
        self.visitedlist.append(pointId)
        self.unvisitedlist.remove(pointId)
        self.unvisitednum -= 1

class SDE:
    def __init__(self,mainpt, a,b,angle):
        self.a=a
        self.b=b
        self.angle = angle
        self.mainpt =mainpt

def dis_two_point(pi,pj):
    dis=((pi[0]-pj[0])**2+(pi[1]-pj[1])**2)**0.5
    return dis

def calculate_SDE(ptindex_array, eps):
    pt_array = dataset[ptindex_array]
    center_pt = pt_array.mean(axis=0)
    pt_trans = pt_array - center_pt
    tempA = np.square(pt_trans)
    A = sum(tempA[:,0])-sum(tempA[:,1])
    C = 2*sum(pt_trans[:,0]*pt_trans[:,1])
    B = (A**2+C**2)**0.5

    if (C == 0):
        if (-A + B ==0):
            angle = 0
        else:
            angle = math.pi / 2
    else:
        angle = math.atan((-A+B)/C)

    a_ori = math.sqrt(sum(np.square(pt_trans[:,1]*math.sin(angle)+pt_trans[:,0]*math.cos(angle)))/len(pt_array))
    b_ori = math.sqrt(sum(np.square(pt_trans[:,1]*math.cos(angle)-pt_trans[:,0]*math.sin(angle)))/len(pt_array))

    if a_ori*b_ori==0:
        if a_ori > b_ori:
            a_final = float('inf')
            b_final = 0
        else:
            b_final = float('inf')
            a_final = 0
    else:
        trans_indicator = math.sqrt(eps**2/(a_ori*b_ori))
        if a_ori>b_ori:
            a_final = a_ori*trans_indicator
            b_final = b_ori*trans_indicator
        else:
            b_final = a_ori*trans_indicator
            a_final = b_ori*trans_indicator

    result = SDE(center_pt,a_final,b_final,angle)
    return result

def if_point_in_SDE(pt,SDE):
    [xj, yj] = pt
    [xi, yi] = SDE.mainpt
    if SDE.b==0:
        if (yj-yi)*math.cos(SDE.angle)-(xj-xi)*math.sin(SDE.angle)==0:
            return 'in'
        else:
            return 'out'
    elif dis_two_point(pt,SDE.mainpt)>SDE.a:
        return 'out'
    elif dis_two_point(pt,SDE.mainpt)<=SDE.b:
        return 'in'
    else:
        temp = (((yj-yi)*math.sin(SDE.angle)+(xj-xi)*math.cos(SDE.angle))**2/SDE.a**2)+(((yj-yi)*math.cos(SDE.angle)-(xj-xi)*math.sin(SDE.angle))**2/SDE.b**2)
        if temp<=1:
            return 'in'
        else:
            return 'out'

def Pts_in_SDE(pts_index,SDE):
    in_list=[]
    for ptindex in pts_index:
        pt = dataset[ptindex]
        tag=if_point_in_SDE(pt,SDE)
        if tag=='in':
            in_list.append(ptindex)
    return in_list

def adcn(dataSet, eps, minPts):
    nPoints = dataSet.shape[0]
    vPoints = visitlist(nPoints)
    k = -1
    C = [-1 for i in range(nPoints)]
    kd = KDTree(dataset)
    while(vPoints.unvisitednum>0):
        print(vPoints.unvisitednum)
        p = random.choice(vPoints.unvisitedlist)
        vPoints.visit(p)
        N_index = kd.query(dataset[p],k=minPts)[1]
        SDEN = calculate_SDE(N_index,eps)
        May_in_SDEN_ptlist=kd.query_ball_point(dataset[p],SDEN.a)
        pts_in_SDEN = Pts_in_SDE(May_in_SDEN_ptlist,SDEN)

        if len(pts_in_SDEN) >= minPts:
            k += 1
            C[p] = k
            for p1 in pts_in_SDEN:
                if p1 in vPoints.unvisitedlist:
                    vPoints.visit(p1)
                    M_index = kd.query(dataset[p1],k=minPts)[1]
                    SDEM = calculate_SDE(M_index,eps)
                    May_in_SDEM_ptlist=kd.query_ball_point(dataset[p1],SDEM.a)
                    pts_in_SDEM = Pts_in_SDE(May_in_SDEM_ptlist,SDEM)
                    if len(pts_in_SDEM) >= minPts:
                        for i in pts_in_SDEM:
                            if i not in pts_in_SDEN:
                                pts_in_SDEN.append(i)
                    if C[p1] == -1:
                        C[p1] = k
        else:
            C[p1] = -1
    #plt.scatter(dataset[:, 0], dataset[:, 1], c=C, marker='.')
    #plt.show()
    return C

def generate_data(path):
    fw = open(path,'r')
    pt_array=[]
    for line in fw:
        pt = [float(line.split(',')[3]), float(line.split(',')[4])]
        pt_array.append(pt)

    pt_array=np.array(pt_array)
    #plt.figure(figsize=(12, 9), dpi=80)
    #plt.scatter(pt_array[:, 0], pt_array[:, 1], marker='.')
    #plt.show()
    return pt_array

def Draw_shapefile(path):
    sf = shapefile.Writer(path,shapeType=1)
    sf.autoBalance = 1
    sf.field('CID', 'N')

    for i in range(len(dataset)):
        pt = dataset[i]
        cid = typelist[i]
        sf.point(pt[0],pt[1])
        sf.record(cid)
    sf.close()



if __name__ == '__main__':
    #point path && final shapefile path
    path = 'bridge_pt.txt'
    write_path = 'Cluster_result.shp'
    
    #read data
    dataset = generate_data(path)
    
    #ADCN method with dataset, eps and minpts
    typelist = adcn(dataset,40,10)
    
    #draw result to final shapefile
    Draw_shapefile(write_path)


