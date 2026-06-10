#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dip Wavelength分析模块
负责计算每个位移位置的凹陷波长（功率最小值对应的波长）
"""

import numpy as np
from config import NUM_MEASUREMENTS, get_displacement_array


def find_dip_wavelength(wavelength, power_data):
    """
    找到每个位移位置下功率最低时对应的波长

    Args:
        wavelength: 波长数组，单位nm
        power_data: 功率数据矩阵，shape=(波长点数, 位移点数)

    Returns:
        numpy.ndarray: Dip wavelength数组，长度为位移点数，单位nm

    物理意义:
        Dip wavelength是光谱曲线中功率最小值对应的波长，
        这是传感器响应位移变化的特征波长。
        当传感器发生位移时，dip wavelength会随之偏移。
    """
    dip_wavelength = np.zeros(NUM_MEASUREMENTS)

    print("="*60)
    print("开始计算Dip Wavelength...")
    print("="*60)

    for i in range(NUM_MEASUREMENTS):
        # 找到功率最小的索引
        min_index = np.argmin(power_data[:, i])

        # 获取对应的波长
        dip_wavelength[i] = wavelength[min_index]

        # 获取最小功率值
        min_power = power_data[min_index, i]

        print(f"位移点 {i+1}: Dip波长 = {dip_wavelength[i]:.4f} nm, "
              f"最小功率 = {min_power:.4f} dBm")

    print("="*60)
    print("Dip Wavelength计算完成!")
    print("="*60)

    return dip_wavelength


def analyze_dip_characteristics(wavelength, power_data, dip_wavelength):
    """
    分析Dip特征，包括功率最小值和波长范围

    Args:
        wavelength: 波长数组
        power_data: 功率数据矩阵
        dip_wavelength: Dip wavelength数组

    Returns:
        dict: 包含Dip特征信息的字典
    """
    displacement = get_displacement_array()

    # 获取每个位移点的最小功率值
    min_powers = np.zeros(NUM_MEASUREMENTS)
    for i in range(NUM_MEASUREMENTS):
        min_powers[i] = np.min(power_data[:, i])

    # 计算Dip波长范围
    dip_range = dip_wavelength.max() - dip_wavelength.min()

    characteristics = {
        'displacement': displacement,
        'dip_wavelength': dip_wavelength,
        'min_power': min_powers,
        'dip_wavelength_range': dip_range,
        'dip_wavelength_min': dip_wavelength.min(),
        'dip_wavelength_max': dip_wavelength.max(),
    }

    print("\nDip特征分析:")
    print(f"  Dip波长范围: {dip_range:.4f} nm")
    print(f"  最小Dip波长: {dip_wavelength.min():.4f} nm (位移={displacement[dip_wavelength.argmin()]} mm)")
    print(f"  最大Dip波长: {dip_wavelength.max():.4f} nm (位移={displacement[dip_wavelength.argmax()]} mm)")
    print(f"  平均最小功率: {min_powers.mean():.4f} dBm")

    return characteristics


def check_multiple_minima(wavelength, power_data, tolerance=0.001):
    """
    检查是否存在多个功率最小值点

    Args:
        wavelength: 波长数组
        power_data: 功率数据矩阵
        tolerance: 判断多个最小值的容差（dBm）

    Returns:
        list: 包含多个最小值的位移点索引列表
    """
    multiple_minima_indices = []

    for i in range(NUM_MEASUREMENTS):
        min_power = np.min(power_data[:, i])
        # 找到所有接近最小值的点
        min_indices = np.where(
            np.abs(power_data[:, i] - min_power) < tolerance
        )[0]

        if len(min_indices) > 1:
            multiple_minima_indices.append(i)
            print(f"警告: 位移点 {i+1} 存在 {len(min_indices)} 个接近最小值的点")

    return multiple_minima_indices


if __name__ == "__main__":
    # 测试Dip wavelength计算
    from data_loader import load_all_data

    wavelength, power_data = load_all_data()
    dip_wavelength = find_dip_wavelength(wavelength, power_data)

    print(f"\nDip wavelength数组: {dip_wavelength}")

    # 分析Dip特征
    characteristics = analyze_dip_characteristics(wavelength, power_data, dip_wavelength)

    # 检查多个最小值
    multiple_minima = check_multiple_minima(wavelength, power_data)
    if multiple_minima:
        print(f"\n存在多个最小值的位移点: {multiple_minima}")