import inspect

from app import models
from app import factories  # noqa


def test_models_repr():
    classes = inspect.getmembers(models, inspect.isclass)
    model_classes = [cls for cls in classes if cls[1].__module__ == "app.models"]

    for cls in model_classes:
        test_data = eval(f"factories.{cls[0]}Factory.process_kwargs()")
        obj = cls[1](**test_data)
        test_data_str = ", ".join(
            f"{attr}={repr(value)}" for attr, value in test_data.items()
        )
        assert repr(obj) == f"{cls[0]}({test_data_str})"
