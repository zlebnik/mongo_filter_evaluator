======================
Mongo Filter Evaluator
======================


.. image:: https://img.shields.io/pypi/v/mongo_filter_evaluator.svg
        :target: https://pypi.python.org/pypi/mongo_filter_evaluator


Evaluator & validator for mongo-like queries


* Free software: MIT license
* Documentation: https://mongo-filter-evaluator.readthedocs.io.


Features
--------

* Evaluate mongo-like queries in Python:

.. code-block:: python

    DataConditionEvaluator({
        'value': 'value',
        'int': {'$lte': 2}
    }, {
        'value': 'value',
        'int': 1
    }).evaluate()


* Validate typed mongo-like queries:

.. code-block:: python

    errors = ConditionValidator({
        'value': 'value',
        'int': {'$lte': 1}
    }, {
        'value': StringField,
        'int': NumericField
    }).validate()


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
