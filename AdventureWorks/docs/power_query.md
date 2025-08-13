# ⚡ Power Query

This document details the data transformation and loading processes implemented in Power Query (M language).

## Query Summary

| Query | Steps | Description |
|-------|-------|-------------|
| Query_1 | 1 | Data transformation query |
| Query_2 | 1 | Data transformation query |
| Query_3 | 1 | Data transformation query |
| Query_4 | 1 | Data transformation query |
| Query_5 | 1 | Data transformation query |
| Query_6 | 1 | Data transformation query |
| Query_7 | 1 | Data transformation query |
| Query_8 | 1 | Data transformation query |
| Query_9 | 1 | Data transformation query |
| Query_10 | 1 | Data transformation query |

---

## Detailed Query Information

### Query_1


#### Transformation Steps
1. `let\n    Source = Csv.Document(File.Contents("...`

#### Complete M Code
```m
let\n    Source = Csv.Document(File.Contents("...
1                Product Lookup  
```

---

### Query_2


#### Transformation Steps
1. `let\n    Source = Csv.Document(File.Contents("...`

#### Complete M Code
```m
let\n    Source = Csv.Document(File.Contents("...
2     Product Categories Lookup  
```

---

### Query_3


#### Transformation Steps
1. `let\n    Source = Csv.Document(File.Contents("...`

#### Complete M Code
```m
let\n    Source = Csv.Document(File.Contents("...
3  Product Subcategories Lookup  
```

---

### Query_4


#### Transformation Steps
1. `let\n    Source = Csv.Document(File.Contents("...`

#### Complete M Code
```m
let\n    Source = Csv.Document(File.Contents("...
4               Customer Lookup  
```

---

### Query_5


#### Transformation Steps
1. `let\n    Source = Csv.Document(File.Contents("...`

#### Complete M Code
```m
let\n    Source = Csv.Document(File.Contents("...
5               Calendar Lookup  
```

---

### Query_6


#### Transformation Steps
1. `let\n    Source = Csv.Document(File.Contents("...`

#### Complete M Code
```m
let\n    Source = Csv.Document(File.Contents("...
6              Rolling Calendar  
```

---

### Query_7


#### Transformation Steps
1. `let\n    Source = #date(2023, 1, 1),\n    Cust...`

#### Complete M Code
```m
let\n    Source = #date(2023, 1, 1),\n    Cust...
7                    Sales Data  
```

---

### Query_8


#### Transformation Steps
1. `let\n    Source = Folder.Files("C:\Users\rich\...`

#### Complete M Code
```m
let\n    Source = Folder.Files("C:\Users\rich\...
8                  Returns Data  
```

---

### Query_9


#### Transformation Steps
1. `let\n    Source = Csv.Document(File.Contents("...`

#### Complete M Code
```m
let\n    Source = Csv.Document(File.Contents("...
9                Measures Table  
```

---

### Query_10


#### Transformation Steps
1. `let\n    Source = Table.FromRows(Json.Document...`

#### Complete M Code
```m
let\n    Source = Table.FromRows(Json.Document...
```






## Complete Power Query Code

<details>
<summary>Click to expand full M code</summary>

```m
                      TableName                                         Expression
0              Territory Lookup  let\n    Source = Csv.Document(File.Contents("...
1                Product Lookup  let\n    Source = Csv.Document(File.Contents("...
2     Product Categories Lookup  let\n    Source = Csv.Document(File.Contents("...
3  Product Subcategories Lookup  let\n    Source = Csv.Document(File.Contents("...
4               Customer Lookup  let\n    Source = Csv.Document(File.Contents("...
5               Calendar Lookup  let\n    Source = Csv.Document(File.Contents("...
6              Rolling Calendar  let\n    Source = #date(2023, 1, 1),\n    Cust...
7                    Sales Data  let\n    Source = Folder.Files("C:\Users\rich\...
8                  Returns Data  let\n    Source = Csv.Document(File.Contents("...
9                Measures Table  let\n    Source = Table.FromRows(Json.Document...
```

</details>


## 🔍 Data Flow Analysis

### Data Sources Identified

- CSV File
- JSON Data

### Common Transformations

*No specific transformations identified*

## 📊 Performance Considerations

### Optimization Tips
- **Query Folding**: Check if transformations can be pushed to the source
- **Data Types**: Ensure appropriate data types are set early
- **Filtering**: Apply filters as early as possible in the transformation chain
- **Column Selection**: Remove unnecessary columns early to reduce memory usage

### Potential Issues
- Complex transformations may impact refresh performance
- Multiple data sources may require careful connection management
- Large datasets may benefit from incremental refresh

## 💡 Usage Guidelines

### For Developers
- Review each query's transformation steps for optimization opportunities
- Understand data source connections and authentication requirements
- Consider error handling for robust data refresh processes
- Document any custom functions for team knowledge sharing

### For Business Users
- Power Query handles the "Extract, Transform, Load" (ETL) process
- Each query represents a data preparation workflow
- Parameters allow for flexible data source configuration
- Refresh schedules should align with source data update frequencies

---

*This documentation was generated automatically by PBNJ from your Power BI file.*