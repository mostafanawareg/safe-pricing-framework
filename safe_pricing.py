"""
Safe Pricing Framework (PPP) — reference implementation.

Methodology by Dr. Mostafa Nawareg — International Marketing Consultant,
Corporate Trainer & Author. https://mostafanawareg.com

This module reproduces, rule for rule, the calculations of the
"Safe Pricing" calculator (التسعير الآمن) published in the Marketing Planner
Suite:
https://marketingplannerai.mostafanawareg.com/marketing-template.html#tool-pricing-safe

PPP = Premium · Promotion · Penetration
  * Premium     — an even "quality" anchor price derived from the quality leader.
  * Promotion   — an odd promotional price that reads as a deal.
  * Penetration — the safe price sits 10% below the market leader.

Run as a script for a quick calculation:
    python safe_pricing.py --quality 1250000 --market 980000 --cost 700000 \
        --fixed 2000000 --variable 600000
"""

from __future__ import annotations

import argparse
import math
from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass, asdict

__all__ = [
    "SafePriceResult",
    "BreakEvenResult",
    "anchor_price",
    "safe_price",
    "calculate_safe_price",
    "calculate_break_even",
]

PENETRATION_FACTOR = 0.90  # safe price = market leader price × 90%


def _js_round(x: float) -> int:
    """Round half up, like JavaScript's Math.round (Python's round() is half-even)."""
    return math.floor(x + 0.5)


