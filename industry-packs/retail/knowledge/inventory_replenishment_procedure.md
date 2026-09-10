# Inventory Replenishment Procedure (Synthetic Reference Document)

> This is a synthetic reference document created for the Industry IQ Platform Accelerator demo. It does not represent a real retailer's procedure.

## Reorder Trigger

When `quantity_on_hand` falls below `reorder_point` for a Product at a Store, the system flags it for review. A reorder is never placed automatically - an inventory manager must approve it.

## Demand Signal Handling

A `spike` signal combined with low on-hand quantity should be prioritized for review, since it indicates rising demand against limited supply.
