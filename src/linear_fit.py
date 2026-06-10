#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
线性拟合模块
负责对波长偏移-位移数据进行线性拟合，并计算传感器灵敏度
"""

import numpy as np
from config import get_displacement_array


def perform_linear_fit(displacement, wavelength_shift):
    """
    对波长偏移-位移数据进行线性拟合

    Args:
        displacement: 位移数组，单位mm
        wavelength_shift: 波长偏移数组，单位nm

    Returns:
        dict: 包含拟合结果的字典
            - slope: 斜率（灵敏度）
            - intercept: 截距
            - r_squared: R²值
            - y_pred: 拟合预测值
            - residuals: 残差

    拟合方法:
        使用最小二乘法进行一阶多项式拟合
        Python实现: np.polyfit(displacement, wavelength_shift, 1)

    拟合参数:
        斜率 (m): polyfit结果[0]
        截距 (b): polyfit结果[1]
        拟合方程: Δλ = m × d + b
    """
    print("="*60)
    print("开始线性拟合...")
    print("="*60)

    # 一阶多项式拟合
    coefficients = np.polyfit(displacement, wavelength_shift, 1)
    slope = coefficients[0]
    intercept = coefficients[1]

    # 计算拟合预测值
    y_pred = slope * displacement + intercept

    # 计算R²值
    ss_tot = np.sum((wavelength_shift - np.mean(wavelength_shift)) ** 2)
    ss_res = np.sum((wavelength_shift - y_pred) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # 计算残差
    residuals = wavelength_shift - y_pred

    # 打印拟合结果
    print(f"拟合方程: Δλ = {slope:.4f} × d + {intercept:.4f}")
    print(f"斜率 (灵敏度): {slope:.4f} nm/mm")
    print(f"截距: {intercept:.4f} nm")
    print(f"R²值: {r_squared:.4f}")

    # 评估拟合质量
    if r_squared > 0.95:
        print("拟合质量: 优秀 (R² > 0.95)")
    elif r_squared > 0.90:
        print("拟合质量: 良好 (R² > 0.90)")
    elif r_squared > 0.80:
        print("拟合质量: 一般 (R² > 0.80)")
    else:
        print("拟合质量: 较差 (R² < 0.80)，可能存在非线性关系")

    print("="*60)

    fit_results = {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'y_pred': y_pred,
        'residuals': residuals,
        'equation': f'Δλ = {slope:.4f} × d + {intercept:.4f}',
    }

    return fit_results


def calculate_sensitivity(slope):
    """
    计算传感器灵敏度

    Args:
        slope: 线性拟合的斜率

    Returns:
        float: 传感器灵敏度，单位nm/mm

    物理意义:
        灵敏度表示每毫米位移引起的波长变化量。
        灵敏度越高，传感器对微小位移越敏感。
        是评估传感器性能的关键指标。
    """
    sensitivity = slope

    print("="*60)
    print("传感器灵敏度计算结果:")
    print("="*60)
    print(f"灵敏度: {sensitivity:.4f} nm/mm")
    print(f"物理意义: 每毫米位移引起 {sensitivity:.4f} nm 的波长变化")
    print("="*60)

    return sensitivity


def analyze_residuals(residuals, displacement):
    """
    分析拟合残差，检查是否存在非线性或异常点

    Args:
        residuals: 拟合残差数组
        displacement: 位移数组

    Returns:
        dict: 残差分析结果
    """
    # 计算残差统计量
    mean_residual = np.mean(residuals)
    std_residual = np.std(residuals)
    max_residual = np.abs(residuals).max()

    # 找到残差最大的点（可能的异常点）
    max_residual_idx = np.argmax(np.abs(residuals))
    max_residual_disp = displacement[max_residual_idx]

    print("\n残差分析:")
    print(f"  平均残差: {mean_residual:.4f} nm")
    print(f"  残差标准差: {std_residual:.4f} nm")
    print(f"  最大残差: {max_residual:.4f} nm (位移 {max_residual_disp} mm)")

    # 检查残差是否随机分布
    if np.abs(mean_residual) < 0.001:
        print("  残差分布: 随机分布（平均残差接近0）")
    else:
        print("  残差分布: 可能存在系统性偏差")

    # 检查是否存在非线性趋势
    # 通过检查残差与位移的关系来判断
    if len(residuals) > 5:
        # 简单检查：残差是否有明显的趋势
        residual_trend = np.polyfit(displacement, residuals, 1)[0]
        if np.abs(residual_trend) > 0.01:
            print("  警告: 残差存在趋势，可能存在非线性关系")
        else:
            print("  残差趋势: 无明显趋势，线性拟合合理")

    analysis = {
        'mean_residual': mean_residual,
        'std_residual': std_residual,
        'max_residual': max_residual,
        'max_residual_idx': max_residual_idx,
        'max_residual_disp': max_residual_disp,
    }

    return analysis


def evaluate_sensor_performance(sensitivity, r_squared):
    """
    评估传感器性能

    Args:
        sensitivity: 传感器灵敏度（nm/mm）
        r_squared: 线性拟合R²值

    Returns:
        dict: 性能评估结果
    """
    print("\n传感器性能评估:")
    print("="*60)

    # 灵敏度评估
    if sensitivity > 0.5:
        sensitivity_level = "高灵敏度"
        sensitivity_score = "优秀"
    elif sensitivity > 0.1:
        sensitivity_level = "中等灵敏度"
        sensitivity_score = "良好"
    else:
        sensitivity_level = "低灵敏度"
        sensitivity_score = "一般"

    print(f"灵敏度评估: {sensitivity_level} ({sensitivity_score})")

    # 线性度评估
    if r_squared > 0.98:
        linearity_level = "极佳线性度"
        linearity_score = "优秀"
    elif r_squared > 0.95:
        linearity_level = "良好线性度"
        linearity_score = "良好"
    elif r_squared > 0.90:
        linearity_level = "一般线性度"
        linearity_score = "一般"
    else:
        linearity_level = "较差线性度"
        linearity_score = "较差"

    print(f"线性度评估: {linearity_level} ({linearity_score})")

    # 综合评估
    if sensitivity_score == "优秀" and linearity_score == "优秀":
        overall_score = "优秀"
    elif sensitivity_score in ["优秀", "良好"] and linearity_score in ["优秀", "良好"]:
        overall_score = "良好"
    else:
        overall_score = "一般"

    print(f"综合评估: {overall_score}")
    print("="*60)

    performance = {
        'sensitivity_level': sensitivity_level,
        'sensitivity_score': sensitivity_score,
        'linearity_level': linearity_level,
        'linearity_score': linearity_score,
        'overall_score': overall_score,
    }

    return performance


if __name__ == "__main__":
    # 测试线性拟合功能
    from data_loader import load_all_data
    from dip_analysis import find_dip_wavelength
    from wavelength_shift import calculate_wavelength_shift

    # 加载和处理数据
    wavelength, power_data = load_all_data()
    dip_wavelength = find_dip_wavelength(wavelength, power_data)
    wavelength_shift = calculate_wavelength_shift(dip_wavelength)
    displacement = get_displacement_array()

    # 执行线性拟合
    fit_results = perform_linear_fit(displacement, wavelength_shift)

    # 计算灵敏度
    sensitivity = calculate_sensitivity(fit_results['slope'])

    # 分析残差
    residual_analysis = analyze_residuals(fit_results['residuals'], displacement)

    # 评估传感器性能
    performance = evaluate_sensor_performance(sensitivity, fit_results['r_squared'])