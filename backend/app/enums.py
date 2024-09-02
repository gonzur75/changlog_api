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


class ProductExample(str, Enum):
    name = "ChangelogAPI"


class ExceptionMessages(str, Enum):
    not_found = "Resource not found!"


class UpdateStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    SHIPPED = "shipped"
    DEPRECATED = "deprecated"


class UpdatePointType(str, Enum):
    NEW = "new"
    IMPROVED = "improved"
    FIXED = "fixed"
    UPDATED = "updated"
    DEPRECATED = "deprecated"
    REMOVED = "removed"
