# Lab 5: Configure a Copilot Studio Agent

Estimated time: 30 minutes

Connect each IQ layer to the agent separately and prepare it for testing. Do not run evaluation questions on this page.

## 1. Prepare the Agent

1. Create a lab agent in Copilot Studio.
2. Set the contents of [`industry-packs/<pack>/agents/investigation_agent_instructions.md`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" } as the agent instructions.
3. Review the instructions' rules for source separation, zero results, tool failures, and human approval.
4. Record the agent name, environment, connection user, and selected industry.

<figure class="lab-image-placeholder" markdown>
    **Image replacement location: Agent Instructions**
    `assets/images/labs/copilot-studio-instructions.png`
    <figcaption>Replace with a screen showing the selected industry's instructions.</figcaption>
</figure>

## 2. Connect Tools Individually

Add the tools one at a time in the following order.

1. Under **Tools > Add Tool > Fabric IQ MCP (Preview)**, create a new connection, enter the Fabric workspace ID and Ontology item ID, and select **Create > Add**.
2. Under **Tools > Add Tool > Foundry IQ**, select an authentication method, select the Knowledge Base created in Lab 3, and select **Add to agent**.
3. Under **Tools > Add Tool > Model Context Protocol > Work IQ (preview)**, create a connection for the test user and select **Add and Configure**.

Do not identify a connection by the tool display name alone. Confirm that the workspace, Ontology, Knowledge Base, and connection user match the intended values.

!!! warning "Work IQ Connection Screen"
    The Work IQ connection path, display names, and availability requirements may change. If the options above do not appear, do not enter a generic Remote MCP URL based on assumptions. Review the current [official procedure](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-work-iq) and tenant policy as of the date of the lab.

<figure class="lab-image-placeholder" markdown>
    **Image replacement location: List of three IQ tools**
    `assets/images/labs/copilot-studio-tools.png`
    <figcaption>Replace with a screen showing Fabric IQ, Foundry IQ, Work IQ, and each connection.</figcaption>
</figure>

## 3. Pre-Test Configuration Check

1. Open each of the three tools and record its destination and authentication user.
2. Save the agent instructions and record the version as an unpublished development version.
3. Confirm that tool names, descriptions, and destinations contain no values from another industry.
4. Continue to [agent testing](06-agent-test.md) without changing the configuration.

## Acceptance Criteria

- [ ] All three IQ tools have been added to the agent.
- [ ] The Fabric workspace, Ontology, Knowledge Base, and connection user match the recorded values.
- [ ] The selected industry's agent instructions are saved.
- [ ] You recorded the agent version before testing.

If a connection or save operation fails, resolve it using [troubleshooting](../../troubleshooting/README.md) before proceeding to testing.

[Back: Work IQ](04-work-iq.md){ .md-button }
[Next: Test the agent](06-agent-test.md){ .md-button .md-button--primary }
