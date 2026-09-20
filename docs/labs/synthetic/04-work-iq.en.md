# Lab 4: Work IQ

Estimated time: 30 minutes

Place synthetic content from the selected Industry Pack in Microsoft 365 so it can be retrieved under the test user's existing permissions.

## 1. Prepare the Destination

Use a SharePoint site, Teams team/channel, Exchange test mailbox, and calendar dedicated to the lab. Do not mix the content with existing production-user content.

Before using Work IQ, have an administrator confirm tenant enablement, usage-based billing, spending policy, and MCP policy against current official procedures as of the date of the lab. Keep initial validation read-only; do not permit create, update, or send operations.

## 2. Place the Synthetic Content

Open [`industry-packs/<pack>/sample-data/work-iq/*.md`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" } and place each document according to its purpose.

| Content | Example Destination |
| --- | --- |
| Case and review materials | SharePoint document library |
| `teams-thread` | Synthetic post in a Teams channel |
| `email` | Synthetic email between test mailboxes |
| `meeting` | Meeting description or minutes in a test calendar |

Do not merely place the Markdown files. Create content intended for email or meeting validation in the corresponding Microsoft 365 workload. Retain the `*-SYN-*` ID in each record.

1. Save case and review materials in the SharePoint document library.
2. Post the `teams-thread` content in the lab-only Teams channel.
3. Send the `email` content between test mailboxes.
4. Add the `meeting` content to a test calendar meeting body or its minutes.
5. Confirm that the same `*-SYN-*` starting ID reviewed in the Fabric lab appears in each content item's subject or body.

<figure class="lab-evidence">
    <a class="lab-evidence__link" href="../../../../assets/images/labs/work-iq-synthetic-content.png" target="_blank" rel="noopener" aria-label="Open the synthetic Microsoft 365 content image at full size">
        <img src="../../../../assets/images/labs/work-iq-synthetic-content.png" alt="Microsoft 365 content showing a synthetic ID in Teams or SharePoint" loading="lazy" decoding="async">
    </a>
    <figcaption>Synthetic content placed in Microsoft 365</figcaption>
</figure>

## 3. Confirm Permissions

1. Sign in to Microsoft 365 as the test user used in Copilot Studio.
2. Confirm that you can open the SharePoint documents, Teams posts, emails, and meetings through their standard interfaces.
3. Confirm that the test user cannot open another lab area for which they do not have permission.

This is not a procedure for uploading files to Work IQ as a separate search index. The acceptance criterion is that the Copilot Studio connection user can retrieve the target content within their existing Microsoft 365 permissions.

<figure class="lab-evidence">
    <a class="lab-evidence__link" href="../../../../assets/images/labs/work-iq-permission-check.png" target="_blank" rel="noopener" aria-label="Open the test user access check image at full size">
        <img src="../../../../assets/images/labs/work-iq-permission-check.png" alt="Screen showing that the test user can open permitted content" loading="lazy" decoding="async">
    </a>
    <figcaption>Test user access check</figcaption>
</figure>

## Acceptance Criteria

- [ ] You placed the required synthetic content in SharePoint, Teams, Exchange, and the calendar.
- [ ] Each record includes its starting `*-SYN-*` ID.
- [ ] The test user can view only the target records.

Confirm Work IQ availability requirements, billing, policies, and write capabilities against current official documentation and tenant settings as of the date of the lab.

[Back: Foundry IQ](03-foundry-iq.md){ .md-button }
[Next: Copilot Studio](05-copilot-studio.md){ .md-button .md-button--primary }
