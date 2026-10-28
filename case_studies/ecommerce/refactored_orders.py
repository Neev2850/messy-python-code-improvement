"""
Refactored Order Processing Module
Refactored with AI Assistance to adhere to SOLID principles, PEP 8,
immutable dataclasses, and dedicated discount strategy abstractions.
"""

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import List, Optional, Protocol


class DiscountType(Enum):
    NONE = "NONE"
    SAVE10 = "SAVE10"
    SAVE20 = "SAVE20"
    VIP = "VIP"


class DiscountStrategy(Protocol):
    """Protocol defining discount calculation strategies."""
    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        ...


class Save10Strategy:
    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        return (subtotal * Decimal("0.10")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class Save20Strategy:
    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        if subtotal > Decimal("100.00"):
            return (subtotal * Decimal("0.20")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return min(Decimal("5.00"), subtotal)


class VIPStrategy:
    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        return (subtotal * Decimal("0.25")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class NoDiscountStrategy:
    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        return Decimal("0.00")


DISCOUNT_STRATEGIES = {
    DiscountType.NONE: NoDiscountStrategy(),
    DiscountType.SAVE10: Save10Strategy(),
    DiscountType.SAVE20: Save20Strategy(),
    DiscountType.VIP: VIPStrategy()
}


@dataclass(frozen=True)
class OrderItem:
    """Immutable representation of an order item with strict validation."""
    name: str
    unit_price: Decimal
    quantity: int
    discount_type: DiscountType = DiscountType.NONE
    tax_rate: Decimal = Decimal("0.0825")

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Item name cannot be empty")
        if self.unit_price < Decimal("0.00"):
            raise ValueError(f"Price must be non-negative: {self.unit_price}")
        if self.quantity <= 0:
            raise ValueError(f"Quantity must be positive: {self.quantity}")

    @property
    def gross_subtotal(self) -> Decimal:
        return (self.unit_price * self.quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def discount_amount(self) -> Decimal:
        strategy = DISCOUNT_STRATEGIES.get(self.discount_type, NoDiscountStrategy())
        return strategy.calculate_discount(self.gross_subtotal)

    @property
    def net_subtotal(self) -> Decimal:
        return self.gross_subtotal - self.discount_amount

    @property
    def tax_amount(self) -> Decimal:
        return (self.net_subtotal * self.tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def total(self) -> Decimal:
        return self.net_subtotal + self.tax_amount


@dataclass
class Cart:
    """Manages order items and provides aggregate billing breakdowns."""
    items: List[OrderItem] = field(default_factory=list)

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)

    @property
    def subtotal(self) -> Decimal:
        return sum((item.net_subtotal for item in self.items), Decimal("0.00"))

    @property
    def total_tax(self) -> Decimal:
        return sum((item.tax_amount for item in self.items), Decimal("0.00"))

    @property
    def grand_total(self) -> Decimal:
        return sum((item.total for item in self.items), Decimal("0.00"))

    def get_receipt(self) -> str:
        lines = ["=" * 40, "            ORDER RECEIPT", "=" * 40]
        for item in self.items:
            lines.append(f"{item.name:<24} x{item.quantity:<2} ${item.total:>8.2f}")
            if item.discount_amount > 0:
                lines.append(f"  └─ Discount ({item.discount_type.value}): -${item.discount_amount:.2f}")
        lines.append("-" * 40)
        lines.append(f"{'Subtotal:':<28} ${self.subtotal:>8.2f}")
        lines.append(f"{'Estimated Tax:':<28} ${self.total_tax:>8.2f}")
        lines.append(f"{'Grand Total:':<28} ${self.grand_total:>8.2f}")
        lines.append("=" * 40)
        return "\n".join(lines)


if __name__ == "__main__":
    cart = Cart()
    cart.add_item(OrderItem("Mechanical Keyboard", Decimal("120.00"), 1, DiscountType.SAVE20))
    cart.add_item(OrderItem("USB-C Hub", Decimal("25.00"), 2, DiscountType.SAVE10))
    print(cart.get_receipt())
