# -*- coding: utf-8 -*-
import sys

sys.path.append("g:\\Github\\iapws")
from iapws import IAPWS97

"""这是本人的一个练习项目
旨在计算本人自然循环回路内的各项压降情况，采用分相流模型
这其中包含中心管的重位压降、阻力、环隙内的重位压降、摩擦压惊、加速压降
假设一进入环隙即发生了饱和沸腾，中心管与环隙无热量交换，汽包饱和
计算采用国际单位SI
"""

"""p_zhongwei_qb 汽包内的重位压降
   p_zhongwei_zx 中心管内的重位压降
   p_moca_zx 中心管内的摩擦压降
   p_zhongwei_jr 加热环隙内的重位压降
   p_moca_jr 加热环隙内的摩擦压降
   p_jiasu_jr 加热环隙内的加速压降
   p_zhongwei_ss 上升环隙内的重位压降
   p_moca_ss 上升环隙内的摩擦压降
"""


quality_x = input('input the quality in the center tube:')  # mass quality in the center tube
DP_loop = 0.1 # Pa
H_zx=2.9 # length of the center tube
H_qb=0.1 # height in the drum
H_jr=1.4 # height of the heating section
H_ss=3.0 #height of risng section H_ss should be the sum of H_zx and H_qb

def main():
    moshi=input('please select the calcultion mode: zuli or qudongli or qiujie:')
    if moshi=='zuli':
        m_min = input('please input the minimal flow rate:')  # kg/s, mass flow rate
        m_max = input('Then the maximal flow rate:')
        q = input('heating power 100~10000:')  # W, heating power
        zuli_hx(m_min,m_max,q)
    elif moshi=='qudongli':
        m_min = input('please input the minimal flow rate:')
        m_max = input('Then the maximal flow rate:')
        qudong_zx(m_min,m_max)
    elif moshi=='qiujie':
        solve()
    else:
        print('Input Erro')

def qudong_zx(m_min,m_max): # dring force in the center tube
    results={}
    while i> m_min and i<m_max:
        1_cache=p_zhongwei_zx(i)-p_moca_zx(i)+p_zhongwei_qb()
        results[i]=1_cache
        i=i+0.001
    with open('results','w') as f:
        for item in results:
            f.write(str(item)+' '+str(results[item])+'\n')

def zuli_hx(m_min,m_max,Q): # resistance in the annulus
    results={}
    while i>m_min and i<m_max:
        2_chache=p_zhongwei_jr(i)+p_moca_jr(i)+p_jiasu_jr(i)+p_zhongwei_ss(i)+p_moca_ss(i)
        results[i]=2_cache
        i=i+0.001
    with open('results','w') as f:
        for item in results:
            f.write(str(item)+' '+str(results[item])+'\n')

def p_zhongwei_zx(m):
    pass


def p_moca_zx(m):
    pass


def p_zhongwei_jr(m):
    pass


def p_moca_jr(m):
    pass


def p_jiasu_jr(m):
    pass


def p_zhongwei_ss(m):
    pass


def p_moca_ss(m):
    pass


def p_zhongwei_qb():
    pass


def solve():
    while DP_loop > 1E-3:
        m = m + 1E-3
        DP_loop = p_zhongwei_zx(m) - p_moca_zx(m) - p_zhongwei_jr(m) - p_moca_jr(m) - p_jiasu_jr(m) \
                  - p_zhongwei_ss(m) - p_moca_ss(m)+p_zhongwei_qb()
     return m