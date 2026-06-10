#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序模块
整合所有功能模块，完成光纤位移传感器性能分析
"""

import os
import sys
from datetime import datetime

# 导入各个功能模块
from config import (
    ensure_output_dir, OUTPUT_DIR, get_displacement_array,
    NUM_MEASUREMENTS
)
from data_loader import load_all_data
from dip_analysis import find_dip_wavelength, analyze_dip_characteristics
from wavelength_shift import (
    calculate_wavelength_shift, validate_wavelength_shift,
    calculate_shift_statistics
)
from linear_fit import (
    perform_linear_fit, calculate_sensitivity,
    analyze_residuals, evaluate_sensor_performance
)
from data_exporter import save_to_csv, save_analysis_summary, verify_csv_file
from plotting import (
    plot_spectra, plot_wavelength_shift, plot_linear_fit,
    plot_all_spectra_comparison
)


def print_header():
    """打印程序标题"""
    print("\n" + "="*70)
    print(" "*15 + "光纤位移传感器性能分析程序")
    print(" "*20 + "Scientific Programming Project")
    print("="*70)
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("="*70 + "\n")


def print_summary(displacement, dip_wavelength, wavelength_shift,
                  sensitivity, r_squared, performance):
    """
    打印分析结果摘要

    Args:
        displacement: 位移数组
        dip_wavelength: Dip wavelength数组
        wavelength_shift: 波长偏移数组
        sensitivity: 传感器灵敏度
        r_squared: R²值
        performance: 性能评估结果
    """
    print("\n" + "="*70)
    print(" "*25 + "分析结果摘要")
    print("="*70)

    print("\n一、基本数据统计")
    print(f"  测量点数: {len(displacement)}")
    print(f"  位移范围: {displacement.min()} - {displacement.max()} mm")
    print(f"  Dip波长范围: {dip_wavelength.min():.4f} - {dip_wavelength.max():.4f} nm")
    print(f"  波长偏移范围: {wavelength_shift.min():.4f} - {wavelength_shift.max():.4f} nm")

    print("\n二、传感器性能指标")
    print(f"  灵敏度: {sensitivity:.4f} nm/mm")
    print(f"  线性拟合R²值: {r_squared:.4f}")
    print(f"  灵敏度评估: {performance['sensitivity_level']}")
    print(f"  线性度评估: {performance['linearity_level']}")
    print(f"  综合评估: {performance['overall_score']}")

    print("\n三、详细数据表")
    print("位移(mm) | Dip波长(nm) | 波长偏移(nm)")
    print("-"*50)
    for d, wl, ws in zip(displacement, dip_wavelength, wavelength_shift):
        print(f"{d:6.2f}   | {wl:12.4f}  | {ws:12.4f}")

    print("="*70)


def main():
    """
    主函数：执行完整的分析流程

    分析流程:
        1. 加载原始数据
        2. 计算Dip wavelength
        3. 计算波长偏移
        4. 执行线性拟合
        5. 计算传感器灵敏度
        6. 保存数据到CSV
        7. 生成分析图表
        8. 保存分析摘要
    """
    try:
        # 打印程序标题
        print_header()

        # 确保输出目录存在
        ensure_output_dir()

        # 步骤1: 加载原始数据
        print("\n【步骤1】加载原始数据")
        wavelength, power_data = load_all_data()

        # 步骤2: 计算Dip wavelength
        print("\n【步骤2】计算Dip Wavelength")
        dip_wavelength = find_dip_wavelength(wavelength, power_data)

        # 分析Dip特征
        dip_characteristics = analyze_dip_characteristics(
            wavelength, power_data, dip_wavelength
        )

        # 步骤3: 计算波长偏移
        print("\n【步骤3】计算波长偏移")
        wavelength_shift = calculate_wavelength_shift(dip_wavelength)

        # 验证波长偏移计算
        validate_wavelength_shift(wavelength_shift)

        # 计算波长偏移统计信息
        shift_statistics = calculate_shift_statistics(wavelength_shift)

        # 获取位移数组
        displacement = get_displacement_array()

        # 步骤4: 执行线性拟合
        print("\n【步骤4】执行线性拟合")
        fit_results = perform_linear_fit(displacement, wavelength_shift)

        # 分析残差
        residual_analysis = analyze_residuals(
            fit_results['residuals'], displacement
        )

        # 步骤5: 计算传感器灵敏度
        print("\n【步骤5】计算传感器灵敏度")
        sensitivity = calculate_sensitivity(fit_results['slope'])

        # 评估传感器性能
        performance = evaluate_sensor_performance(
            sensitivity, fit_results['r_squared']
        )

        # 步骤6: 保存数据到CSV
        print("\n【步骤6】保存数据到CSV")
        csv_path = save_to_csv(displacement, dip_wavelength, wavelength_shift)

        # 验证CSV文件
        verify_csv_file(csv_path)

        # 步骤7: 生成分析图表
        print("\n【步骤7】生成分析图表")

        # 绘制光谱图
        spectra_path = plot_spectra(wavelength, power_data, displacement)

        # 绘制波长偏移图
        shift_path = plot_wavelength_shift(displacement, wavelength_shift)

        # 绘制线性拟合图
        fit_path = plot_linear_fit(
            displacement, wavelength_shift,
            fit_results['slope'], fit_results['intercept'],
            fit_results['r_squared']
        )

        # 绘制全光谱对比图（可选）
        all_spectra_path = plot_all_spectra_comparison(
            wavelength, power_data, displacement
        )

        # 步骤8: 保存分析摘要
        print("\n【步骤8】保存分析摘要")
        summary_path = save_analysis_summary(
            displacement, dip_wavelength, wavelength_shift,
            sensitivity, fit_results['r_squared']
        )

        # 打印分析结果摘要
        print_summary(
            displacement, dip_wavelength, wavelength_shift,
            sensitivity, fit_results['r_squared'], performance
        )

        # 打印完成信息
        print("\n" + "="*70)
        print(" "*25 + "分析完成!")
        print("="*70)
        print(f"\n输出文件:")
        print(f"  CSV数据: {csv_path}")
        print(f"  光谱图: {spectra_path}")
        print(f"  波长偏移图: {shift_path}")
        print(f"  线性拟合图: {fit_path}")
        print(f"  全光谱对比图: {all_spectra_path}")
        print(f"  分析摘要: {summary_path}")
        print("="*70 + "\n")

        return True

    except Exception as e:
        print("\n" + "="*70)
        print("错误: 分析过程中出现异常")
        print("="*70)
        print(f"错误信息: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        print("="*70)

        # 打印详细的错误追踪信息
        import traceback
        traceback.print_exc()

        return False


if __name__ == "__main__":
    # 运行主程序
    success = main()

    # 根据执行结果设置退出码
    if success:
        sys.exit(0)
    else:
        sys.exit(1)