# 📋 Tables

This document provides detailed information about all tables in the Power BI data model.

## Table Summary

| Table | Type | Hidden | Columns | Description |
|-------|------|--------|---------|-------------|
| Calendar Lookup | Table | No | 12 |  |
| Customer Lookup | Table | No | 20 |  |
| Product Categories Lookup | Table | No | 2 |  |
| Product Lookup | Table | No | 13 |  |
| Product Subcategories Lookup | Table | No | 3 |  |
| Returns Data | Table | No | 4 |  |
| Rolling Calendar | Table | No | 4 |  |
| Sales Data | Table | No | 11 |  |
| Territory Lookup | Table | No | 4 |  |

---

## Detailed Table Information

### Calendar Lookup


**Properties:**
- **Type**: Table
- **Hidden**: No
- **Column Count**: 12

#### Columns

| Column | Type | Description |
|--------|------|-------------|
| Date | Unknown |  |
| Day Name | Unknown |  |
| Start of Week | Unknown |  |
| Start of Month | Unknown |  |
| Month Name | Unknown |  |
| Month Number | Unknown |  |
| Start of Year | Unknown |  |
| Year | Unknown |  |
| Month Short | Unknown |  |
| Day of Week | Unknown |  |
| Weekend | Unknown |  |
| Start of Quarter | Unknown |  |

---

### Customer Lookup


**Properties:**
- **Type**: Table
- **Hidden**: No
- **Column Count**: 20

#### Columns

| Column | Type | Description |
|--------|------|-------------|
| CustomerKey | Unknown |  |
| Prefix | Unknown |  |
| FirstName | Unknown |  |
| LastName | Unknown |  |
| FullName | Unknown |  |
| BirthDate | Unknown |  |
| MaritalStatus | Unknown |  |
| Gender | Unknown |  |
| EmailAddress | Unknown |  |
| AnnualIncome | Unknown |  |
| TotalChildren | Unknown |  |
| EducationLevel | Unknown |  |
| Occupation | Unknown |  |
| HomeOwner | Unknown |  |
| DomainName | Unknown |  |
| Parent | Unknown |  |
| Customer Priority | Unknown |  |
| Income Level | Unknown |  |
| Education Category | Unknown |  |
| Birth Year | Unknown |  |

---

### Product Categories Lookup


**Properties:**
- **Type**: Table
- **Hidden**: No
- **Column Count**: 2

#### Columns

| Column | Type | Description |
|--------|------|-------------|
| ProductCategoryKey | Unknown |  |
| CategoryName | Unknown |  |

---

### Product Lookup


**Properties:**
- **Type**: Table
- **Hidden**: No
- **Column Count**: 13

#### Columns

| Column | Type | Description |
|--------|------|-------------|
| ProductKey | Unknown |  |
| ProductSubcategoryKey | Unknown |  |
| ProductSKU | Unknown |  |
| ProductName | Unknown |  |
| ModelName | Unknown |  |
| ProductDescription | Unknown |  |
| ProductColor | Unknown |  |
| ProductStyle | Unknown |  |
| ProductCost | Unknown |  |
| ProductPrice | Unknown |  |
| SKU Type | Unknown |  |
| DiscountPrice | Unknown |  |
| SKU Category | Unknown |  |

---

### Product Subcategories Lookup


**Properties:**
- **Type**: Table
- **Hidden**: No
- **Column Count**: 3

#### Columns

| Column | Type | Description |
|--------|------|-------------|
| ProductSubcategoryKey | Unknown |  |
| SubcategoryName | Unknown |  |
| ProductCategoryKey | Unknown |  |

---

### Returns Data


**Properties:**
- **Type**: Table
- **Hidden**: No
- **Column Count**: 4

#### Columns

| Column | Type | Description |
|--------|------|-------------|
| ReturnDate | Unknown |  |
| TerritoryKey | Unknown |  |
| ProductKey | Unknown |  |
| ReturnQuantity | Unknown |  |

---

### Rolling Calendar


**Properties:**
- **Type**: Table
- **Hidden**: No
- **Column Count**: 4

#### Columns

| Column | Type | Description |
|--------|------|-------------|
| Date | Unknown |  |
| Year | Unknown |  |
| Start of Quarter | Unknown |  |
| Start of Month | Unknown |  |

---

### Sales Data


**Properties:**
- **Type**: Table
- **Hidden**: No
- **Column Count**: 11

#### Columns

| Column | Type | Description |
|--------|------|-------------|
| OrderDate | Unknown |  |
| StockDate | Unknown |  |
| OrderNumber | Unknown |  |
| ProductKey | Unknown |  |
| CustomerKey | Unknown |  |
| TerritoryKey | Unknown |  |
| OrderLineItem | Unknown |  |
| OrderQuantity | Unknown |  |
| QuantityType | Unknown |  |
| Retail Price | Unknown |  |
| Revenue | Unknown |  |

---

### Territory Lookup


**Properties:**
- **Type**: Table
- **Hidden**: No
- **Column Count**: 4

#### Columns

| Column | Type | Description |
|--------|------|-------------|
| SalesTerritoryKey | Unknown |  |
| Region | Unknown |  |
| Country | Unknown |  |
| Continent | Unknown |  |



## 🔍 Analysis Notes

### Data Volume Insights

- **Total Tables**: 9
- **Visible Tables**: 9
- **Hidden Tables**: 0

### Table Categories



## 💡 Usage Tips

### For Developers
- Review hidden tables - they may contain important calculated tables
- Pay attention to table types for proper relationship modeling
- Consider column data types when writing DAX

### For Business Users
- Focus on visible tables as they represent your main data entities
- Table descriptions provide context for business understanding
- Column names often reflect business terminology

---

*This documentation was generated automatically by PBNJ from your Power BI file.*