# Logistics Analysis Summary

## Objective

Analyze package delivery performance, shipping costs, providers, shipping methods, and destination provinces using a synthetic logistics dataset.

## Data Preparation

The dataset was intentionally modified with common data quality issues, including missing values, duplicate IDs, invalid values, inconsistent provider names, unrealistic weights, and inconsistent dates.

A Python cleaning pipeline was used to standardize the data, remove invalid records, handle missing values, and create derived metrics such as `delivery_days`, `delay_days`, and `on_time`.

The final dataset contains **9,885 packages** from January to September 2026.

## Key Findings

### 1. Shipping cost vs delivery speed

Express shipping has the highest average cost at **$34.12** and the shortest average delivery time at **7.25 days**. Economy shipping costs **$16.49** and takes **9.63 days** on average.

### 2. Provider performance

Amazon handles the highest package volume and has the shortest average delivery time at **7.67 days**. Temu has the lowest average shipping cost at **$16.02** but the longest average delivery time at **9.55 days**.

### 3. Geographical differences

Delivery performance varies across provinces. Guanacaste has the longest average delivery time at **10.09 days**, while Heredia has the shortest at **7.99 days** and the highest on-time rate at **40.53%**.

### 4. Weight and shipping cost

Package weight has a positive relationship with shipping cost, with a Pearson correlation of approximately **0.69**.

### 5. Delivery attempts

Packages requiring three delivery attempts have the highest average delay and the lowest on-time delivery rate, suggesting an association between repeated delivery attempts and poorer delivery performance.

### 6. Package volume

Monthly package volume remains relatively stable throughout the analyzed period, ranging from **1,005 to 1,146 packages** per month. July has the highest volume and February the lowest.

## Limitations

The dataset is synthetic and was created for learning and portfolio purposes. The results should not be interpreted as actual operational performance from Amazon, Temu, AliExpress, or other logistics providers.
