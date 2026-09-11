"""Generate scenario-rich synthetic prompt libraries for all Industry Packs."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPTS: dict[str, dict[str, list[str]]] = {
    "manufacturing": {
        "quality-investigation": [
            "Summarize the highest-severity open quality issues and their affected factories.",
            "Find recurring defects by part and recommend a human-reviewed investigation plan.",
            "Compare defect rates across factories for the latest reporting period.",
            "Trace the supplier history for the part with the most critical issues.",
            "Identify quality issues without an engineering change and explain the risk.",
            "Which production lines are associated with the most unresolved issues?",
            "Prepare an evidence-based briefing for the quality engineering lead.",
            "Find issues whose defect rate exceeds the review threshold and group them by supplier.",
            "Summarize the timeline of the latest issue from detection through engineering review.",
            "What additional information is needed before a quality issue can be closed?",
        ],
        "supplier-risk": [
            "Rank suppliers by reliability score and related unresolved quality issues.",
            "Identify parts supplied by suppliers with repeated quality signals.",
            "Compare supplier risk across factories without making an automatic decision.",
            "Find the supplier associated with the largest number of affected parts.",
            "Summarize open supplier quality actions for management review.",
            "Which suppliers need a manual audit recommendation based on current data?",
            "Trace a part from supplier to production line and quality issue.",
            "Identify gaps in supplier history for the latest critical issue.",
            "Create a supplier review agenda from the highest-risk records.",
            "Explain uncertainty in the supplier risk ranking.",
        ],
        "engineering-change": [
            "List proposed engineering changes that address high-severity issues.",
            "Find engineering changes that are still in progress and summarize blockers.",
            "Compare implemented changes with their originating quality issues.",
            "Which issues have no corresponding engineering change?",
            "Prepare a human approval checklist for engineering change review.",
            "Summarize changes created during the latest reporting period.",
            "Identify engineering changes that may affect multiple production lines.",
            "Find unresolved issues related to an implemented change.",
            "Explain which facts support prioritizing an engineering change.",
            "Draft questions for the engineering lead before approval.",
        ],
        "factory-operations": [
            "Summarize quality issues observed at each factory.",
            "Compare production lines by unresolved issue count.",
            "Find factories with both high defect rates and open issues.",
            "Prepare an operations review for the factory quality lead.",
            "Identify missing factory or production-line relationships.",
            "Which factory should be reviewed first and why?",
            "Trace a quality issue to its factory and production line.",
            "Summarize operational trends without inferring unsupported causes.",
            "Find factories with no recent quality records.",
            "List follow-up questions for a factory inspection.",
        ],
        "governance": [
            "Check whether the requested action requires a quality engineer review.",
            "Separate confirmed facts from recommendations in this quality investigation.",
            "Identify prohibited automatic actions in the current scenario.",
            "Explain which evidence is missing before a recall decision.",
            "Generate a traceable summary with source records for audit review.",
            "Flag conflicting quality records and explain the conflict.",
            "Recommend a human-in-the-loop checkpoint for this case.",
            "Identify data freshness concerns in the quality dataset.",
            "List assumptions used in the investigation.",
            "Produce an audit-ready investigation summary without approving an action.",
        ],
    },
    "financial-services": {
        "fraud-investigation": [
            "Summarize the highest-risk open fraud cases.", "Investigate the latest flagged transaction.",
            "Find transactions with unusually high amounts and explain the evidence.", "Trace a fraud case to its account and customer segment.",
            "Compare fraud cases by status and risk score.", "Identify cases that need manual escalation.",
            "Summarize the timeline for the most recent investigation.", "Find accounts with multiple flagged transactions.",
            "Prepare an investigator briefing with citations to source records.", "What information is missing before closing this case?",
        ],
        "transaction-monitoring": [
            "Identify transaction patterns that warrant review.", "Group flagged transactions by currency and transaction type.",
            "Find accounts with repeated high-value activity.", "Summarize monitoring signals by customer segment.",
            "Compare recent transaction activity with the available fraud cases.", "Find transactions with inconsistent case status.",
            "Prepare a transaction monitoring review agenda.", "Explain uncertainty in the current risk signals.",
            "Identify data quality gaps in transaction records.", "List questions for the compliance analyst.",
        ],
        "customer-and-account": [
            "Summarize accounts associated with the latest fraud case.", "Find customers with multiple accounts under investigation.",
            "Compare account types across customer segments.", "Trace a transaction from customer to account and case.",
            "Identify accounts with no recent transaction activity.", "Prepare a customer risk context without making a decision.",
            "Find orphaned transactions without a valid account.", "Summarize account opening periods for investigated accounts.",
            "Explain which customer facts are confirmed.", "List missing customer context for manual review.",
        ],
        "compliance-review": [
            "Prepare a compliance review summary for open cases.", "Identify cases that need enhanced review.",
            "Separate evidence from investigator recommendations.", "Find cases with conflicting status and risk signals.",
            "List required human approvals for the proposed next steps.", "Summarize policy-relevant facts without exposing sensitive data.",
            "Identify stale or incomplete case records.", "Create an audit trail for the latest investigation.",
            "Explain why an automatic account action is not appropriate.", "Draft questions for the compliance committee.",
        ],
        "portfolio-analytics": [
            "Compare transaction volume across customer segments.", "Summarize fraud case rates by account type.",
            "Find segments with increasing investigation activity.", "Identify the largest concentration of open risk.",
            "Prepare a management summary of portfolio signals.", "Explain limitations in the available sample data.",
            "Find trends by currency and transaction type.", "Compare closed and open case distributions.",
            "List recommended analysis follow-ups for an analyst.", "Provide a traceable portfolio snapshot.",
        ],
    },
    "retail": {
        "inventory": [
            "Find products below reorder point across all stores.", "Summarize the most urgent inventory shortages.",
            "Compare stock coverage by store and product category.", "Identify stores with repeated low-stock records.",
            "Trace a demand signal to the affected inventory record.", "Prepare a replenishment review without placing an order.",
            "Find products with high stock but declining demand.", "List inventory records with missing product or store references.",
            "Explain which shortages need manual confirmation.", "Summarize inventory risk for the operations lead.",
        ],
        "demand-analysis": [
            "Investigate the latest demand signals and recommend analysis steps.", "Compare demand trends by store and product.",
            "Find products with sharp demand increases.", "Identify declining demand signals with excess inventory.",
            "Summarize seasonal signals for the planning team.", "Trace a demand signal to stock and recent orders.",
            "Find demand signals with incomplete context.", "Prepare a demand review agenda.",
            "Explain uncertainty in the demand trend data.", "List questions for the merchandising analyst.",
        ],
        "orders": [
            "Summarize pending replenishment orders by store.", "Find orders associated with low-stock products.",
            "Compare order quantities across stores.", "Identify cancelled orders that may affect inventory.",
            "Trace an order from store to product and demand signal.", "Prepare an order review without automatically changing status.",
            "Find products with no recent order activity.", "Summarize order status distribution.",
            "Identify inconsistent order and inventory records.", "Draft follow-up questions for supply planning.",
        ],
        "store-operations": [
            "Compare store inventory risk across regions.", "Find stores with the largest number of shortages.",
            "Summarize operational actions needed by store.", "Identify stores with no recent demand signals.",
            "Prepare a regional inventory briefing.", "Trace a shortage to its store, product, and order context.",
            "Find stores with unusual order patterns.", "Explain limitations of the current store sample.",
            "List high-priority store follow-ups.", "Create an evidence-based operations summary.",
        ],
        "governance": [
            "Separate confirmed inventory facts from recommendations.", "Identify actions that require manager approval.",
            "Flag data freshness and duplicate-record concerns.", "Explain why an automatic order change should not be made.",
            "Prepare an audit-friendly replenishment summary.", "Identify missing evidence for a stockout decision.",
            "List assumptions used in the inventory analysis.", "Find conflicting stock and order records.",
            "Recommend a human review checkpoint.", "Summarize the source records used in the analysis.",
        ],
    },
    "healthcare": {
        "case-history": [
            "Review the latest synthetic encounter and identify documentation gaps.", "Summarize encounter history for a synthetic patient.",
            "Find encounters with incomplete provider or patient references.", "Trace a clinical event to its encounter.",
            "Compare encounter reasons over the reporting period.", "Prepare a care coordination review without clinical diagnosis.",
            "Find patients with repeated encounters.", "Identify missing context for a documentation review.",
            "Summarize administrative follow-up actions.", "List questions for the care coordinator.",
        ],
        "care-coordination": [
            "Find encounters requiring care coordination follow-up.", "Summarize provider involvement by encounter.",
            "Compare care coordination records across synthetic patients.", "Identify unresolved administrative events.",
            "Trace a patient record to provider and encounter context.", "Prepare a coordination meeting agenda.",
            "Find encounters without recent clinical events.", "Explain uncertainty in the administrative data.",
            "List missing documentation evidence.", "Draft non-clinical follow-up questions.",
        ],
        "documentation-quality": [
            "Identify encounters with potential documentation completeness gaps.", "Compare event coverage by provider role.",
            "Find clinical events without a valid encounter reference.", "Summarize recent documentation patterns.",
            "Prepare a quality review using only synthetic administrative data.", "Find repeated event types by encounter.",
            "Explain which facts are confirmed and which are unknown.", "List records needing manual documentation review.",
            "Identify stale encounter records.", "Create an audit-ready documentation summary.",
        ],
        "capacity-planning": [
            "Summarize encounter volume by provider role.", "Find periods with unusually high encounter counts.",
            "Compare administrative workload across providers.", "Identify capacity signals for care coordination.",
            "Prepare a staffing discussion using synthetic data only.", "Find providers with no recent encounters.",
            "Explain limitations in the capacity sample.", "Trace workload to encounter reason.",
            "List planning questions for the operations team.", "Create a non-clinical workload snapshot.",
        ],
        "safety-and-governance": [
            "Confirm that this response does not make a clinical diagnosis.", "Separate administrative facts from recommendations.",
            "Identify required human review points.", "Flag sensitive-data handling concerns in the workflow.",
            "Prepare a privacy-aware synthetic case summary.", "List unsupported assumptions in the analysis.",
            "Explain why an automated clinical action must not be taken.", "Identify data-quality risks.",
            "Create a traceable administrative review.", "Draft questions for a qualified reviewer.",
        ],
    },
    "public-sector": {
        "case-review": [
            "Summarize the highest-priority open cases.", "Investigate the latest synthetic administrative case.",
            "Find cases awaiting a decision or more information.", "Trace a case to citizen, agency, and application context.",
            "Compare case status by agency.", "Prepare a case review without making an eligibility decision.",
            "Identify cases with missing application context.", "Summarize the latest case timeline.",
            "List unresolved review actions.", "Draft questions for the caseworker.",
        ],
        "application-processing": [
            "Find applications pending review by agency.", "Compare application types and statuses.",
            "Identify cases with multiple applications.", "Summarize application processing bottlenecks.",
            "Find applications without a valid case reference.", "Prepare a processing review agenda.",
            "Trace an application to its case and agency.", "Explain uncertainty in the application sample.",
            "List missing evidence for manual review.", "Create a status summary for operations leadership.",
        ],
        "agency-operations": [
            "Compare case workload across agencies.", "Find agencies with the largest open-case backlog.",
            "Summarize case types by agency.", "Identify agencies with no recent applications.",
            "Prepare an inter-agency workload briefing.", "Find unusual case status distributions.",
            "Explain the limitations of the synthetic workload data.", "Trace workload to agency and case type.",
            "List operational follow-up questions.", "Create an evidence-based agency summary.",
        ],
        "service-review": [
            "Identify cases that need a manual service review.", "Find cases awaiting citizen documents.",
            "Summarize pending decisions without recommending eligibility.", "Compare open and closed cases by case type.",
            "Prepare a service review checklist.", "Identify conflicting case and application statuses.",
            "Find stale cases requiring attention.", "List evidence needed before a decision.",
            "Explain confirmed facts versus assumptions.", "Draft questions for an authorized reviewer.",
        ],
        "governance": [
            "Separate case facts from recommendations.", "Identify actions that require authorized human approval.",
            "Prepare an audit-ready case summary.", "Flag privacy and access-control concerns.",
            "Identify data-quality gaps in citizen and case records.", "Explain why an automatic decision is not appropriate.",
            "List assumptions used in the review.", "Find records with inconsistent relationships.",
            "Recommend a human-in-the-loop checkpoint.", "Summarize source records used for this response.",
        ],
    },
}


def yaml_quote(text: str) -> str:
    return '"' + text.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main() -> None:
    for pack_id, scenarios in PROMPTS.items():
        lines = ["# Enterprise-scale synthetic prompts; all values are safe test content.", "prompts:"]
        index = 1
        for scenario, texts in scenarios.items():
            for text in texts:
                lines.extend([
                    f"  - id: enterprise-{scenario}-{index:02d}",
                    f"    text: {yaml_quote(text)}",
                    f"    scenario: {pack_id}-{scenario}",
                ])
                index += 1
        output = REPO_ROOT / "industry-packs" / pack_id / "sample-data" / "prompts" / "enterprise_prompts.yaml"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{pack_id}: {index - 1} prompts")


if __name__ == "__main__":
    main()
