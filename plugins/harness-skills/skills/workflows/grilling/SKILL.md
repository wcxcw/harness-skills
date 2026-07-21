---
name: grilling
description: Interrogate a plan, decision, or idea until the user and agent reach shared understanding. Use only when the user explicitly invokes `$grilling`, asks to be grilled, or uses another clear grill trigger phrase.
---

# Grilling

Resolve material decisions before taking action or before creating a run.

1. Explore the repository and available environment first. Answer discoverable factual questions yourself.
2. Separate facts from decisions. Facts come from evidence; decisions remain the user's.
3. Walk each material branch of the decision tree in dependency order.
4. Ask one question at a time and wait for the answer before continuing.
5. For every question, provide a recommended answer with a concise reason and tradeoff.
6. Revisit dependent decisions when an answer changes an earlier assumption.
7. When no material branch remains, summarize the shared understanding and ask the user to confirm it.

Do not create or update Harness artifacts, edit code, scaffold files, or take implementation action during grilling. After explicit confirmation, return control to the user; if they want to begin a Harness run, let `writing-specs` record the confirmed shared understanding directly in the task contract.
