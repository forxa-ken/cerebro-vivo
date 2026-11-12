# Auditor report (template; spec 044)

Filled in by the auditor (internal or external) and handed to whoever asked for the review. **It only warns: it does not change code or block the closing.** Every finding carries file and line; what could not be checked goes apart, never stated as fact.

- **Mode:** general / closing / spec closing
- **Who audits:** (model and effort; if an external AI took part, which one)
- **What was reviewed:** (folder, diff or files)
- **Verdict:** fit / fit with remarks / returned

## Quality
1. **[high|medium|low] `file:line`** — what fails and why it breaks the requirement. *Checked by running: yes/no.*

## Resource consumption
1. **[high|medium|low] `file:line`** — what it wastes (CPU, memory, disk, network). *Checked: yes/no.*

## Security
1. **[high|medium|low] `file:line`** — what can be abused and how. *Checked: yes/no.*

## Not checked
- (what could not be run or confirmed, and why)

## Agreements and disagreements (only if there were two auditors)
- **Both found:** (findings seen by both)
- **Only the internal one:** …
- **Only the external one:** …

## Cost
- (tokens and time of each auditor, if known)
