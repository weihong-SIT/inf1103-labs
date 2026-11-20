from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Common interface: every discount turns an order total into a new total."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):

    def __init__(self, percentage: float) -> None:

        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")

        self.__percentage = percentage

    @property
    def percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):

    def __init__(self, threshold: float, amount: float) -> None:

        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")

        self.__threshold = threshold
        self.__amount = amount

    def apply(self, total: float) -> float:

        if total >= self.__threshold:
            return max(total - self.__amount, 0.0)

        return total


class StudentDiscount(DiscountStrategy):
    """Fourth strategy: a flat 5% off. Order did not need to change."""

    RATE = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)