
"""
config_validation.py — Config and CSV validation.

This module provides functions to validate configuration files and CSVs used by the system.
It ensures that config files and data files conform to expected schemas and formats.
"""

import csv
import json
import re


def validate_rules_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("rules.json must be a list of objects")
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(f"rules.json item {i} is not an object")
            if 'category' not in item or 'pattern' not in item:
                raise ValueError(f"rules.json item {i} missing 'category' or 'pattern'")
            try:
                re.compile(item['pattern'])
            except re.error as e:
                raise ValueError(f"rules.json item {i} pattern regex error: {e}")
    except Exception as e:
        raise RuntimeError(f"rules.json: {e}")

def validate_overrides_csv(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != ['key', 'category']:
                raise ValueError("overrides.csv must have headers: key,category")
            for i, row in enumerate(reader):
                if 'key' not in row or 'category' not in row:
                    raise ValueError(f"overrides.csv row {i+2} missing 'key' or 'category'")
    except Exception as e:
        raise RuntimeError(f"overrides.csv: {e}")

def validate_splits_csv(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != ['fingerprint', 'category', 'amount']:
                raise ValueError("splits.csv must have headers: fingerprint,category,amount")
            for i, row in enumerate(reader):
                if 'fingerprint' not in row or 'category' not in row or 'amount' not in row:
                    raise ValueError(f"splits.csv row {i+2} missing required fields")
                try:
                    float(row['amount'])
                except ValueError:
                    raise ValueError(f"splits.csv row {i+2} amount not a float: {row['amount']}")
    except Exception as e:
        raise RuntimeError(f"splits.csv: {e}")
