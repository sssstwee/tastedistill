"""Hermes plugin entrypoint for TasteDistill."""

from pathlib import Path


_SKILLS = {
    "learn": "tasted-learn",
    "think": "tasted-think",
    "design": "tasted-design",
    "debug": "tasted-debug",
    "ship": "tasted-ship",
    "distill": "tasted-distill",
}


def register(ctx):
    """Register TasteD skills with Hermes using plugin-qualified short names."""
    skills_dir = Path(__file__).parent / "plugins" / "tastedistill" / "hermes-skills"
    for public_name, directory_name in _SKILLS.items():
        skill_md = skills_dir / directory_name / "SKILL.md"
        if skill_md.exists():
            ctx.register_skill(public_name, skill_md)
            ctx.register_skill(directory_name, skill_md)
