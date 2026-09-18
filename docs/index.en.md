---
hide:
    - navigation
    - toc
---

<section class="lab-hero" markdown>
<div markdown>

# Industry IQ Platform Labs

These hands-on labs build industry knowledge from synthetic data and connect Microsoft Fabric IQ, Foundry IQ, and Work IQ to Copilot Studio.

<div class="lab-hero__actions" markdown>
[Start the labs](labs/index.md){ .md-button .md-button--primary }
[Pre-lab checklist](labs/prerequisites.md){ .md-button }
</div>

</div>
</section>

<!-- Solution icon PNGs: assets/images/solution-icons/{fabric-iq,foundry-iq,work-iq}.png -->
<div class="lab-grid" markdown>
<div class="lab-card" markdown>
<img class="lab-card__icon" src="assets/images/solution-icons/fabric-iq.png" alt="Fabric IQ">
**Fabric IQ**
<small>Bind synthetic Lakehouse data to Ontology entities and relationships.</small>
</div>
<div class="lab-card" markdown>
<img class="lab-card__icon" src="assets/images/solution-icons/foundry-iq.png" alt="Foundry IQ">
**Foundry IQ**
<small>Ingest industry documents into a Knowledge Source and validate answers with citations.</small>
</div>
<div class="lab-card" markdown>
<img class="lab-card__icon" src="assets/images/solution-icons/work-iq.png" alt="Work IQ">
**Work IQ**
<small>Review business context from synthetic Microsoft 365 content.</small>
</div>
</div>

## Lab Structure

| Content | Audience | Duration | Goal |
| --- | --- | ---: | --- |
| Main lab | Solution architects and Copilot Studio authors | 3-4 hours | Select one of five industries, then connect and validate three IQ layers with synthetic data |
| Custom MCP Backend | Advanced users and integration implementers | Optional | Validate an MCP Backend that exposes synthetic data on Azure Container Apps |

<figure class="lab-architecture">
    <a class="lab-architecture__link" href="assets/images/Architecture.png" target="_blank" rel="noopener" aria-label="Open the Industry IQ Platform architecture diagram at full size">
        <img src="assets/images/Architecture.png" alt="Industry IQ Platform architecture overview" width="4349" height="2190" loading="lazy" decoding="async">
    </a>
    <figcaption>Industry IQ Platform architecture</figcaption>
</figure>

!!! warning "Check Before You Begin"
    This lab uses only each participant's existing tenant and the synthetic data already stored in the repository. Do not use real customer data. If you cannot confirm the required licenses, Preview availability, tenant settings, capacity, and roles, do not begin the setup; consult your administrator.

## Existing References

- [Production environment setup guide](Production-Environment-Setup.md)
- [Ontology design and implementation guide for real customer data](Customer-Data-Ontology-Design-Guide.md)
- [Sample data regeneration guide](reference/Sample-Data-Regeneration-Guide.md)
- [IQ demo data deployment and reconfiguration runbook](evaluation/Demo-Data-Deployment-Runbook.md)
- [Copilot Studio IQ layer test execution and evaluation guide](evaluation/Copilot-Studio-IQ-Layer-Test-Catalog.md)
- [Troubleshooting](troubleshooting/README.md)

The main lab does not replace these documents. It divides UI procedures and acceptance criteria into short units and directs you to the references only for the details you need.
