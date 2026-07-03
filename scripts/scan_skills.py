from __future__ import annotations

from skillhub_common import refresh_registry


def main() -> None:
    data = refresh_registry()
    project_count = len(data["projects"])
    skill_count = sum(project["skill_count"] for project in data["projects"])
    print(f"Indexed {project_count} projects and {skill_count} skills into registry/projects.yaml")


if __name__ == "__main__":
    main()
