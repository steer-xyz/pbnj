# 📊 Measures

This document contains all DAX measures and their formulas from the Power BI data model.

## Measures Summary

| Measure | Table | Description |
|---------|-------|-------------|
| Order Quantity | Measures Table |  |
| Quantity Returned | Measures Table |  |
| Average Retail Price | Measures Table |  |
| Total Returns | Measures Table |  |
| Total Orders | Measures Table |  |
| Total Customers | Measures Table |  |
| Return Rate | Measures Table |  |
| Quantity Sold | Measures Table |  |
| Bulk Orders | Measures Table |  |
| Weekend Orders | Measures Table |  |
| Bike Returns | Measures Table |  |
| Bikes Sold | Measures Table |  |
| Bike Return Rate | Measures Table |  |
| All Orders | Measures Table |  |
| % of All Orders | Measures Table |  |
| Overall Average Price | Measures Table |  |
| All Returns | Measures Table |  |
| % of All Returns | Measures Table |  |
| High Ticket Orders | Measures Table |  |
| Total Revenue | Measures Table |  |
| Total Cost | Measures Table |  |
| Total Profit | Measures Table |  |
| YTD Revenue | Measures Table |  |
| Previous Month Revenue | Measures Table |  |
| Revenue Target | Measures Table |  |
| 10-Day Rolling Revenue | Measures Table |  |
| Previous Month Orders | Measures Table |  |
| 90-Day Rolling Profit | Measures Table |  |
| Order Target | Measures Table |  |
| Revenue Per Customer | Measures Table |  |
| Previous Month Returns | Measures Table |  |
| Profit Target | Measures Table |  |
| Previous Month Profit | Measures Table |  |
| Order Target Gap | Measures Table |  |
| Profit Target Gap | Measures Table |  |
| Revenue Target Gap | Measures Table |  |
| Parameter Value | Parameter |  |
| Price Adjustment Percentage Value | Price Adjustment Percentage |  |
| Adjusted Price | Measures Table |  |
| Adjusted Revenue | Measures Table |  |
| Adjusted Profit | Measures Table |  |

---

## Detailed Measure Definitions

### Order Quantity


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

SUM(
    'Sales Data'[OrderQuantity]
) 
```



---

### Quantity Returned


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

SUM(
    'Returns Data'[ReturnQuantity]
)
```



---

### Average Retail Price


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

AVERAGE(
    'Product Lookup'[ProductPrice] 
)
```



---

### Total Returns


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

COUNT(
    'Returns Data'[ReturnQuantity]
)
```



---

### Total Orders


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

DISTINCTCOUNT(
    'Sales Data'[OrderNumber]
)
```



---

### Total Customers


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

DISTINCTCOUNT(
    'Sales Data'[CustomerKey]
)
```



---

### Return Rate


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

DIVIDE(
    [Quantity Returned],
    [Quantity Sold],
    "No Sales"
)
```



---

### Quantity Sold


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

SUM(
    'Sales Data'[OrderQuantity]
)
```



---

### Bulk Orders


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Orders],
    'Sales Data'[OrderQuantity] > 1
)
```



---

### Weekend Orders


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Orders],
    'Calendar Lookup'[Weekend] = "Weekend"
)
```



---

### Bike Returns


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Returns],
    'Product Categories Lookup'[CategoryName] = "Bikes"
)
```



---

### Bikes Sold


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Quantity Sold],
    'Product Categories Lookup'[CategoryName] = "Bikes"
)
```



---

### Bike Return Rate


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Return Rate],
    'Product Categories Lookup'[CategoryName] = "Bikes"
)
```



---

### All Orders


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Orders],
    ALL(
        'Sales Data'
    )
)
```



---

### % of All Orders


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

DIVIDE(
    [Total Orders],
    [All Orders]
)

```



---

### Overall Average Price


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Average Retail Price],
    ALL(
        'Product Lookup'
    )
)
```



---

### All Returns


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Returns],
    ALL(
        'Returns Data'
    )
)
```



---

### % of All Returns


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

DIVIDE(
    [Total Returns],
    [All Returns]
)
```



---

### High Ticket Orders


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Orders],
    FILTER(
        'Product Lookup','Product Lookup'[ProductPrice] > [Overall Average Price]
    )
)
```



---

### Total Revenue


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

SUMX(
    'Sales Data',
    'Sales Data'[OrderQuantity]
    *
    RELATED(
        'Product Lookup'[ProductPrice]
    )
)
```



