# -*- coding: utf-8 -*-

"""Top-level package for Mongo Filter Evaluator."""

__author__ = """Gleb Kovalev"""
__email__ = 'gleb@popmechanic.io'
__version__ = '0.1.0'

from .base import BaseConditionEvaluator  # noqa: F401
from .validator import ConditionValidator  # noqa: F401
from .evaluator import DataConditionEvaluator  # noqa: F401
