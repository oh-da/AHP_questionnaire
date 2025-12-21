"""
Application Entry Point
Dependency Injection: Wire up all dependencies
"""

import os
from .ahp_calculator import AHPCalculator
from .persistence import GitHubGistPersistence, InMemoryPersistence
from .criteria_loader import CSVCriteriaLoader
from .services import AHPQuestionnaireService
from .api import AHPQuestionnaireAPI


def create_app():
    """
    Application factory.
    Dependency Injection: Create and wire all dependencies.
    """
    # Create dependencies
    calculator = AHPCalculator()
    criteria_loader = CSVCriteriaLoader(csv_file="criteria.csv")

    # Choose persistence based on configuration
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        persistence = GitHubGistPersistence(
            github_token=github_token,
            gist_id=os.getenv("GIST_ID"),
            filename=os.getenv("GIST_FILENAME", "ahp_results.csv")
        )
        print("✓ GitHub Gist persistence configured")
    else:
        persistence = InMemoryPersistence()
        print("⚠ Using in-memory persistence (GITHUB_TOKEN not set)")

    # Create service with dependencies
    service = AHPQuestionnaireService(
        calculator=calculator,
        persistence=persistence,
        criteria_loader=criteria_loader
    )

    # Create API with service
    api = AHPQuestionnaireAPI(service)

    return api


def main():
    """Main entry point."""
    port = int(os.getenv("PORT", "5000"))

    print("=" * 50)
    print("AHP Questionnaire API Server")
    print("=" * 50)

    api = create_app()

    print(f"\n✓ Server starting on port {port}")
    print(f"✓ Health check: http://localhost:{port}/api/health")
    print("\nPress CTRL+C to stop\n")

    api.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
