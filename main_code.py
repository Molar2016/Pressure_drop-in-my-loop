# -*- coding: utf-8 -*-
import sys

sys.path.append("g:\\Github\\iapws")
from iapws import IAPWS97
import math
from numpy import arange

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

moshi = input('please select the calcultion mode: zuli or qudongli or qiujie:')
quality_x = float(input('input the initial quality in the center tube:'))  # mass quality in the center tube
m_min = float(input('please input the minimal flow rate:'))  # kg/s, mass flow rate
m_max = float(input('Then the maximal flow rate:'))
q = float(input('input heating power 100~10000:'))  # W, heating power

H_zx = 2.9  # length of the center tube
H_qb = 0.1  # height in the drum
H_jr = 1.4  # height of the heating section
H_ss = 3.0  # height of risng section H_ss should be the sum of H_zx and H_qb
water_sat = IAPWS97(T=100 + 273.15, x=0)
steam_sat = IAPWS97(T=100 + 273.15, x=1)
p_zhongwei_qb = 9.8 * H_qb / water_sat.v
result_qiujie = [0.0000001, 0.00001, 0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, \
                 0.0008, 0.0009, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, \
                 0.009, 0.01, 0.02, 0.03, 0.04, 0.05,0.06,0.07,0.08,0.09,0.1]


def qudong_zx(mina, maxa):  # dring force in the center tube
    results = {}
    i = mina
    while mina <= i < maxa:
        p_cache = p_zhongwei_zx(i) - p_moca_zx(i) + p_zhongwei_qb
        results[i] = p_cache
        i = i + 0.001
    with open('results.txt', 'w') as f:
        for item in results:
            f.write('%.5f %.2f \n' % (item, results[item]))


def zuli_hx(mina, maxa):  # resistance in the annulus
    results = {}
    i = mina
    while mina <= i < maxa:
        p_cache = p_zhongwei_jr(i) + p_moca_jr(i) + p_jiasu_jr(i) + p_zhongwei_ss(i) + p_moca_ss(i)
        results[i] = p_cache
        i = i + 0.001
    with open('results.txt', 'w') as f:
        for item in results:
            f.write('%.5f %.2f \n' % (item, results[item]))


def p_zhongwei_zx(m):
    g_ = m / (3.1415 / 4 * 0.01 ** 2)
    alpha = voidfraction(quality_x, g_)
    return 9.8 * H_zx * (alpha / steam_sat.v + (1 - alpha) / water_sat.v)


def p_moca_zx(m):
    g_ = m / (3.1415 / 4 * 0.01 ** 2)
    return H_zx * c_zhesuan(quality_x, g_, 0.01)


def p_zhongwei_jr(m):
    result = 0
    for z in arange(0.0, H_jr, 0.01):
        dx = 0.01
        quality_jr_out = q / 2257.2 / 1000 / m + quality_x
        x_z = quality_x + z / H_jr * (quality_jr_out - quality_x)
        x_z2 = quality_x + (z + dx) / H_jr * (quality_jr_out - quality_x)
        g_ = m / (3.1415 / 4 * (0.0224 ** 2 - 0.0127 ** 2))
        alpha = voidfraction(x_z, g_)
        alpha2 = voidfraction(x_z2, g_)
        y1 = (alpha / steam_sat.v + (1 - alpha) / water_sat.v) * 9.8
        y2 = (alpha2 / steam_sat.v + (1 - alpha2) / water_sat.v) * 9.8
        y = (y1 + y2) / 2
        result = y * dx + result
    return result


def p_moca_jr(m):
    quality_jr_out = q / 2257.2 / 1000 / m + quality_x
    quality_x_aver = (quality_jr_out + quality_x) / 2
    g_ = m / (3.1415 / 4 * (0.0224 ** 2 - 0.0127 ** 2))
    return H_jr * c_zhesuan(quality_x_aver, g_, 0.0097)


