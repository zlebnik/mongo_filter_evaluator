import re
from flatdict import FlatDict

from .base import (BaseConditionEvaluator,
                   BaseComparisonMixin,
                   BaseElementMixin,
                   BaseEvaluationMixin,
                   LogicalMixin)


def if_field_in_data(f):
    def wrap_method(self, field, value):
        return (field in self.data) and f(self, field, value)
    return wrap_method


class ComparisonDataMixin(BaseComparisonMixin):

    @if_field_in_data
    def f_eq(self, field, value):
        return self.data[field] == value

    @if_field_in_data
    def f_gt(self, field, value):
        return self.data[field] > value

    @if_field_in_data
    def f_gte(self, field, value):
        return self.data[field] >= value

    @if_field_in_data
    def f_in(self, field, value):
        return self.data[field] in value

    @if_field_in_data
    def f_lt(self, field, value):
        return self.data[field] < value

    @if_field_in_data
    def f_lte(self, field, value):
        return self.data[field] <= value

    @if_field_in_data
    def f_ne(self, field, value):
        return self.data[field] != value

    @if_field_in_data
    def f_nin(self, field, value):
        return not(self.data[field] in value)


class ElementDataMixin(BaseElementMixin):
    def f_exists(self, field, value):
        if value:
            return field in self.data
        else:
            return field not in self.data


class EvaluationDataMixin(BaseEvaluationMixin):
    @if_field_in_data
    def f_mod(self, field, value):
        """value: [ divisor, remainder ]"""
        divisor, remainder = value
        return (self.data[field] % divisor) == remainder

    @if_field_in_data
    def f_regex(self, field, value):
        return bool(re.match(value, self.data[field]))

    @if_field_in_data
    def f_startswith(self, field, value):
        return self.data[field].startswith(value)

    @if_field_in_data
    def f_endswith(self, field, value):
        return self.data[field].endswith(value)

    @if_field_in_data
    def f_contains(self, field, value):
        return value in self.data[field]


class DataConditionEvaluator(BaseConditionEvaluator,
                             LogicalMixin,
                             ComparisonDataMixin,
                             ElementDataMixin,
                             EvaluationDataMixin):

    def __init__(self, condition, data):
        super(DataConditionEvaluator, self).__init__(condition)
        self.data = FlatDict(data, delimiter='.')

    def evaluate_equality(self, field, value):
        return self.data[field] == value

    def evaluate_logic(self, keyword, body):
        return getattr(self, 'c_%s' % keyword[1:])(body)

    def evaluate_function(self, keyword, field, body):
        return getattr(self, 'f_%s' % keyword[1:])(
            field=field,
            value=body,
        )

    def default_field_condition_handler(self, field, value):
        return field in self.data and self.data[field] == value
