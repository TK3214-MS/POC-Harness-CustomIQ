# Synthetic Sample Data Lab

Estimated time: 3-4 hours

Configure the selected Industry Pack step by step, from reviewing the stored sample data through asking cross-layer questions in Copilot Studio.

<div class="lab-step-strip" markdown>
<div>Local setup</div>
<div>Fabric IQ</div>
<div>Foundry IQ</div>
<div>Work IQ</div>
<div>Copilot Studio</div>
<div>Agent test</div>
<div>Complete</div>
</div>

## Lab Structure

| Lab | Task | Estimate |
| --- | --- | ---: |
| 1 | Sample data and local validation | 15 minutes |
| 2 | Configure entities and relationships in Fabric IQ | 60 minutes |
| 3 | Register knowledge in Foundry IQ | 40 minutes |
| 4 | Place synthetic M365 content in Work IQ | 30 minutes |
| 5 | Configure a Copilot Studio agent | 30 minutes |
| 6 | Independently test and evaluate the agent | 30-45 minutes |
| 7 | Confirm completion and decide on cleanup | 20 minutes |

Each lab assumes the previous lab succeeded. Do not proceed to cross-layer questions while zero-result or connection failures remain unresolved.

## Sources Used

Replace the selected `<pack>` with one of the available values.

- Fabric: [`industry-packs/<pack>/sample-data/fabric/*.csv`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }
- Foundry: [`industry-packs/<pack>/knowledge/*.md`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }
- Work IQ: [`industry-packs/<pack>/sample-data/work-iq/*.md`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }
- Ontology definition: [`industry-packs/<pack>/ontology/entities.yaml`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }
- Agent instructions: [`industry-packs/<pack>/agents/investigation_agent_instructions.md`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }

[Start Lab 1](01-local-setup.md){ .md-button .md-button--primary }
