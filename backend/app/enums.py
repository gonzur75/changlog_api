from enum import Enum


class RouterTags(str, Enum):
    product_updates = "product-updates"
    update = "updates"
    product = "products"
    update_points = "update-points"
    points = "points"
    users = "users"


class PointExample(str, Enum):
    name = "Dark Mode"
    description = "Introduce dark mode to our website to improve user experience"


class UpdateExample(str, Enum):
    title = "Changelog restAPI 0.0.1 is ready"
    body = (
        "The Changelog team has been burning the midnight oil to bring you an array of updates, fixes and "
        "enchantments. We believe these changes will take yor changelog creating, to whole new level"
    )
