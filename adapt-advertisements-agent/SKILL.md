---
name: adapt-advertisements-agent
description: Adapt one advertising concept into channel-specific and model-ready copy for any AI assistant (ChatGPT, Claude, Gemini, open-source copilots, and custom agents). Use when a user asks to rewrite ads for different audiences, platforms, tones, locales, compliance constraints, or prompt formats.
---

# Adapt Advertisements Agent

## Overview
Use this skill to turn a single campaign idea into multiple ad variants that are ready for different AI systems, ad channels, and audience segments while preserving brand voice and policy compliance.

## Workflow

1. **Capture the brief in structured fields**
   - Product, offer, objective, audience, region/language, channel, tone, CTA, legal constraints.
   - If data is missing, ask only for blockers and proceed with explicit assumptions.

2. **Normalize the source message**
   - Distill one core value proposition.
   - Extract supporting proof points (stats, testimonials, differentiators).
   - List forbidden claims and sensitive topics.

3. **Select adaptation axes**
   - **Audience axis:** beginner vs expert, SMB vs enterprise, B2B vs B2C.
   - **Channel axis:** search ad, social ad, short video script, landing hero copy, email subject/preheader.
   - **Model axis:** target AI style (see `references/model-guidelines.md`).

4. **Generate copy sets**
   - Produce at least 3 headline variants and 2 body variants per target.
   - Keep one variant conservative/compliance-first and one bold/performance-first.
   - Preserve a single CTA per variant.

5. **Run policy and quality checks**
   - Remove unverifiable superlatives and absolute guarantees.
   - Check clarity, reading level, and localization fit.
   - Ensure each variant keeps the same product truth.

6. **Deliver in machine-usable format**
   - Return JSON/CSV-ready blocks for programmatic use.
   - Include a short rationale per variant and a risk flag (`low|medium|high`).

## Output contract

When possible, return this structure:

```json
{
  "campaign": "string",
  "targets": [
    {
      "ai_target": "chatgpt|claude|gemini|generic",
      "channel": "search|social|email|landing|video",
      "audience": "string",
      "variants": [
        {
          "headline": "string",
          "body": "string",
          "cta": "string",
          "tone": "string",
          "risk": "low|medium|high",
          "rationale": "string"
        }
      ]
    }
  ]
}
```

## Resource usage

- Use `scripts/adapt_ads.py` when the user provides a structured JSON brief and requests bulk variant generation scaffolding.
- Read `references/model-guidelines.md` when adapting output format/style for specific AI assistants.

