"""Hermes plugin entrypoint for TasteDistill."""

from pathlib import Path


_SKILLS = {
    "learn": "tastedistill-learn",
    "think": "tastedistill-think",
    "design": "tastedistill-design",
    "debug": "tastedistill-debug",
    "ship": "tastedistill-ship",
    "distill": "tastedistill-distill",
}


def register(ctx):
    """Register TasteD skills with Hermes using short names."""
    skills_dir = Path(__file__).parent / "plugins" / "tastedistill" / "skills"
    for public_name, directory_name in _SKILLS.items():
        skill_md = skills_dir / directory_name / "SKILL.md"
        if skill_md.exists():
            ctx.register_skill(public_name, skill_md)
