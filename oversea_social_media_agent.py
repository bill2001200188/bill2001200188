"""Overseas social media sales agent for Chinese companies.

This module provides a practical, extensible baseline agent that:
1) Accepts product and campaign inputs
2) Creates localized post drafts for multiple platforms
3) Produces direct-message outreach scripts
4) Scores leads and recommends next actions

The implementation is intentionally lightweight and dependency-free so it can be
used as a starter in constrained environments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional


@dataclass
class Product:
    """Product information from a Chinese supplier/manufacturer."""

    name: str
    category: str
    key_features: List[str]
    target_price_usd: float
    moq: int
    certifications: List[str] = field(default_factory=list)
    shipping_regions: List[str] = field(default_factory=lambda: ["US", "EU", "SEA", "MENA"])


@dataclass
class AudienceProfile:
    """International audience persona."""

    segment: str
    regions: List[str]
    pain_points: List[str]
    preferred_platforms: List[str]
    tone: str = "professional"


@dataclass
class Lead:
    """Potential B2B/B2C buyer discovered from social channels."""

    handle: str
    platform: str
    region: str
    intent_signal: int  # 1..5 (5 = strong buying intent)
    budget_fit: int  # 1..5
    response_speed: int  # 1..5
    trust_signal: int  # 1..5


class OverseasSocialMediaAgent:
    """A simple agent orchestrating social selling workflows."""

    def __init__(self, company_name: str, default_language: str = "en") -> None:
        self.company_name = company_name
        self.default_language = default_language

    def build_value_proposition(self, product: Product, audience: AudienceProfile) -> str:
        """Construct a concise value proposition with regional relevance."""
        features = ", ".join(product.key_features[:3])
        pains = ", ".join(audience.pain_points[:2])
        certs = f" Certified: {', '.join(product.certifications)}." if product.certifications else ""
        return (
            f"{product.name} helps {audience.segment} solve {pains}. "
            f"Top advantages: {features}. "
            f"Factory-direct target price from ${product.target_price_usd:.2f}, MOQ {product.moq}.{certs}"
        )

    def generate_platform_post(
        self,
        platform: str,
        product: Product,
        audience: AudienceProfile,
        cta: str = "DM us for catalog and sample pricing",
    ) -> str:
        """Generate a platform-tailored post draft."""
        vp = self.build_value_proposition(product, audience)

        if platform.lower() == "linkedin":
            return (
                f"{vp}\n\n"
                f"We support private label and fast export onboarding in {', '.join(audience.regions)}.\n"
                f"{cta}. #B2B #Sourcing #MadeInChina"
            )
        if platform.lower() == "instagram":
            return (
                f"Factory-direct {product.name} for {audience.segment}!\n"
                f"{vp}\n"
                f"{cta}. ✨\n"
                f"#{product.category.replace(' ', '')} #Wholesale #GlobalTrade"
            )
        if platform.lower() in {"tiktok", "youtube shorts"}:
            return (
                f"POV: You need reliable {product.category} supply for your market.\n"
                f"{product.name} | MOQ {product.moq} | from ${product.target_price_usd:.2f}\n"
                f"Comment 'CATALOG' and we'll send details."
            )

        return f"{vp}\n{cta}."

    def create_dm_script(self, lead: Lead, product: Product) -> str:
        """Create a first-touch direct message script."""
        return (
            f"Hi {lead.handle}, I noticed your interest in {product.category}. "
            f"I work with {self.company_name}, a China-based supplier of {product.name}. "
            f"We can support {lead.region} with stable lead time and competitive pricing. "
            f"Would you like our latest catalog + sample quote?"
        )

    def score_lead(self, lead: Lead) -> int:
        """Simple weighted lead score (0-100)."""
        weighted = (
            lead.intent_signal * 0.35
            + lead.budget_fit * 0.25
            + lead.response_speed * 0.2
            + lead.trust_signal * 0.2
        )
        return int((weighted / 5) * 100)

    def recommend_action(self, score: int) -> str:
        """Map score to next sales action."""
        if score >= 80:
            return "Hot lead: schedule call within 24h and send quote immediately."
        if score >= 60:
            return "Warm lead: send case study + pricing tiers and follow up in 48h."
        if score >= 40:
            return "Nurture: add to weekly content workflow and re-engage in 7 days."
        return "Low priority: keep in CRM and retarget with awareness content."

    def weekly_content_calendar(
        self, product: Product, audience: AudienceProfile, start: Optional[datetime] = None
    ) -> List[Dict[str, str]]:
        """Create a simple 7-day social posting plan."""
        start = start or datetime.utcnow()
        themes = [
            "problem/solution",
            "factory credibility",
            "customer testimonial",
            "feature spotlight",
            "FAQ",
            "pricing transparency",
            "call-to-action",
        ]
        platforms = audience.preferred_platforms or ["LinkedIn", "Instagram"]

        calendar = []
        for i, theme in enumerate(themes):
            day = (start + timedelta(days=i)).strftime("%Y-%m-%d")
            platform = platforms[i % len(platforms)]
            post = self.generate_platform_post(platform, product, audience)
            calendar.append({"date": day, "platform": platform, "theme": theme, "draft": post})
        return calendar


if __name__ == "__main__":
    product = Product(
        name="Solar Power Bank 20000mAh",
        category="consumer electronics",
        key_features=["PD fast charging", "water-resistant casing", "OEM branding"],
        target_price_usd=8.9,
        moq=300,
        certifications=["CE", "RoHS", "FCC"],
    )
    audience = AudienceProfile(
        segment="distributors and e-commerce sellers",
        regions=["US", "Germany", "UAE"],
        pain_points=["high landed cost", "inconsistent quality", "slow replenishment"],
        preferred_platforms=["LinkedIn", "Instagram", "TikTok"],
    )
    lead = Lead(
        handle="@globalgadgets",
        platform="Instagram",
        region="US",
        intent_signal=4,
        budget_fit=5,
        response_speed=3,
        trust_signal=4,
    )

    agent = OverseasSocialMediaAgent(company_name="Shenzhen NovaTech")
    print("=== Value Proposition ===")
    print(agent.build_value_proposition(product, audience))
    print("\n=== LinkedIn Draft ===")
    print(agent.generate_platform_post("LinkedIn", product, audience))
    print("\n=== DM Script ===")
    print(agent.create_dm_script(lead, product))
    lead_score = agent.score_lead(lead)
    print("\n=== Lead Score & Action ===")
    print(lead_score, agent.recommend_action(lead_score))
