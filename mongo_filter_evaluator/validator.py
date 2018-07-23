from functools import reduce
from operator import and_, or_

from .base import (
    BaseConditionEvaluator,
    LogicalMixin,
    BaseComparisonMixin,
    BaseElementMixin,
    BaseEvaluationMixin
)


def is_field_available(f):
    def wrap_method(self, field, value, *args, **kwargs):
        if not (field in self.available_fields):
            self.errors.append('%s not in available_fields' % field)
        return f(self, field, value, *args, **kwargs)

    return wrap_method


def is_value_permissible(f):
    def wrap_method(self, field, value, *args, **kwargs):
        if not self.permissible_value_for_field(field, value):
            self.errors.append('%s can`t be value of %s' % (value, field))
        return f(self, field, value, *args, **kwargs)

    return wrap_method


class LogicalValidatorMixin(LogicalMixin):
    def default_logical_conjunction(self, i):
        return reduce(and_, i)

    def default_logical_disjunction(self, i):
        return reduce(or_, i)

    def c_and(self, body):
        if not (isinstance(body, dict) or isinstance(body, list)):
            self.errors.append('$and takes list or dict')
        return super(LogicalValidatorMixin, self).c_and(body)

    def c_not(self, body):
        if not isinstance(body, dict):
            self.errors.append('$not takes only dict')
        return super(LogicalValidatorMixin, self).c_not(body)

    def c_or(self, body):
        if not (isinstance(body, dict) or isinstance(body, list)):
            self.errors.append('$or takes list or dict')
        return super(LogicalValidatorMixin, self).c_or(body)


class ComparisonValidatorMixin(BaseComparisonMixin):
    @is_field_available
    @is_value_permissible
    def f_in(self, field, value):
        if not isinstance(value, list):
            self.errors.append('$in takes only list, not %s' % value)
        for v in value:
            if not self.permissible_value_for_field(field, v):
                raise ValueError('%s can`t be value of %s in $in' % (v, field))
        return True

    @is_field_available
    @is_value_permissible
    def f_nin(self, field, value):
        if not isinstance(value, list):
            self.errors.append(
                '%s $nin takes only list, not %s' % (field, value)
            )
        for v in value:
            if not self.permissible_value_for_field(field, v):
                self.errors.append(
                    '%s can`t be value of %s in $nin' % (v, field)
                )
        return True


class ElementValidatorMixin(BaseElementMixin):
    @is_field_available
    def f_exists(self, field, value):
        if not isinstance(value, bool):
            self.errors.append(
                "$exists takes True or False, not " % value
            )
        return True


class EvaluationValidatorMixin(BaseEvaluationMixin):
    @is_field_available
    @is_value_permissible
    def f_mod(self, field, value):
        if not (isinstance(value, list) and len(value) == 2 and
                isinstance(value[0], int) and
                isinstance(value[1], int)):
            self.errors.append('$mod takes list like [int, int]')
        return True

    @is_field_available
    @is_value_permissible
    def f_regex(self, field, value):
        if not isinstance(value, str):
            self.errors.append(
                '$regex take a string, but type %s is %s' % (
                    value, type(value)
                )
            )
        return True

    @is_field_available
    @is_value_permissible
    def f_startswith(self, field, value):
        if not isinstance(value, str):
            self.errors.append(
                '$startswith take a string, but type %s is %s' % (
                    value, type(value)
                )
            )
        return True

    @is_field_available
    @is_value_permissible
    def f_endswith(self, field, value):
        if not isinstance(value, str):
            self.errors.append(
                '$endswith take a string, but type %s is %s' % (
                    value, type(value)
                )
            )
        return True

    @is_field_available
    @is_value_permissible
    def f_contains(self, field, value):
        if not isinstance(value, str):
            self.errors.append(
                '$contains take a string, but type %s is %s' % (
                    value, type(value)
                )
            )
        return True


class ConditionValidator(
    BaseConditionEvaluator,
    ComparisonValidatorMixin,
    ElementValidatorMixin,
    EvaluationValidatorMixin
):
    def __init__(self, condition, available_fields):
        super(ConditionValidator, self).__init__(condition)
        self.available_fields = available_fields
        self.errors = []

    def evaluate_logic(self, keyword, body):
        if isinstance(body, dict):
            return all(
                self.evaluate_condition(condition_keyword, condition_body)
                for (condition_keyword, condition_body) in body.items()
            )
        elif isinstance(body, list):
            return all(
                self.evaluate(condition)
                for condition in body
            )

    def evaluate_function(self, keyword, field, body):
        if keyword not in self.available_fields[field].operators:
            self.errors.append(
                'Operation %s not permitted with field %s' % (
                    keyword, field
                )
            )
        if hasattr(self, 'f_%s' % keyword[1:]):
            getattr(self, 'f_%s' % keyword[1:])(field, body)

    def evaluate_equality(self, field, value):
        return self.permissible_value_for_field(field, value)

    def permissible_value_for_field(self, field, value):
        return self.available_fields[field].validate_value(value)

    def validate(self, condition=None):
        self.errors = []
        self.evaluate(condition)
        return self.errors

    def evaluate(self, condition=None):
        _condition = condition if condition else self.condition

        if isinstance(_condition, dict):
            super(ConditionValidator, self).evaluate(condition)
        else:
            self.errors.append('condition must be dict.')

    def evaluate_condition(self, keyword, body):
        if not isinstance(keyword, str):
            self.errors.append(
                'condition_keyword can`t be %s' % type(keyword)
            )

        return super(ConditionValidator, self).evaluate_condition(
            keyword, body
        )
