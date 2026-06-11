#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Module
Defines paths, parameters, and constants for the project
"""

import os

# Project root directory (parent of src directory)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directory
DATA_DIR = os.path.join(PROJECT_ROOT, 'Data')

# Output directory
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')

# Data file configuration
WAVELENGTH_FILE = 'WL.txt'
POWER_FILE_PATTERN = 'P{}.txt'  # P1.txt, P2.txt, ..., P15.txt
NUM_MEASUREMENTS = 15  # Number of measurement points

# Displacement configuration
DISPLACEMENT_STEP = 2  # Displacement step (mm)
DISPLACEMENT_START = 0  # Start displacement (mm)
DISPLACEMENT_END = 28  # End displacement (mm)

# Plot configuration
PLOT_DPI = 300  # Image resolution
PLOT_FORMAT = 'png'  # Image format
PLOT_SIZE = (10, 6)  # Image size (width, height)

# Displacement points to plot (for spectra plot)
PLOT_DISPLACEMENTS = [0, 4, 8, 12, 16, 20, 24, 28]  # mm

# Output filenames
OUTPUT_CSV = 'sensor_data_analysis.csv'
OUTPUT_SPECTRA_PLOT = 'spectra_plot.png'
OUTPUT_SHIFT_PLOT = 'wavelength_shift_plot.png'
OUTPUT_FIT_PLOT = 'linear_fit_plot.png'

# Data precision
DECIMAL_PLACES = 4  # Number of decimal places

# Color configuration (for spectra plot)
SPECTRA_COLORS = [
    'blue', 'green', 'red', 'cyan',
    'magenta', 'orange', 'purple', 'brown'
]


def ensure_output_dir():
    """Ensure output directory exists"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")


def get_displacement_array():
    """
    Generate displacement array

    Returns:
        numpy.ndarray: Displacement array in mm
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
    Get indices of displacement points to plot in the displacement array

    Returns:
        list: Index list
    """
    indices = [d // DISPLACEMENT_STEP for d in PLOT_DISPLACEMENTS]
    return indices