from abc import abstractmethod, ABCMeta


class BaseConditionEvaluator(object):
    __metaclass__ = ABCMeta

    def __init__(self, condition):
        self.condition = condition

    @abstractmethod
    def evaluate_logic(self, keyword, body):
        """Evaluates $and, $or, $not"""
        raise NotImplementedError('Error :(')

    @abstractmethod
    def evaluate_function(self, keyword, field, body):
        """Evaluates $-functions"""
        raise NotImplementedError('Error :(')

    @abstractmethod
    def evaluate_equality(self, field, value):
        """Should check equality"""
        raise NotImplementedError('Error :(')

    def evaluate(self, condition=None):
        condition = condition if condition is not None else self.condition
        return self.evaluate_logic('$and', condition)

    def evaluate_condition(self, keyword, body):
        if keyword.startswith('$'):
            return self.evaluate_logic(keyword, body)
        else:
            if isinstance(body, dict):
                return all(
                    self.evaluate_function(op_keyword, keyword, op_body)
                    for op_keyword, op_body in body.items()
                )
            else:
                return self.evaluate_equality(keyword, body)


class LogicalMixin:
    def c_and(self, body):
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

    def c_not(self, body):
        return not self.evaluate(body)

    def c_or(self, body):
        if isinstance(body, dict):
            return any(
                self.evaluate_condition(condition_keyword, condition_body)
                for (condition_keyword, condition_body) in body.items()
            )
        elif isinstance(body, list):
            return any(
                self.evaluate(condition)
                for condition in body
            )


class BaseComparisonMixin:
    @abstractmethod
    def f_eq(self, field, value):
        """{ 'field': { '$eq': 'value' } }"""

    @abstractmethod
    def f_gt(self, field, value):
        """{ 'field': { '$gt': 'value' } }"""

    @abstractmethod
    def f_gte(self, field, value):
        """{ 'field': { '$gte': 'value' } }"""

    @abstractmethod
    def f_in(self, field, value):
        """{ 'field': { '$in': 'value' } }"""

    @abstractmethod
    def f_lt(self, field, value):
        """{ 'field': { '$lt': 'value' } }"""

    @abstractmethod
    def f_lte(self, field, value):
        """{ 'field': { '$lte': 'value' } }"""

    @abstractmethod
    def f_ne(self, field, value):
        """{ 'field': { '$ne': 'value' } }"""

    @abstractmethod
    def f_nin(self, field, value):
        """{ field: { '$nin': value } }"""


class BaseElementMixin:
    @abstractmethod
    def f_exists(self, field, value):
        """
        { field: { '$nin': value } }
        value: <True|False>
        """


class BaseEvaluationMixin:
    @abstractmethod
    def f_mod(self, field, value):
        """
        { field: { '$mod': [ divisor, remainder ] } }
        value: [ divisor, remainder ]
        """

    @abstractmethod
    def f_regex(self, field, value):
        """
        { field: { '$regex': regexp } }
        value: python regexp expression.
        """

    @abstractmethod
    def f_startswith(self, field, value):
        """
        { field: { '$startswith': value } }
        """

    @abstractmethod
    def f_endswith(self, field, value):
        """
        { field: { '$endswith': value } }
        """

    @abstractmethod
    def f_contains(self, field, value):
        """
        { field: { '$contains': value } }
        """

    # TODO: f_expr, I WANT TO BELIEVE
    # def f_expr(self, field, value):
    #   Allows use of aggregation expressions within the query language.
    #   pass