def _js_to_fixed_1(x: float) -> float:
    """One decimal place with ties rounded up, like JavaScript's Number.prototype.toFixed(1)."""
    return float(Decimal(x).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def _num(x: float) -> str:
    return f"{x:,.0f}" if float(x).is_integer() else f"{x:,.2f}"


# ──────────────────────────────────────────────────────────────
# Step 1 — PPP safe price
# ──────────────────────────────────────────────────────────────

def anchor_price(quality_leader_price: float) -> int:
    """Premium anchor: the quality leader's price as an even integer.

    An even integer price is kept as-is; otherwise the price is rounded up
    and, if the result is odd, raised by 1.
    """
    if quality_leader_price <= 0:
        raise ValueError("quality_leader_price must be > 0")
    anchor = math.ceil(quality_leader_price)
    if anchor % 2 != 0:
        anchor += 1
    if float(quality_leader_price).is_integer() and quality_leader_price % 2 == 0:
        anchor = int(quality_leader_price)
    return anchor


def safe_price(market_leader_price: float) -> int:
    """Promotional safe price: 90% of the market leader, floored, forced odd, minimum 1."""
    if market_leader_price <= 0:
        raise ValueError("market_leader_price must be > 0")
    sale = math.floor(market_leader_price * PENETRATION_FACTOR)
    if sale % 2 == 0:
        sale -= 1
    if sale < 1:
        sale = 1
    return sale


@dataclass(frozen=True)
class SafePriceResult:
    product: str
    quality_leader_price: float
    market_leader_price: float
    cost_leader_price: float
    anchor: int                 # المرساة النفسية — even premium anchor (shown struck through)
    safe_price: int             # السعر الترويجي الآمن — odd promotional price
    customer_saving: int        # توفير العميل = anchor − safe price
    discount_pct: int           # نسبة الخصم عن قائد الجودة (%)
    safe_zone: tuple            # المنطقة الآمنة = (safe price, market leader price)

    def as_dict(self) -> dict:
        return asdict(self)


def calculate_safe_price(
    quality_leader_price: float,
    market_leader_price: float,
    cost_leader_price: float,
    product: str = "Product",
) -> SafePriceResult:
    """Full PPP calculation.

    Args:
        quality_leader_price: highest price in the category (the premium leader).
        market_leader_price:  price of the best-selling product in the category.
        cost_leader_price:    lowest competitor price in the category.
        product:              product or service name.
    """
    if not product or not str(product).strip():
        raise ValueError("product name is required")
    for name, value in (
        ("quality_leader_price", quality_leader_price),
        ("market_leader_price", market_leader_price),
        ("cost_leader_price", cost_leader_price),
    ):
        if value is None or not value > 0:
            raise ValueError(f"{name} must be > 0")

    anchor = anchor_price(quality_leader_price)
    sale = safe_price(market_leader_price)
    return SafePriceResult(
        product=str(product).strip(),
        quality_leader_price=quality_leader_price,
        market_leader_price=market_leader_price,
        cost_leader_price=cost_leader_price,
        anchor=anchor,
        safe_price=sale,
        customer_saving=anchor - sale,
        discount_pct=_js_round((1 - sale / quality_leader_price) * 100),
        safe_zone=(sale, market_leader_price),
    )


# ──────────────────────────────────────────────────────────────
# Step 2 — Break-even at the safe price
# ──────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class BreakEvenResult:
    selling_price: float
    fixed_costs: float
    variable_cost_per_unit: float
    units: int                  # نقطة التعادل (units per month)
    contribution_margin: float  # هامش المساهمة للقطعة
    contribution_pct: float     # نسبة هامش المساهمة من سعر البيع (%)
    revenue: float              # الإيراد الكلي عند نقطة التعادل

    def as_dict(self) -> dict:
        return asdict(self)


def calculate_break_even(
    selling_price: float,
    fixed_costs: float,
    variable_cost_per_unit: float,
) -> BreakEvenResult:
    """Break-even units = ceil(fixed costs ÷ (selling price − variable cost per unit))."""
    if selling_price is None or not selling_price > 0:
        raise ValueError("selling_price must be > 0")
    if fixed_costs is None or not fixed_costs > 0:
        raise ValueError("fixed_costs must be > 0")
    if variable_cost_per_unit is None or variable_cost_per_unit < 0:
        raise ValueError("variable_cost_per_unit must be >= 0")

    contribution = selling_price - variable_cost_per_unit
    if contribution <= 0:
        raise ValueError("variable cost per unit equals or exceeds the selling price")

    units = math.ceil(fixed_costs / contribution)
    return BreakEvenResult(
        selling_price=selling_price,
        fixed_costs=fixed_costs,
        variable_cost_per_unit=variable_cost_per_unit,
        units=units,
        contribution_margin=contribution,
        contribution_pct=_js_to_fixed_1(contribution / selling_price * 100),
        revenue=units * selling_price,
    )


# ──────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────

def _main() -> None:
    p = argparse.ArgumentParser(description="Safe Pricing Framework (PPP) — Dr. Mostafa Nawareg")
    p.add_argument("--product", default="Product")
    p.add_argument("--quality", type=float, required=True, help="quality leader (highest) price")
    p.add_argument("--market", type=float, required=True, help="market leader (best-selling) price")
    p.add_argument("--cost", type=float, required=True, help="cost leader (lowest) price")
    p.add_argument("--fixed", type=float, help="monthly fixed costs (optional, for break-even)")
    p.add_argument("--variable", type=float, help="variable cost per unit (optional, for break-even)")
    a = p.parse_args()

    r = calculate_safe_price(a.quality, a.market, a.cost, a.product)
    print(f"Product:            {r.product}")
    print(f"Premium anchor:     {r.anchor:,}")
    print(f"Safe price:         {r.safe_price:,}")
    print(f"Customer saving:    {r.customer_saving:,}")
    print(f"Discount vs quality leader: {r.discount_pct}%")
    print(f"Safe zone:          {_num(r.safe_zone[0])} – {_num(r.safe_zone[1])}")

    if a.fixed is not None and a.variable is not None:
        b = calculate_break_even(r.safe_price, a.fixed, a.variable)
        print(f"Break-even:         {b.units:,} units / month")
        print(f"Contribution:       {b.contribution_margin:,.0f} per unit ({b.contribution_pct}%)")
        print(f"Break-even revenue: {b.revenue:,.0f}")


if __name__ == "__main__":
    _main()
