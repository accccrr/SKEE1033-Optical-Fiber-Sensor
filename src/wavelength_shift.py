#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波长偏移计算模块
负责计算每个位移位置相对于零位移的波长变化
"""

import numpy as np
from config import get_displacement_array


def calculate_wavelength_shift(dip_wavelength):
    """
    计算波长偏移（Δλ）

    Args:
        dip_wavelength: Dip wavelength数组，单位nm

    Returns:
        numpy.ndarray: 波长偏移数组，单位nm

    计算公式:
        Δλ[n] = λ[n] - λ[0]

    参数说明:
        Δλ[n]: 第n个位移位置的波长偏移
        λ[n]: 第n个位移位置的dip wavelength
        λ[0]: 零位移时的dip wavelength（参考基准）

    物理意义:
        波长偏移反映了传感器对位移的响应灵敏度。
        正偏移表示波长随位移增加而增大，
        负偏移表示波长随位移增加而减小。
    """
    # 零位移时的dip wavelength作为参考基准
    reference_wavelength = dip_wavelength[0]

    # 计算波长偏移
    wavelength_shift = dip_wavelength - reference_wavelength

    print("="*60)
    print("波长偏移计算结果:")
    print("="*60)

    displacement = get_displacement_array()

    for i, (disp, shift) in enumerate(zip(displacement, wavelength_shift)):
        print(f"位移 {disp} mm: 波长偏移 Δλ = {shift:.4f} nm")

    print("="*60)
    print(f"参考波长（零位移）: {reference_wavelength:.4f} nm")
    print(f"波长偏移范围: {wavelength_shift.min():.4f} - {wavelength_shift.max():.4f} nm")
    print("="*60)

    return wavelength_shift


def validate_wavelength_shift(wavelength_shift):
    """
    验证波长偏移计算的正确性

    Args:
        wavelength_shift: 波长偏移数组

    Returns:
        bool: 计算是否正确

    检查项:
        1. 零位移时的波长偏移必须为0
        2. 波长偏移值应在合理范围内（通常几纳米）
    """
    # 检查零位移时的偏移是否为0
    if wavelength_shift[0] != 0:
        raise ValueError(
            f"零位移时的波长偏移不为0: {wavelength_shift[0]}"
        )

    # 检查波长偏移范围是否合理（通常在几纳米范围内）
    max_shift = np.abs(wavelength_shift).max()
    if max_shift > 10:  # 如果超过10nm，可能存在问题
        print(f"警告: 波长偏移值较大 ({max_shift:.2f} nm)，请检查数据")

    print("\n波长偏移验证通过!")
    return True


def calculate_shift_statistics(wavelength_shift):
    """
    计算波长偏移的统计特性

    Args:
        wavelength_shift: 波长偏移数组

    Returns:
        dict: 统计信息字典
    """
    displacement = get_displacement_array()

    statistics = {
        'mean_shift': np.mean(wavelength_shift),
        'std_shift': np.std(wavelength_shift),
        'max_shift': wavelength_shift.max(),
        'min_shift': wavelength_shift.min(),
        'shift_range': wavelength_shift.max() - wavelength_shift.min(),
    }

    print("\n波长偏移统计信息:")
    print(f"  平均偏移: {statistics['mean_shift']:.4f} nm")
    print(f"  标准差: {statistics['std_shift']:.4f} nm")
    print(f"  最大偏移: {statistics['max_shift']:.4f} nm")
    print(f"  最小偏移: {statistics['min_shift']:.4f} nm")
    print(f"  偏移范围: {statistics['shift_range']:.4f} nm")

    return statistics


def create_shift_data_dict(displacement, dip_wavelength, wavelength_shift):
    """
    创建包含位移、dip波长和波长偏移的数据字典

    Args:
        displacement: 位移数组
        dip_wavelength: Dip wavelength数组
        wavelength_shift: 波长偏移数组

    Returns:
        dict: 数据字典
    """
    data_dict = {
        'displacement': displacement,
        'dip_wavelength': dip_wavelength,
        'wavelength_shift': wavelength_shift,
    }

    return data_dict


if __name__ == "__main__":
    # 测试波长偏移计算
    from data_loader import load_all_data
    from dip_analysis import find_dip_wavelength

    wavelength, power_data = load_all_data()
    dip_wavelength = find_dip_wavelength(wavelength, power_data)

    wavelength_shift = calculate_wavelength_shift(dip_wavelength)

    # 验证计算结果
    validate_wavelength_shift(wavelength_shift)

    # 计算统计信息
    statistics = calculate_shift_statistics(wavelength_shift)

    # 创建数据字典
    displacement = get_displacement_array()
    data_dict = create_shift_data_dict(displacement, dip_wavelength, wavelength_shift)

    print(f"\n数据字典示例:")
    print(f"  位移: {data_dict['displacement'][:5]}")
    print(f"  Dip波长: {data_dict['dip_wavelength'][:5]}")
    print(f"  波长偏移: {data_dict['wavelength_shift'][:5]}")