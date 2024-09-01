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
