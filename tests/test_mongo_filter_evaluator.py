#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mongo_filter_evaluator` package."""

import pytest

from mongo_filter_evaluator import ConditionValidator, DataConditionEvaluator
from mongo_filter_evaluator.types import StringField, NumericField


def test_validate():
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    assert len(ConditionValidator({
        'value': 'value',
        'int': {'$lte': 1}
    }, {
        'value': StringField,
        'int': NumericField
    }).validate()) == 0

    assert len(ConditionValidator({
        'value': 'value',
        'int': {'$startswith': 1}
    }, {
        'value': StringField,
        'int': NumericField
    }).validate()) == 2


def test_evaluate_emptyfilter():
    assert DataConditionEvaluator(
        {
            "$and": [
               {'value': 'value'},
               {}
            ]
        },
        {
            'value': 'value',
            'int': 1
        }
    ).evaluate()

def test_evaluate():
    assert DataConditionEvaluator(
        {
            'value': 'value',
            'int': {'$lte': 2}
        },
        {
            'value': 'value',
            'int': 1
        }
    ).evaluate()

    assert not DataConditionEvaluator(
        {
            'value': 'value',
            'int': {'$lte': 2}
        },
        {
            'value': 'value',
            'int': 3
        }
    ).evaluate()


def test_evaluate_deep():
    assert DataConditionEvaluator(
        {
            'value.a': 1,
            'int': {
                '$lte': 2
            }
        },
        {
            'value': {
                'a': 1
            },
            'int': 1
        }
    ).evaluate()

    assert not DataConditionEvaluator(
        {
            'value.a': 2,
            'int': {'$lte': 2}
        },
        {
            'value': {
                'a': 1
            },
            'int': 3
        }
    ).evaluate()