def p_jiasu_jr(m):
    quality_jr_out = q / 2257.2 / 1000 / m + quality_x
    g_ = m / (3.1415 / 4 * (0.0224 ** 2 - 0.0127 ** 2))
    alpha1 = voidfraction(quality_x, g_)
    alpha2 = voidfraction(quality_jr_out, g_)
    k1 = (1 - quality_jr_out) ** 2 * water_sat.v / (1 - alpha2) + quality_jr_out ** 2 * steam_sat.v / alpha2
    k2 = (1 - quality_x) ** 2 * water_sat.v / (1 - alpha1) + quality_x ** 2 * steam_sat.v / alpha1
    return g_ ** 2 * (k1 - k2)


def p_zhongwei_ss(m):
    g_ = m / (3.1415 / 4 * (0.0224 ** 2 - 0.0127 ** 2))
    quality_jr_out = q / 2257.2 / 1000 / m + quality_x
    alpha = voidfraction(quality_jr_out, g_)
    return 9.8 * H_ss * (alpha / steam_sat.v + (1 - alpha) / water_sat.v)


def p_moca_ss(m):
    quality_jr_out = q / 2257.2 / 1000 / m + quality_x
    g_ = m / (3.1415 / 4 * (0.0224 ** 2 - 0.0127 ** 2))
    return H_ss * c_zhesuan(quality_jr_out, g_, 0.0097)


def voidfraction(x, g_):
    u_zhesuan_g = g_ * x * steam_sat.v
    u_zhesuan_l = g_ * (1 - x) * water_sat.v
    k = (water_sat.v / steam_sat.v) ** 0.1
    k1 = u_zhesuan_g * (1 + (u_zhesuan_l / u_zhesuan_g) ** k)
    k2 = 2.9 * (9.8 * 0.0589 * (water_sat.v - water_sat.v ** 2 / steam_sat.v)) ** 0.25
    return u_zhesuan_g * (k1 + k2) ** -1


def c_zhesuan(x, g_, dh):
    rel = (1 - x) * g_ * dh / water_sat.mu
    reg = x * g_ * dh / water_sat.mu
    if rel <= 2200:
        friction_l = 64 / float(rel)
    else:
        friction_l = 0.3164 * rel ** -0.25
    if reg <= 2200:
        friction_g = 64 / float(reg)
    else:
        friction_g = 0.3164 * reg ** -0.25
    tidu_l = friction_l / dh * g_ ** 2 / 2 * (1 - x) ** 2 * water_sat.v
    tidu_g = friction_g / dh * g_ ** 2 / 2 * x ** 2 * water_sat.v
    Ma = (tidu_l / tidu_g) ** 0.5
    k1 = water_sat.v / steam_sat.v * (water_sat.mu / steam_sat.mu) ** 0.2
    if g_ > 8711.1:
        g_linshi = 8711.1
    else:
        g_linshi = g_
    k2 = math.exp(-(math.log(k1, 10) + 2.5) ** 2 / (2.4 - g_linshi * 10 ** -4))
    c1 = -2 + (28 - 0.3 * g_linshi ** 0.5) * k2
    if c1 < 2.0:
        c = 2.0
    else:
        c = c1
    return (1 + c / Ma + 1 / Ma ** 2) * tidu_l


def solve():
    dp_loop = 0.1  # Pa
    m = 0.001
    while dp_loop > 1E-3 and m <= 0.3:
        dp_loop = p_zhongwei_zx(m) - p_moca_zx(m) - p_zhongwei_jr(m) - p_moca_jr(m) - p_jiasu_jr(m) \
                  - p_zhongwei_ss(m) - p_moca_ss(m) + p_zhongwei_qb
        m = m + 1E-3
    return m


if moshi == 'zuli':
    zuli_hx(m_min, m_max)
elif moshi == 'qudongli':
    qudong_zx(m_min, m_max)
elif moshi == 'qiujie':
    with open('results.txt', 'w') as f:
        for i in range(0, len(result_qiujie)):
            quality_x = result_qiujie[i]
            jie = solve()
            p1 = p_zhongwei_zx(jie) - p_moca_zx(jie) + p_zhongwei_qb
            f.write('%.8f %.4f %.2f \n' % (result_qiujie[i], jie, p1))
else:
    print('Input Erro')
