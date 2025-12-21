"""
Flask API Application
Single Responsibility: HTTP routing and request/response handling
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from .services import AHPQuestionnaireService


class AHPQuestionnaireAPI:
    """
    Flask API wrapper.
    Interface Segregation: Focused on HTTP concerns only.
    """

    def __init__(self, service: AHPQuestionnaireService):
        """Initialize API with service dependency."""
        self.service = service
        self.app = Flask(__name__)

        # Configure CORS with comprehensive settings
        CORS(self.app,
             resources={r"/api/*": {"origins": "*"}},
             allow_headers=["Content-Type", "Authorization"],
             methods=["GET", "POST", "OPTIONS"],
             supports_credentials=False,
             max_age=3600)

        # Add after_request handler for explicit CORS headers
        @self.app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
            return response

        self._register_routes()

    def _register_routes(self):
        """Register all API routes."""

        @self.app.route("/api/health", methods=["GET"])
        def health():
            """Health check endpoint."""
            return jsonify(self.service.get_health_status())

        @self.app.route("/api/criteria", methods=["GET"])
        def get_criteria():
            """Get questionnaire criteria."""
            criteria = self.service.get_criteria()
            return jsonify({"criteria": criteria})

        @self.app.route("/api/results", methods=["GET"])
        def list_results():
            """List all saved results."""
            results = self.service.get_all_responses()
            return jsonify(results)

        @self.app.route("/api/calculate", methods=["POST", "OPTIONS"])
        def calculate_and_save():
            """Calculate AHP weights and save to storage."""
            # Handle CORS preflight request explicitly
            if request.method == "OPTIONS":
                response = jsonify({"status": "ok"})
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.headers.add("Access-Control-Allow-Headers", "Content-Type")
                response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
                return response, 200

            try:
                # Parse request
                payload = request.get_json(silent=True) or {}
                user_name = payload.get("userName", "")
                criteria = payload.get("criteria")
                comparisons = payload.get("comparisons", [])

                # Validate
                if not isinstance(criteria, list) or not criteria:
                    return jsonify({
                        "error": "criteria must be a non-empty list"
                    }), 400

                if not isinstance(comparisons, list) or not comparisons:
                    return jsonify({
                        "error": "comparisons must be a non-empty list"
                    }), 400

                # Process questionnaire
                results = self.service.process_questionnaire(
                    user_name=user_name,
                    criteria=criteria,
                    comparisons=comparisons
                )

                # Return results
                status_code = 200 if results.get('savedToGist', False) else 200
                return jsonify(results), status_code

            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                return jsonify({"error": f"Internal error: {str(e)}"}), 500

        @self.app.errorhandler(404)
        def not_found(e):
            """404 handler."""
            return jsonify({"error": "Endpoint not found"}), 404

        @self.app.errorhandler(500)
        def internal_error(e):
            """500 handler."""
            return jsonify({"error": "Internal server error"}), 500

    def run(self, host: str = "0.0.0.0", port: int = 5000):
        """Run the Flask application."""
        self.app.run(host=host, port=port)

    def get_app(self):
        """Get Flask app instance (for WSGI servers)."""
        return self.app
