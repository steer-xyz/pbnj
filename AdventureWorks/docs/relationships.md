# 🔗 Relationships

This document describes the data model relationships that connect tables in the Power BI semantic model.

## Relationship Summary

| From Table | To Table | Cardinality | Direction | Active |
|-------------|----------|-------------|-----------|---------|
| Sales Data | Customer Lookup | M:1 | Single | Yes |
| Sales Data | Territory Lookup | M:1 | Single | Yes |
| Sales Data | Calendar Lookup | M:1 | Single | Yes |
| Sales Data | Product Lookup | M:1 | Single | Yes |
| Product Subcategories Lookup | Product Categories Lookup | M:1 | Single | Yes |
| Product Lookup | Product Subcategories Lookup | M:1 | Single | Yes |
| Sales Data | Calendar Lookup | M:1 | Single | No |
| Returns Data | Product Lookup | M:1 | Single | Yes |
| Returns Data | Calendar Lookup | M:1 | Single | Yes |
| Returns Data | Territory Lookup | M:1 | Single | Yes |

---

## Detailed Relationship Information

### Sales Data → Customer Lookup

**Connection Details:**
- **From Column**: CustomerKey
- **To Column**: CustomerKey
- **Cardinality**: M:1
- **Cross Filter Direction**: Single
- **Active**: Yes


**Business Impact:**

---

### Sales Data → Territory Lookup

**Connection Details:**
- **From Column**: TerritoryKey
- **To Column**: SalesTerritoryKey
- **Cardinality**: M:1
- **Cross Filter Direction**: Single
- **Active**: Yes


**Business Impact:**

---

### Sales Data → Calendar Lookup

**Connection Details:**
- **From Column**: OrderDate
- **To Column**: Date
- **Cardinality**: M:1
- **Cross Filter Direction**: Single
- **Active**: Yes


**Business Impact:**

---

### Sales Data → Product Lookup

**Connection Details:**
- **From Column**: ProductKey
- **To Column**: ProductKey
- **Cardinality**: M:1
- **Cross Filter Direction**: Single
- **Active**: Yes


**Business Impact:**

---

### Product Subcategories Lookup → Product Categories Lookup

**Connection Details:**
- **From Column**: ProductCategoryKey
- **To Column**: ProductCategoryKey
- **Cardinality**: M:1
- **Cross Filter Direction**: Single
- **Active**: Yes


**Business Impact:**

---

### Product Lookup → Product Subcategories Lookup

**Connection Details:**
- **From Column**: ProductSubcategoryKey
- **To Column**: ProductSubcategoryKey
- **Cardinality**: M:1
- **Cross Filter Direction**: Single
- **Active**: Yes


**Business Impact:**

---

### Sales Data → Calendar Lookup

**Connection Details:**
- **From Column**: StockDate
- **To Column**: Date
- **Cardinality**: M:1
- **Cross Filter Direction**: Single
- **Active**: No


**Business Impact:**

---

### Returns Data → Product Lookup

**Connection Details:**
- **From Column**: ProductKey
- **To Column**: ProductKey
- **Cardinality**: M:1
- **Cross Filter Direction**: Single
- **Active**: Yes


**Business Impact:**

---

### Returns Data → Calendar Lookup

**Connection Details:**
- **From Column**: ReturnDate
- **To Column**: Date
- **Cardinality**: M:1
- **Cross Filter Direction**: Single
- **Active**: Yes


**Business Impact:**

---

### Returns Data → Territory Lookup

**Connection Details:**
- **From Column**: TerritoryKey
- **To Column**: SalesTerritoryKey
- **Cardinality**: M:1
- **Cross Filter Direction**: Single
- **Active**: Yes


**Business Impact:**



## 🏗️ Data Model Structure

### Star Schema Analysis

#### Potential Fact Tables
- **Sales Data** (5 relationships)
- **Product Subcategories Lookup** (1 relationships)
- **Product Lookup** (1 relationships)
- **Returns Data** (3 relationships)

#### Dimension Tables  
- **Customer Lookup** (provides lookup/filter context)
- **Territory Lookup** (provides lookup/filter context)
- **Calendar Lookup** (provides lookup/filter context)
- **Product Lookup** (provides lookup/filter context)
- **Product Categories Lookup** (provides lookup/filter context)
- **Product Subcategories Lookup** (provides lookup/filter context)

### Relationship Types Distribution

- **One-to-Many**: 0 (standard dimension relationships)
- **Many-to-Many**: 0 (complex relationships)
- **One-to-One**: 0 (unique identifier relationships)

### Cross-Filter Direction

- **Single Direction**: 10 (standard filtering)
- **Both Directions**: 0 (bidirectional filtering)


## 🎯 Model Quality Assessment

### Strengths
- 9/10 relationships are active
- Mostly uses single-direction filtering (good for performance)

### Potential Improvements
- 1 inactive relationships may indicate model complexity


## 📐 Relationship Diagram

```
Sales Data
  ├── M:1 → Customer Lookup
  ├── M:1 → Territory Lookup
  ├── M:1 → Calendar Lookup
  ├── M:1 → Product Lookup
  ├── M:1 → Calendar Lookup
Product Subcategories Lookup
  ├── M:1 → Product Categories Lookup
Product Lookup
  ├── M:1 → Product Subcategories Lookup
Returns Data
  ├── M:1 → Product Lookup
  ├── M:1 → Calendar Lookup
  ├── M:1 → Territory Lookup
```

## 💡 Best Practices

### For Data Modelers
- Prefer star schema design with clear fact and dimension tables
- Use one-to-many relationships where possible
- Minimize many-to-many relationships
- Consider performance impact of bidirectional filtering
- Keep inactive relationships only when necessary for alternative relationship paths

### For Report Developers
- Understand how relationships affect filter context in DAX
- Be aware of active vs inactive relationships when writing measures
- Consider relationship direction when designing visuals
- Test filtering behavior across related tables

### For Business Users
- Relationships determine how data filtering works across visuals
- Connected tables allow for interactive filtering in reports
- Relationship quality directly impacts report accuracy and performance

---

*This documentation was generated automatically by PBNJ from your Power BI file.*