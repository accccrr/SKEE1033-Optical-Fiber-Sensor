# 光纤位移传感器性能分析项目

## 项目概述

本项目使用Python编程分析光纤位移传感器的性能特性，通过处理实验测量数据，计算传感器灵敏度并生成可视化图表。

## 项目目录结构

```
python小组作业11/
├── Data/                      # 原始数据目录
│   ├── WL.txt                 # 波长数据文件
│   └── P1.txt ~ P15.txt       # 功率数据文件（15个位移点）
│
├── src/                       # 源代码目录
│   ├── config.py              # 配置模块
│   ├── data_loader.py         # 数据读取模块
│   ├── dip_analysis.py        # Dip Wavelength分析模块
│   ├── wavelength_shift.py    # 波长偏移计算模块
│   ├── linear_fit.py          # 线性拟合模块
│   ├── data_exporter.py       # 数据导出模块
│   ├── plotting.py            # 绘图模块
│   └── main.py                # 主程序模块
│
├── output/                    # 输出目录（运行后生成）
│   ├── sensor_data_analysis.csv       # CSV数据文件
│   ├── spectra_plot.png               # 光谱对比图
│   ├── wavelength_shift_plot.png      # 波长偏移图
│   ├── linear_fit_plot.png            # 线性拟合图
│   ├── all_spectra_comparison.png     # 全光谱对比图
│   └── analysis_summary.txt           # 分析摘要
│
├── docs/                      # 文档目录
│   ├── README.md                      # 项目说明文档
│   └── project_instruction.txt        # 项目说明（文本版）
│
├── analyse/                   # 分析报告目录
│   └── 分析报告.md            # 详细的项目分析报告
│
├── scripts/                   # 辅助脚本目录
│   ├── pdf_to_txt.py          # PDF转TXT脚本
│   └── read_docx.py           # DOCX读取脚本
│
├── 1779958033180-Project Instruction.docx   # 原始项目说明
├── 1779958033200-Example Answer 1.pdf       # 示例答案PDF
└── 1779958033200-Example Answer 1.txt       # 示例答案TXT
```

## 模块说明

### src/ - 源代码模块

| 文件 | 模块 | 功能 |
|-----|-----|-----|
| config.py | 配置模块 | 定义路径、参数和常量 |
| data_loader.py | 数据读取模块 | 读取WL和P1-P15数据文件 |
| dip_analysis.py | Dip分析模块 | 计算每个位移点的凹陷波长 |
| wavelength_shift.py | 波长偏移模块 | 计算波长偏移Δλ |
| linear_fit.py | 线性拟合模块 | 执行线性拟合和灵敏度计算 |
| data_exporter.py | 数据导出模块 | 保存CSV和摘要文件 |
| plotting.py | 绘图模块 | 生成所有图表 |
| main.py | 主程序模块 | 整合所有功能 |

## 使用方法

### 运行完整分析

```bash
cd python小组作业11
python3 src/main.py
```

### 单独测试各模块

```bash
cd python小组作业11
python3 src/data_loader.py      # 测试数据读取
python3 src/dip_analysis.py     # 测试Dip计算
python3 src/plotting.py         # 测试绘图功能
```

## 分析流程

1. **数据加载**: 从Data目录读取WL.txt和P1-P15.txt文件
2. **Dip Wavelength计算**: 找到每个位移点功率最低对应的波长
3. **波长偏移计算**: 计算相对于零位移的波长变化
4. **线性拟合**: 对波长偏移-位移数据进行线性拟合
5. **灵敏度计算**: 从拟合斜率计算传感器灵敏度
6. **数据保存**: 将结果保存为CSV文件
7. **图表生成**: 生成光谱图、偏移图和拟合图
8. **摘要保存**: 生成分析摘要文本文件

## 输出结果

### CSV文件内容
```
displacement,dip_wavelength,wavelength_shift
0,1553.7800,0.0000
2,1553.7300,-0.0500
...
```

### 关键结果示例
- **传感器灵敏度**: -0.0128 nm/mm
- **线性拟合R²值**: 0.9824
- **波长偏移范围**: -0.38 nm

## 技术要求

### Python版本
- Python 3.6+

### 依赖库
- numpy: 数值计算
- matplotlib: 数据可视化

### 安装依赖
```bash
pip install numpy matplotlib
```

## 项目评估要点

1. **代码清晰度** (25%): 代码结构清晰，注释充分，变量命名规范
2. **计算正确性** (30%): Dip wavelength和波长偏移计算准确
3. **可视化效果** (25%): 图表符合规范，美观易读
4. **结果分析** (20%): 正确解释传感器灵敏度的物理意义

## 作者信息

- 课程: SKEE 1033 Scientific Programming
- 项目: 光纤位移传感器性能分析
- 时间: 2025/2026学年