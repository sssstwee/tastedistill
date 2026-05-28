"""Hermes plugin entrypoint for TasteDistill."""

from pathlib import Path


_SKILLS = {
    "tasted-learn": "tasted-learn",
    "tasted-think": "tasted-think",
    "tasted-design": "tasted-design",
    "tasted-debug": "tasted-debug",
    "tasted-ship": "tasted-ship",
    "tasted-distill": "tasted-distill",
}


def register(ctx):
    """Register TasteD skills with Hermes using its short public names."""
    skills_dir = Path(__file__).parent / "plugins" / "tastedistill" / "hermes-skills"
    for public_name, directory_name in _SKILLS.items():
        skill_md = skills_dir / directory_name / "SKILL.md"
        if skill_md.exists():
            ctx.register_skill(public_name, skill_md)
