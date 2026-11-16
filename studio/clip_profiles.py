"""Selection profiles that steer which moments SCut Studio asks the AI to find."""

CLIP_PROFILES = {
    "balanced": {
        "label": "Balanced",
        "prompt": "Prioritize the strongest broadly entertaining standalone moments. Consider humor, surprise, skill, strong reactions, and stories with a payoff.",
    },
    "funny": {
        "label": "Funny",
        "prompt": "Prioritize genuinely funny moments: jokes with a payoff, unexpected mishaps, playful banter, absurd turns, and authentic laughter. Include enough setup to make the joke land; skip moments that are merely loud.",
    },
    "horror": {
        "label": "Horror / suspense",
        "prompt": "Prioritize horror or suspense moments: mounting tension, creepy reveals, jump scares, near misses, and genuine fear or surprise. Include the lead-in and reaction when needed for the moment to make sense. The transcript may not describe everything visible, so use only evidence in the transcript and reaction markers; do not invent visual events.",
    },
    "controversial": {
        "label": "Controversial",
        "prompt": "Prioritize clearly expressed strong opinions, disagreements, heated debates, and surprising takes that could prompt discussion. Include enough context to represent what was said fairly; do not exaggerate a disagreement or present an opinion as established fact.",
    },
    "scandal": {
        "label": "Scandal / revelations",
        "prompt": "Prioritize explicit revelations, admissions, accusations, or dramatic disclosures discussed in the transcript. Keep the surrounding context that identifies what is being claimed. Treat claims as claims, not verified facts; do not infer wrongdoing, invent details, or turn speculation into an assertion.",
    },
}


def prompt_for(profile):
    return CLIP_PROFILES.get(profile, CLIP_PROFILES["balanced"])["prompt"]
