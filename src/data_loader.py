#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Loading Module
Responsible for loading wavelength and power data from files
"""

import os
import numpy as np
from config import DATA_DIR, WAVELENGTH_FILE, POWER_FILE_PATTERN, NUM_MEASUREMENTS


def load_wavelength_data():
    """
    Load wavelength data from WL.txt file

    Returns:
        numpy.ndarray: Wavelength array in nm

    Raises:
        FileNotFoundError: If wavelength file does not exist
    """
    filepath = os.path.join(DATA_DIR, WAVELENGTH_FILE)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Wavelength data file not found: {filepath}")

    # Read wavelength data (tab-separated single line)
    with open(filepath, 'r') as f:
        content = f.read().strip()
        wavelength = np.array([float(x) for x in content.split('\t')])

    print(f"Successfully loaded wavelength data: {len(wavelength)} data points")
    print(f"Wavelength range: {wavelength.min():.3f} - {wavelength.max():.3f} nm")

    return wavelength


def load_power_data():
    """
    Load power data from P1.txt to P15.txt files

    Returns:
        numpy.ndarray: Power data matrix with shape=(number of wavelength points, number of displacement points), unit: dBm

    Raises:
        FileNotFoundError: If power file does not exist
    """
    power_data_list = []

    for i in range(1, NUM_MEASUREMENTS + 1):
        filename = POWER_FILE_PATTERN.format(i)
        filepath = os.path.join(DATA_DIR, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Power data file not found: {filepath}")

        # Read power data (tab-separated single line)
        with open(filepath, 'r') as f:
            content = f.read().strip()
            power = np.array([float(x) for x in content.split('\t')])
            power_data_list.append(power)

        print(f"Successfully loaded {filename}: {len(power)} data points")

    # Convert to 2D array with shape=(number of displacement points, number of wavelength points)
    power_data = np.array(power_data_list)

    # Transpose to shape=(number of wavelength points, number of displacement points) for easier processing
    power_data = power_data.T

    print(f"\nPower data matrix shape: {power_data.shape}")
    print(f"Power range: {power_data.min():.3f} - {power_data.max():.3f} dBm")

    return power_data


def validate_data(wavelength, power_data):
    """
    Validate data integrity and consistency

    Args:
        wavelength: Wavelength array
        power_data: Power data matrix

    Returns:
        bool: Whether data is valid

    Raises:
        ValueError: If data dimensions do not match
    """
    # Check if wavelength and power data dimensions match
    num_wavelength_points = len(wavelength)
    num_power_points = power_data.shape[0]

    if num_wavelength_points != num_power_points:
        raise ValueError(
            f"Data dimension mismatch: wavelength points {num_wavelength_points} "
            f"!= power points {num_power_points}"
        )

    # Check number of displacement points
    num_displacements = power_data.shape[1]
    if num_displacements != NUM_MEASUREMENTS:
        raise ValueError(
            f"Displacement point count mismatch: {num_displacements} != {NUM_MEASUREMENTS}"
        )

    print("\nData validation passed!")
    print(f"  Wavelength points: {num_wavelength_points}")
    print(f"  Displacement points: {num_displacements}")

    return True


def load_all_data():
    """
    Load all data and perform validation

    Returns:
        tuple: (wavelength, power_data)
            wavelength: Wavelength array
            power_data: Power data matrix

    Example:
        >>> wavelength, power_data = load_all_data()
        >>> print(wavelength.shape)
        >>> print(power_data.shape)
    """
    print("="*60)
    print("Loading sensor data...")
    print("="*60)

    # Read wavelength data
    wavelength = load_wavelength_data()

    # Read power data
    power_data = load_power_data()

    # Validate data
    validate_data(wavelength, power_data)

    print("="*60)
    print("Data loading complete!")
    print("="*60)

    return wavelength, power_data


if __name__ == "__main__":
    # Test data loading
    wavelength, power_data = load_all_data()
    print(f"\nWavelength data example (first 5): {wavelength[:5]}")
    print(f"Power data example (first 5 of P1): {power_data[:5, 0]}")