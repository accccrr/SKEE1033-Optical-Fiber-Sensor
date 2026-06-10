#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件模块
定义项目所需的路径、参数和常量
"""

import os

# 项目根目录（src目录的父目录）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据目录
DATA_DIR = os.path.join(PROJECT_ROOT, 'Data')

# 输出目录
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')

# 数据文件配置
WAVELENGTH_FILE = 'WL.txt'
POWER_FILE_PATTERN = 'P{}.txt'  # P1.txt, P2.txt, ..., P15.txt
NUM_MEASUREMENTS = 15  # 测量点数量

# 位移配置
DISPLACEMENT_STEP = 2  # 位移步长 (mm)
DISPLACEMENT_START = 0  # 起始位移 (mm)
DISPLACEMENT_END = 28  # 结束位移 (mm)

# 绘图配置
PLOT_DPI = 300  # 图像分辨率
PLOT_FORMAT = 'png'  # 图像格式
PLOT_SIZE = (10, 6)  # 图像尺寸 (宽, 高)

# 需要绘制的位移点（用于光谱图）
PLOT_DISPLACEMENTS = [0, 4, 8, 12, 16, 20, 24, 28]  # mm

# 输出文件名
OUTPUT_CSV = 'sensor_data_analysis.csv'
OUTPUT_SPECTRA_PLOT = 'spectra_plot.png'
OUTPUT_SHIFT_PLOT = 'wavelength_shift_plot.png'
OUTPUT_FIT_PLOT = 'linear_fit_plot.png'

# 数据精度
DECIMAL_PLACES = 4  # 小数位数

# 颜色配置（用于光谱图）
SPECTRA_COLORS = [
    'blue', 'green', 'red', 'cyan',
    'magenta', 'orange', 'purple', 'brown'
]


def ensure_output_dir():
    """确保输出目录存在"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"创建输出目录: {OUTPUT_DIR}")


def get_displacement_array():
    """
    生成位移数组

    Returns:
        numpy.ndarray: 位移数组，单位mm
    """
    import numpy as np
    displacements = np.arange(
        DISPLACEMENT_START,
        DISPLACEMENT_END + DISPLACEMENT_STEP,
        DISPLACEMENT_STEP
    )
    return displacements


def get_plot_indices():
    """
    获取需要绘制的位移点在位移数组中的索引

    Returns:
        list: 索引列表
    """
    indices = [d // DISPLACEMENT_STEP for d in PLOT_DISPLACEMENTS]
    return indices