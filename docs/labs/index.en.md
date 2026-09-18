# Lab Guide

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/labs/index.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/labs/index.en.md)

This click-through lab uses each participant's own Microsoft tenant to configure the Industry IQ Platform. Review the tasks and acceptance criteria on each page before continuing.

## Learning Path

```mermaid
flowchart LR
    A[Prerequisites] --> B[Choose an industry]
    B --> C[Review existing sample data]
    C --> D[Fabric IQ]
    D --> E[Foundry IQ]
    E --> F[Work IQ]
    F --> G[Copilot Studio]
    G --> H[Completion check]
    H --> I[Optional: Custom MCP Backend]
```

| Content | Data Used | Outcome |
| --- | --- | --- |
| Main lab | Repository-provided `*-SYN-*` data | Validate Fabric IQ, Foundry IQ, and Work IQ from Copilot Studio |
| Optional: Custom MCP Backend | The same synthetic dataset | Validate startup of an MCP endpoint on Azure Container Apps |

!!! warning "Do Not Enter Real Customer Data"
    Do not use real records, credentials, secrets, or personal information in this lab. To design from real customer data, refer to the [Ontology design and implementation guide for real customer data](../Customer-Data-Ontology-Design-Guide.md), not this lab.

## How to Proceed

1. Complete the [prerequisites](prerequisites.md).
2. [Choose an Industry Pack](choose-industry.md).
3. Review the stored sample data.
4. Configure Fabric IQ, Foundry IQ, Work IQ, and Copilot Studio in order.
5. Confirm the **acceptance criteria** on each page.

[Continue to prerequisites](prerequisites.md){ .md-button .md-button--primary }