---

### Total Cost


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

SUMX(
    'Sales Data',
    'Sales Data'[OrderQuantity] *
    RELATED(
        'Product Lookup'[ProductCost]
    )
)
```



---

### Total Profit


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

[Total Revenue]-[Total Cost]
```



---

### YTD Revenue


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Revenue],
    DATESYTD(
        'Calendar Lookup'[Date]
    )
)
```



---

### Previous Month Revenue


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Revenue],
    DATEADD(
        'Calendar Lookup'[Date],
        -1,
        MONTH
    )
)
```



---

### Revenue Target


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

[Previous Month Revenue] * 1.1
```



---

### 10-Day Rolling Revenue


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Revenue],
    DATESINPERIOD(
        'Calendar Lookup'[Date],
        MAX(
            'Calendar Lookup'[Date]
        ),
        -10,
        DAY
    )
)
```



---

### Previous Month Orders


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Orders],
    DATEADD(
        'Calendar Lookup'[Date],
        -1,
        MONTH
    )
)
```



---

### 90-Day Rolling Profit


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Profit],
    DATESINPERIOD(
        'Calendar Lookup'[Date],
        LASTDATE(
            'Calendar Lookup'[Date]
        ),
        -90,
        DAY
    )
)
```



---

### Order Target


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

[Previous Month Orders] * 1.1
```



---

### Revenue Per Customer


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

DIVIDE(
    [Total Revenue],
    [Total Customers]
)
```



---

### Previous Month Returns


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Returns],
    DATEADD(
        'Calendar Lookup'[Date],
        -1,
        MONTH
    )
)
```



---

### Profit Target


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

[Previous Month Profit] * 1.1
```



---

### Previous Month Profit


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

CALCULATE(
    [Total Profit],
    DATEADD(
        'Calendar Lookup'[Date],
        -1,
        MONTH
    )
)
```



---

### Order Target Gap


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax
[Total Orders] - [Order Target]
```



---

### Profit Target Gap


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax
[Total Profit] - [Profit Target]
```



---

### Revenue Target Gap


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax
[Total Revenue] - [Revenue Target]
```



---

### Parameter Value


**Properties:**
- **Table**: Parameter
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax
SELECTEDVALUE('Parameter'[Parameter])
```



---

### Price Adjustment Percentage Value


**Properties:**
- **Table**: Price Adjustment Percentage
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax
SELECTEDVALUE('Price Adjustment Percentage'[Price Adjustment Percentage], 0)
```



---

### Adjusted Price


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

[Average Retail Price] * (1 + 'Price Adjustment Percentage'[Price Adjustment Percentage Value])
```



---

### Adjusted Revenue


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

SUMX(
    'Sales Data',
    'Sales Data'[OrderQuantity]
    *
    [Adjusted Price]
)
```



---

### Adjusted Profit


**Properties:**
- **Table**: Measures Table
- **Data Type**: Unknown
- **Format**: Auto

#### DAX Formula
```dax

[Adjusted Revenue]-[Total Cost]
```





## 🎯 Measure Categories

### Key Performance Indicators
- **Total Returns**: 
- **Total Orders**: 
- **Total Customers**: 
- **Total Revenue**: 
- **Total Cost**: 
- **Total Profit**: 

### Calculated Ratios
- **Return Rate**: 
- **Bike Return Rate**: 
- **% of All Orders**: 
- **% of All Returns**: 
- **Price Adjustment Percentage Value**: 

## 📈 DAX Patterns Analysis

### Common Functions Used
- **SUM()**: Used for aggregating numerical values
- **CALCULATE()**: Used for filtered calculations
- **SUMX()**: Used for row-by-row calculations
- **FILTER()**: Used for applying filters
- **RELATED()**: Used for accessing related table data

### Complexity Assessment

- **Simple Measures**: 41 (basic aggregations)  
- **Complex Measures**: 0 (advanced DAX)


## 💡 Best Practices

### For DAX Development
- Use CALCULATE() for most filtered aggregations
- Consider performance implications of complex measures
- Document business logic in measure descriptions
- Use meaningful measure names that reflect business terminology

### For Business Users
- Measures represent the calculated metrics in your reports
- Each measure follows a specific business rule encoded in DAX
- Measure names should be intuitive for report consumers

---

*This documentation was generated automatically by PBNJ from your Power BI file.*