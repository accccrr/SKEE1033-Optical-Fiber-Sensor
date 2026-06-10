#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据读取模块
负责从文件中读取波长和功率数据
"""

import os
import numpy as np
from config import DATA_DIR, WAVELENGTH_FILE, POWER_FILE_PATTERN, NUM_MEASUREMENTS


def load_wavelength_data():
    """
    从WL.txt文件读取波长数据

    Returns:
        numpy.ndarray: 波长数组，单位nm

    Raises:
        FileNotFoundError: 如果波长文件不存在
    """
    filepath = os.path.join(DATA_DIR, WAVELENGTH_FILE)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"波长数据文件不存在: {filepath}")

    # 读取波长数据（制表符分隔的单行数据）
    with open(filepath, 'r') as f:
        content = f.read().strip()
        wavelength = np.array([float(x) for x in content.split('\t')])

    print(f"成功读取波长数据: {len(wavelength)} 个数据点")
    print(f"波长范围: {wavelength.min():.3f} - {wavelength.max():.3f} nm")

    return wavelength


def load_power_data():
    """
    从P1.txt到P15.txt文件读取功率数据

    Returns:
        numpy.ndarray: 功率数据矩阵，shape=(波长点数, 位移点数)，单位dBm

    Raises:
        FileNotFoundError: 如果功率文件不存在
    """
    power_data_list = []

    for i in range(1, NUM_MEASUREMENTS + 1):
        filename = POWER_FILE_PATTERN.format(i)
        filepath = os.path.join(DATA_DIR, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"功率数据文件不存在: {filepath}")

        # 读取功率数据（制表符分隔的单行数据）
        with open(filepath, 'r') as f:
            content = f.read().strip()
            power = np.array([float(x) for x in content.split('\t')])
            power_data_list.append(power)

        print(f"成功读取 {filename}: {len(power)} 个数据点")

    # 转换为二维数组，shape=(位移点数, 波长点数)
    power_data = np.array(power_data_list)

    # 转置为 shape=(波长点数, 位移点数)，便于后续处理
    power_data = power_data.T

    print(f"\n功率数据矩阵形状: {power_data.shape}")
    print(f"功率范围: {power_data.min():.3f} - {power_data.max():.3f} dBm")

    return power_data


def validate_data(wavelength, power_data):
    """
    验证数据的完整性和一致性

    Args:
        wavelength: 波长数组
        power_data: 功率数据矩阵

    Returns:
        bool: 数据是否有效

    Raises:
        ValueError: 如果数据维度不匹配
    """
    # 检查波长和功率数据的维度是否匹配
    num_wavelength_points = len(wavelength)
    num_power_points = power_data.shape[0]

    if num_wavelength_points != num_power_points:
        raise ValueError(
            f"数据维度不匹配: 波长点数 {num_wavelength_points} "
            f"!= 功率点数 {num_power_points}"
        )

    # 检查位移点数量
    num_displacements = power_data.shape[1]
    if num_displacements != NUM_MEASUREMENTS:
        raise ValueError(
            f"位移点数量不匹配: {num_displacements} != {NUM_MEASUREMENTS}"
        )

    print("\n数据验证通过!")
    print(f"  波长点数: {num_wavelength_points}")
    print(f"  位移点数: {num_displacements}")

    return True


def load_all_data():
    """
    加载所有数据并进行验证

    Returns:
        tuple: (wavelength, power_data)
            wavelength: 波长数组
            power_data: 功率数据矩阵

    Example:
        >>> wavelength, power_data = load_all_data()
        >>> print(wavelength.shape)
        >>> print(power_data.shape)
    """
    print("="*60)
    print("开始加载传感器数据...")
    print("="*60)

    # 读取波长数据
    wavelength = load_wavelength_data()

    # 读取功率数据
    power_data = load_power_data()

    # 验证数据
    validate_data(wavelength, power_data)

    print("="*60)
    print("数据加载完成!")
    print("="*60)

    return wavelength, power_data


if __name__ == "__main__":
    # 测试数据加载
    wavelength, power_data = load_all_data()
    print(f"\n波长数据示例 (前5个): {wavelength[:5]}")
    print(f"功率数据示例 (P1前5个): {power_data[:5, 0]}")