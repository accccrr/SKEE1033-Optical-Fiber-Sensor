#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据导出模块
负责将分析结果保存为CSV文件
"""

import os
import numpy as np
from config import OUTPUT_DIR, OUTPUT_CSV, DECIMAL_PLACES, ensure_output_dir


def save_to_csv(displacement, dip_wavelength, wavelength_shift):
    """
    将位移、dip波长和波长偏移数据保存为CSV文件

    Args:
        displacement: 位移数组，单位mm
        dip_wavelength: Dip wavelength数组，单位nm
        wavelength_shift: 波长偏移数组，单位nm

    Returns:
        str: CSV文件路径

    CSV文件格式:
        displacement,dip_wavelength,wavelength_shift
        0,1550.234,0.000
        2,1550.876,0.642
        ...
    """
    # 确保输出目录存在
    ensure_output_dir()

    # CSV文件路径
    filepath = os.path.join(OUTPUT_DIR, OUTPUT_CSV)

    # 创建数据矩阵
    data = np.column_stack([displacement, dip_wavelength, wavelength_shift])

    # 保存为CSV文件
    header = 'displacement,dip_wavelength,wavelength_shift'

    # 使用numpy.savetxt保存
    np.savetxt(
        filepath,
        data,
        delimiter=',',
        header=header,
        comments='',  # 不添加注释符号
        fmt=f'%.{DECIMAL_PLACES}f'  # 格式化小数位数
    )

    print("="*60)
    print("CSV文件保存成功!")
    print("="*60)
    print(f"文件路径: {filepath}")
    print(f"数据行数: {len(displacement)}")
    print(f"数据列数: 3")

    # 显示CSV文件内容示例
    print("\nCSV文件内容示例:")
    print(header)
    for i in range(min(5, len(displacement))):
        print(f"{displacement[i]:.{DECIMAL_PLACES}f},"
              f"{dip_wavelength[i]:.{DECIMAL_PLACES}f},"
              f"{wavelength_shift[i]:.{DECIMAL_PLACES}f}")
    print("...")

    return filepath


def save_analysis_summary(displacement, dip_wavelength, wavelength_shift,
                          sensitivity, r_squared):
    """
    保存分析摘要到文本文件

    Args:
        displacement: 位移数组
        dip_wavelength: Dip wavelength数组
        wavelength_shift: 波长偏移数组
        sensitivity: 传感器灵敏度（nm/mm）
        r_squared: 线性拟合的R²值

    Returns:
        str: 摘要文件路径
    """
    ensure_output_dir()

    filepath = os.path.join(OUTPUT_DIR, 'analysis_summary.txt')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("光纤位移传感器性能分析摘要\n")
        f.write("="*60 + "\n\n")

        f.write("一、数据概况\n")
        f.write(f"  测量点数: {len(displacement)}\n")
        f.write(f"  位移范围: {displacement.min()} - {displacement.max()} mm\n")
        f.write(f"  Dip波长范围: {dip_wavelength.min():.4f} - {dip_wavelength.max():.4f} nm\n")
        f.write(f"  波长偏移范围: {wavelength_shift.min():.4f} - {wavelength_shift.max():.4f} nm\n\n")

        f.write("二、传感器性能\n")
        f.write(f"  灵敏度: {sensitivity:.4f} nm/mm\n")
        f.write(f"  线性拟合R²值: {r_squared:.4f}\n\n")

        f.write("三、详细数据\n")
        f.write("位移(mm) | Dip波长(nm) | 波长偏移(nm)\n")
        f.write("-"*50 + "\n")
        for d, wl, ws in zip(displacement, dip_wavelength, wavelength_shift):
            f.write(f"{d:6.2f} | {wl:12.4f} | {ws:12.4f}\n")

    print(f"\n分析摘要已保存: {filepath}")

    return filepath


def verify_csv_file(filepath):
    """
    验证CSV文件的正确性

    Args:
        filepath: CSV文件路径

    Returns:
        bool: 文件是否有效
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"CSV文件不存在: {filepath}")

    # 读取CSV文件
    data = np.loadtxt(filepath, delimiter=',', skiprows=1)

    # 检查数据维度
    if data.shape[1] != 3:
        raise ValueError(f"CSV文件列数不正确: {data.shape[1]} != 3")

    print(f"\nCSV文件验证通过!")
    print(f"  数据维度: {data.shape}")

    return True


if __name__ == "__main__":
    # 测试CSV保存功能
    from data_loader import load_all_data
    from dip_analysis import find_dip_wavelength
    from wavelength_shift import calculate_wavelength_shift
    from config import get_displacement_array

    # 加载和处理数据
    wavelength, power_data = load_all_data()
    dip_wavelength = find_dip_wavelength(wavelength, power_data)
    wavelength_shift = calculate_wavelength_shift(dip_wavelength)
    displacement = get_displacement_array()

    # 保存CSV文件
    csv_path = save_to_csv(displacement, dip_wavelength, wavelength_shift)

    # 验证CSV文件
    verify_csv_file(csv_path)