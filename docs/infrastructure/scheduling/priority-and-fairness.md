# Priority and Fairness Scheduling Guide

## Priority Classes & Dynamic Aging
Base scores:
- `CRITICAL`: 1000.0
- `HIGH`: 500.0
- `NORMAL`: 100.0
- `LOW`: 50.0
- `BACKGROUND`: 10.0
- `MAINTENANCE`: 1.0

Dynamic score formula:
$$\text{Score} = \text{BaseScore} + (\text{WaitTimeSeconds} \times \text{AgingRate})$$

## Multi-Tenant Fairness
`FairnessScheduler` applies Deficit Fair Share queue interleaving across tenants and penalizes tenants exceeding their fair share ratio to prevent batch tenant starvation.
