class BaseField:
    operators = (
        '$eq', '$ne', '$exists', '$eq',
        '$gt', '$gte', '$lt', '$lte',
        '$in', '$nin'
    )

    @classmethod
    def validate_value(self, value):
        return True


class StringField(BaseField):
    operators = BaseField.operators + (
        '$startswith', '$endswith', '$regex', '$contains'
    )


class NumericField(BaseField):
    operators = BaseField.operators + (
        '$mod',
    )
