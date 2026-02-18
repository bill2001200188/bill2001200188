#!/usr/bin/env python3
"""Generate adaptation scaffolding for ad copy across AI targets/channels.

Input: JSON file with keys:
  campaign, offer, audiences[], channels[], ai_targets[], tone, cta
Output: JSON printed to stdout following the skill output contract.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


RISK_BY_TONE = {
    "conservative": "low",
    "professional": "low",
    "balanced": "medium",
    "bold": "medium",
    "aggressive": "high",
}


def make_variant(campaign: str, offer: str, audience: str, channel: str, tone: str, cta: str) -> dict:
    headline = f"{campaign} for {audience}"
    body = f"{offer} tailored for {channel} with a {tone} tone."
    return {
        "headline": headline,
        "body": body,
        "cta": cta,
        "tone": tone,
        "risk": RISK_BY_TONE.get(tone.lower(), "medium"),
        "rationale": "Baseline variant generated from structured brief.",
    }


def build(data: dict) -> dict:
    campaign = data.get("campaign", "Campaign")
    offer = data.get("offer", "Offer details")
    audiences = data.get("audiences", ["general audience"])
    channels = data.get("channels", ["social"])
    ai_targets = data.get("ai_targets", ["generic"])
    tone = data.get("tone", "balanced")
    cta = data.get("cta", "Learn more")

    targets = []
    for ai_target in ai_targets:
        for channel in channels:
            for audience in audiences:
                variants = [
                    make_variant(campaign, offer, audience, channel, tone, cta),
                    make_variant(campaign, offer, audience, channel, "conservative", cta),
                    make_variant(campaign, offer, audience, channel, "bold", cta),
                ]
                targets.append(
                    {
                        "ai_target": ai_target,
                        "channel": channel,
                        "audience": audience,
                        "variants": variants,
                    }
                )

    return {"campaign": campaign, "targets": targets}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: adapt_ads.py <brief.json>", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    data = json.loads(input_path.read_text(encoding="utf-8"))
    output = build(data)
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
