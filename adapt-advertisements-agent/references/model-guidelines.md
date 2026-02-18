# Model adaptation guidelines

Use this file only when the user asks for AI-specific formatting.

## ChatGPT-style targets
- Prefer concise section headers and bullet outputs.
- Include explicit constraints in the prompt (word count, banned claims, tone).
- Ask for JSON when downstream automation is needed.

## Claude-style targets
- Prefer clear, policy-aware reasoning and nuance.
- Add "what to avoid" instructions and truthfulness constraints.
- Use structured blocks with labels for safer editing.

## Gemini-style targets
- Prefer multimodal-ready framing (text that can pair with image/video prompts).
- Include context and intent together in each prompt block.
- Keep formatting straightforward with short paragraphs.

## Generic/open-source model targets
- Be explicit and deterministic.
- Use strict schemas, delimiters, and examples.
- Avoid vague goals like "make it catchy" without measurable constraints.

## Cross-model safeguards
1. Never invent pricing, approvals, or certifications.
2. Avoid absolute claims ("best", "guaranteed") unless verified.
3. Keep regional/legal disclaimers in every localized variant.
4. Separate factual claims from creative embellishment.
