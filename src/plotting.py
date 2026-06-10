#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
绘图模块
负责生成光谱图、波长偏移图和线性拟合图
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from config import (
    OUTPUT_DIR, PLOT_DPI, PLOT_FORMAT, PLOT_SIZE,
    OUTPUT_SPECTRA_PLOT, OUTPUT_SHIFT_PLOT, OUTPUT_FIT_PLOT,
    SPECTRA_COLORS, get_plot_indices, ensure_output_dir
)

# 设置matplotlib支持中文（如果需要）
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.unicode_minus'] = False


def plot_spectra(wavelength, power_data, displacement):
    """
    绘制不同位移下的光谱图（功率vs波长）

    Args:
        wavelength: 波长数组，单位nm
        power_data: 功率数据矩阵，shape=(波长点数, 位移点数)
        displacement: 位移数组，单位mm

    Returns:
        str: 图像文件路径

    绘图要求:
        - 选择的位移点: 0, 4, 8, 12, 16, 20, 24, 28 mm
        - 共8条曲线，使用不同颜色区分
        - 包含图例、坐标轴标签、标题
    """
    ensure_output_dir()

    # 获取需要绘制的位移索引
    plot_indices = get_plot_indices()

    # 创建图形
    plt.figure(figsize=PLOT_SIZE)

    # 绘制每条光谱曲线
    for idx, color in zip(plot_indices, SPECTRA_COLORS):
        disp_value = displacement[idx]
        plt.plot(
            wavelength,
            power_data[:, idx],
            color=color,
            linewidth=1.5,
            label=f'{disp_value} mm'
        )

    # 设置坐标轴标签和标题
    plt.xlabel('Wavelength (nm)', fontsize=12)
    plt.ylabel('Power (dBm)', fontsize=12)
    plt.title('Optical Fiber Displacement Sensor Spectra', fontsize=14)

    # 设置图例
    plt.legend(loc='best', fontsize=10)

    # 添加网格
    plt.grid(True, alpha=0.3)

    # 调整布局
    plt.tight_layout()

    # 保存图像
    filepath = os.path.join(OUTPUT_DIR, OUTPUT_SPECTRA_PLOT)
    plt.savefig(filepath, dpi=PLOT_DPI, format=PLOT_FORMAT)
    plt.close()

    print("="*60)
    print("光谱图保存成功!")
    print("="*60)
    print(f"文件路径: {filepath}")
    print(f"包含位移点: {[displacement[i] for i in plot_indices]} mm")

    return filepath


def plot_wavelength_shift(displacement, wavelength_shift):
    """
    绘制波长偏移vs位移的散点图

    Args:
        displacement: 位移数组，单位mm
        wavelength_shift: 波长偏移数组，单位nm

    Returns:
        str: 图像文件路径

    绘图要求:
        - 横轴: 位移（mm）
        - 纵轴: 波长偏移Δλ（nm）
        - 使用散点图或折线图
    """
    ensure_output_dir()

    # 创建图形
    plt.figure(figsize=PLOT_SIZE)

    # 绘制散点图
    plt.scatter(
        displacement,
        wavelength_shift,
        color='blue',
        s=50,
        marker='o',
        label='Data Points',
        zorder=3
    )

    # 绘制折线连接数据点
    plt.plot(
        displacement,
        wavelength_shift,
        color='blue',
        linewidth=1,
        alpha=0.5,
        zorder=2
    )

    # 设置坐标轴标签和标题
    plt.xlabel('Displacement (mm)', fontsize=12)
    plt.ylabel('Wavelength Shift Δλ (nm)', fontsize=12)
    plt.title('Wavelength Shift vs Displacement', fontsize=14)

    # 设置图例
    plt.legend(loc='best', fontsize=10)

    # 添加网格
    plt.grid(True, alpha=0.3)

    # 调整布局
    plt.tight_layout()

    # 保存图像
    filepath = os.path.join(OUTPUT_DIR, OUTPUT_SHIFT_PLOT)
    plt.savefig(filepath, dpi=PLOT_DPI, format=PLOT_FORMAT)
    plt.close()

    print("="*60)
    print("波长偏移图保存成功!")
    print("="*60)
    print(f"文件路径: {filepath}")

    return filepath


