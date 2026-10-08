# Safe Pricing Framework (PPP)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23231855.svg)](https://doi.org/10.5281/zenodo.23231855)

**A launch-pricing method for new products: price 10% below the market leader, anchor against the quality leader, and know your break-even before day one.**

Methodology by **[Dr. Mostafa Nawareg](https://mostafanawareg.com/about-dr-mostafa-nawareg/)** — International Marketing Consultant, Corporate Trainer & Author.
Live calculator (free, Arabic): **[Safe Pricing — التسعير الآمن](https://marketingplannerai.mostafanawareg.com/marketing-template.html#tool-pricing-safe)** · Methodology article (Arabic): [استراتيجية التسعير الآمن للمنتجات الجديدة](https://mostafanawareg.com/maqalat-tswiqia/%D8%A7%D9%84%D8%AA%D8%B3%D8%B9%D9%8A%D8%B1-%D8%A7%D9%84%D8%A2%D9%85%D9%86-%D9%84%D9%84%D9%85%D9%86%D8%AA%D8%AC%D8%A7%D8%AA-%D8%A7%D9%84%D8%AC%D8%AF%D9%8A%D8%AF%D8%A9/) · [Free marketing AI tools](https://mostafanawareg.com/free-marketing-ai-tools/)

This repository is the reference implementation of the calculator's logic in plain Python, verified to produce identical results to the published tool.

---

## The idea

A new product entering a crowded category faces two risks: price too low and destroy perceived value, or price too high and slow down trial. The Safe Pricing Framework resolves this with three principles — **PPP**:

| | Principle | What it does | Basis |
|---|---|---|---|
| **P** | **Premium** — psychological anchor | Shows an even, premium reference price derived from the category's quality leader, so the offer is read against the top of the market. | Anchoring effect (Tversky & Kahneman, 1974) |
| **P** | **Promotion** — odd pricing | The selling price is an odd number, which reads as a deal. | Odd-pricing effect (Schindler & Kirby, 1997) |
| **P** | **Penetration** — the 10% rule | The selling price sits 10% below the best-selling product: enough to trigger first purchase, not enough to cheapen the brand. | Price elasticity & market penetration (Kotler, 2000) |

### Inputs

| Input | Meaning |
|---|---|
| Quality leader price | The highest price in the category (the premium leader) |
| Market leader price | The price of the best-selling product in the category |
| Cost leader price | The lowest competitor price in the category |

### Rules

```
Anchor        = quality leader price as an even integer
                (kept if already even; otherwise rounded up, then +1 if odd)
Safe price    = floor(market leader price × 0.90), then −1 if even   (minimum 1)
Saving        = Anchor − Safe price
Discount %    = round((1 − Safe price ÷ Quality leader price) × 100)
Safe zone     = Safe price … Market leader price
```

Inside the safe zone the product is below the market leader (encourages trial), above the cost leader (protects perceived value), and below the quality leader (leaves room to raise the price later).

### Break-even at the safe price

```
Contribution per unit = Safe price − Variable cost per unit
Break-even units      = ceil(Fixed costs ÷ Contribution per unit)
Contribution %        = Contribution ÷ Safe price × 100
Break-even revenue    = Break-even units × Safe price
```

---

## Usage

No dependencies — Python 3.8+.

```bash
python safe_pricing.py --product "EV sedan" \
  --quality 1250000 --market 980000 --cost 700000 \
  --fixed 2000000 --variable 600000
```

```
Product:            EV sedan
Premium anchor:     1,250,000
Safe price:         881,999
Customer saving:    368,001
Discount vs quality leader: 29%
Safe zone:          881,999 – 980,000
Break-even:         8 units / month
Contribution:       281,999 per unit (32.0%)
Break-even revenue: 7,055,992
```

As a library:

```python
from safe_pricing import calculate_safe_price, calculate_break_even

r = calculate_safe_price(1250000, 980000, 700000, "EV sedan")
print(r.anchor, r.safe_price, r.safe_zone)      # 1250000 881999 (881999, 980000)

b = calculate_break_even(r.safe_price, fixed_costs=2_000_000, variable_cost_per_unit=600_000)
print(b.units)                                   # 8
```

## Tests

```bash
python -m unittest discover -s tests
```

The implementation was additionally checked against the original JavaScript of the live calculator on 20,000 random inputs with zero mismatches.

---

## بالعربية — التسعير الآمن للمنتجات الجديدة

إطار تسعير من إعداد **د. مصطفى نوارج** — استشاري تسويق دولي، مدرّب شركات ومؤلف — لإطلاق منتج جديد بسعر:
يضمن المبيعات، دون أن يؤثر على صورتك الذهنية، ويمنحك الحرية في رفع سعرك مستقبلاً.

- **المرساة النفسية (Premium):** سعر قائد الجودة كرقم زوجي، يظهر مشطوباً بجوار سعرك.
- **السعر الترويجي (Promotion):** رقم فردي يُحدث أثر "الصفقة".
- **الاختراق الآمن (Penetration):** السعر الآمن = سعر قائد السوق × 90%.
- **المنطقة الآمنة:** بين السعر الآمن وسعر قائد السوق.

جرّب الأداة مجاناً: [التسعير الآمن — Marketing Planner Suite](https://marketingplannerai.mostafanawareg.com/marketing-template.html#tool-pricing-safe)

المقال المنهجي: [استراتيجية التسعير الآمن للمنتجات الجديدة](https://mostafanawareg.com/maqalat-tswiqia/%D8%A7%D9%84%D8%AA%D8%B3%D8%B9%D9%8A%D8%B1-%D8%A7%D9%84%D8%A2%D9%85%D9%86-%D9%84%D9%84%D9%85%D9%86%D8%AA%D8%AC%D8%A7%D8%AA-%D8%A7%D9%84%D8%AC%D8%AF%D9%8A%D8%AF%D8%A9/)

---

## Cite

If you use this framework in research, teaching, or a product, please cite it — GitHub's **"Cite this repository"** button uses [`CITATION.cff`](CITATION.cff).

> Nawareg, M. (2026). *Safe Pricing Framework (PPP)* (Version 1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.23231855

## Author

**Dr. Mostafa Nawareg** — [mostafanawareg.com](https://mostafanawareg.com) · [ORCID 0009-0007-8742-9270](https://orcid.org/0009-0007-8742-9270) · [Wikidata Q140563767](https://www.wikidata.org/wiki/Q140563767) · [LinkedIn](https://www.linkedin.com/in/dr-mostafa-nawareg)

## License

Code: [MIT](LICENSE). The PPP Safe Pricing methodology is © Dr. Mostafa Nawareg; attribution is required when it is reproduced or adapted.
