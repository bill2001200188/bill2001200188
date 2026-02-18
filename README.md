# Overseas Social Media Agent (for Chinese Product Sellers)

This repository now includes a lightweight Python agent that helps China-based companies sell products in overseas markets via social media.

## What it does

- Builds a **localized value proposition** from product + audience input.
- Generates post drafts for **LinkedIn, Instagram, and TikTok/Shorts**.
- Creates first-touch **DM outreach scripts**.
- Scores leads with a simple weighted model and recommends sales actions.
- Produces a **7-day content calendar**.

## File

- `oversea_social_media_agent.py`

## Run

```bash
python3 oversea_social_media_agent.py
```

## Typical workflow

1. Add your product details (features, MOQ, pricing, certifications).
2. Define your target overseas audience and platforms.
3. Generate content drafts and outreach scripts.
4. Feed real lead data into scoring.
5. Prioritize hot leads and schedule follow-ups.

## Next improvements

- Integrate real APIs (LinkedIn, Meta, TikTok) for publishing.
- Connect to CRM (HubSpot/Salesforce/Notion database).
- Add multilingual generation (EN/ES/AR/FR).
- Add retrieval over product catalogs and certifications.