def plot_linear_fit(displacement, wavelength_shift, slope, intercept, r_squared):
    """
    绘制线性拟合结果图

    Args:
        displacement: 位移数组，单位mm
        wavelength_shift: 波长偏移数组，单位nm
        slope: 拟合直线斜率（灵敏度）
        intercept: 拟合直线截距
        r_squared: R²值

    Returns:
        str: 图像文件路径

    绘图要求:
        - 同时显示原始数据点和拟合直线
        - 标注拟合方程
        - 显示R²值
    """
    ensure_output_dir()

    # 计算拟合直线
    y_pred = slope * displacement + intercept

    # 创建图形
    plt.figure(figsize=PLOT_SIZE)

    # 绘制原始数据点
    plt.scatter(
        displacement,
        wavelength_shift,
        color='blue',
        s=50,
        marker='o',
        label='Data Points',
        zorder=3
    )

    # 绘制拟合直线
    plt.plot(
        displacement,
        y_pred,
        color='red',
        linewidth=2,
        label=f'Linear Fit: Δλ = {slope:.4f}×d + {intercept:.4f}\nR² = {r_squared:.4f}',
        zorder=2
    )

    # 设置坐标轴标签和标题
    plt.xlabel('Displacement (mm)', fontsize=12)
    plt.ylabel('Wavelength Shift Δλ (nm)', fontsize=12)
    plt.title('Wavelength Shift vs Displacement with Linear Fit', fontsize=14)

    # 设置图例
    plt.legend(loc='best', fontsize=10)

    # 添加网格
    plt.grid(True, alpha=0.3)

    # 调整布局
    plt.tight_layout()

    # 保存图像
    filepath = os.path.join(OUTPUT_DIR, OUTPUT_FIT_PLOT)
    plt.savefig(filepath, dpi=PLOT_DPI, format=PLOT_FORMAT)
    plt.close()

    print("="*60)
    print("线性拟合图保存成功!")
    print("="*60)
    print(f"文件路径: {filepath}")
    print(f"拟合方程: Δλ = {slope:.4f}×d + {intercept:.4f}")
    print(f"R²值: {r_squared:.4f}")

    return filepath


def plot_all_spectra_comparison(wavelength, power_data, displacement):
    """
    绘制所有位移点的光谱对比图（可选功能）

    Args:
        wavelength: 波长数组
        power_data: 功率数据矩阵
        displacement: 位移数组

    Returns:
        str: 图像文件路径
    """
    ensure_output_dir()

    plt.figure(figsize=(12, 8))

    # 使用渐变色绘制所有光谱
    colors = plt.cm.viridis(np.linspace(0, 1, len(displacement)))

    for i, color in enumerate(colors):
        plt.plot(
            wavelength,
            power_data[:, i],
            color=color,
            linewidth=1,
            alpha=0.7,
            label=f'{displacement[i]} mm'
        )

    plt.xlabel('Wavelength (nm)', fontsize=12)
    plt.ylabel('Power (dBm)', fontsize=12)
    plt.title('All Spectra Comparison', fontsize=14)
    plt.legend(loc='best', fontsize=8, ncol=2)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    filepath = os.path.join(OUTPUT_DIR, 'all_spectra_comparison.png')
    plt.savefig(filepath, dpi=PLOT_DPI, format='png')
    plt.close()

    print(f"\n全光谱对比图已保存: {filepath}")

    return filepath


if __name__ == "__main__":
    # 测试绘图功能
    from data_loader import load_all_data
    from dip_analysis import find_dip_wavelength
    from wavelength_shift import calculate_wavelength_shift
    from config import get_displacement_array

    # 加载和处理数据
    wavelength, power_data = load_all_data()
    dip_wavelength = find_dip_wavelength(wavelength, power_data)
    wavelength_shift = calculate_wavelength_shift(dip_wavelength)
    displacement = get_displacement_array()

    # 绘制光谱图
    spectra_path = plot_spectra(wavelength, power_data, displacement)

    # 绘制波长偏移图
    shift_path = plot_wavelength_shift(displacement, wavelength_shift)

    # 简单线性拟合用于测试
    slope, intercept = np.polyfit(displacement, wavelength_shift, 1)
    y_pred = slope * displacement + intercept
    ss_tot = np.sum((wavelength_shift - np.mean(wavelength_shift)) ** 2)
    ss_res = np.sum((wavelength_shift - y_pred) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # 绘制线性拟合图
    fit_path = plot_linear_fit(displacement, wavelength_shift, slope, intercept, r_squared)

    print("\n所有图像已生成完成!")