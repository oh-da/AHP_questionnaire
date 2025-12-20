"""
AHP Questionnaire Streamlit App
SOLID Design Principles Implementation
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import gspread
from google.oauth2.service_account import Credentials


# ============================================================================
# DOMAIN MODELS (Single Responsibility - Data structures)
# ============================================================================

@dataclass
class Criterion:
    """Represents a single criterion in the AHP questionnaire."""
    name: str
    index: int


@dataclass
class PairwiseComparison:
    """Represents a pairwise comparison between two criteria."""
    criterion_a: Criterion
    criterion_b: Criterion
    question_number: int

    def get_question_text(self) -> str:
        return f"{self.criterion_a.name} vs {self.criterion_b.name}"


@dataclass
class AHPResults:
    """Contains computed AHP weights and consistency metrics."""
    weights: Dict[str, float]
    lambda_max: float
    ci: float
    cr: float

    def is_consistent(self, threshold: float = 0.1) -> bool:
        return self.cr <= threshold


# ============================================================================
# ABSTRACTIONS (Dependency Inversion - Define interfaces)
# ============================================================================

class IQuestionnaireDataSource(ABC):
    """Interface for loading questionnaire structure."""

    @abstractmethod
    def get_criteria(self) -> List[Criterion]:
        """Return list of criteria."""
        pass


class IAHPCalculator(ABC):
    """Interface for AHP calculations."""

    @abstractmethod
    def compute_weights(
        self,
        criteria: List[Criterion],
        comparisons: Dict[Tuple[int, int], float]
    ) -> AHPResults:
        """Compute AHP weights and consistency from pairwise comparisons."""
        pass


class IExportService(ABC):
    """Interface for exporting results."""

    @abstractmethod
    def export_to_csv(self, answers: Dict, results: AHPResults) -> bytes:
        """Export answers and results to CSV format."""
        pass

    @abstractmethod
    def export_to_json(self, answers: Dict, results: AHPResults) -> bytes:
        """Export answers and results to JSON format."""
        pass


# ============================================================================
# AHP CALCULATION ENGINE (Single Responsibility - Pure computation)
# ============================================================================

class AHPCalculator(IAHPCalculator):
    """
    Implements AHP weight calculation and consistency checking.
    Open-Closed: Can be extended without modification.
    """

    def __init__(self, ri_values: Optional[Dict[int, float]] = None):
        """Initialize with Random Index values for different matrix sizes."""
        self.ri_values = ri_values or {
            1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
            5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
            9: 1.45, 10: 1.49
        }

    def convert_scale_to_ratio(self, scale_value: int) -> float:
        """
        Convert -8..8 scale to AHP ratio.
        0: equal importance (1.0)
        Positive: B more important than A (slider moved RIGHT)
        Negative: A more important than B (slider moved LEFT)
        """
        if scale_value > 0:
            return 1.0 / (scale_value + 1)  # B more important (right side)
        elif scale_value == 0:
            return 1.0
        else:
            return abs(scale_value) + 1  # A more important (left side)

    def build_pairwise_matrix(
        self,
        n_criteria: int,
        comparisons: Dict[Tuple[int, int], float]
    ) -> np.ndarray:
        """Build the full pairwise comparison matrix from upper triangle."""
        matrix = np.ones((n_criteria, n_criteria))

        # Fill upper triangle
        for (i, j), value in comparisons.items():
            if i < j:
                matrix[i, j] = value
                matrix[j, i] = 1.0 / value  # Reciprocal for lower triangle

        return matrix

    def compute_weights(
        self,
        criteria: List[Criterion],
        comparisons: Dict[Tuple[int, int], float]
    ) -> AHPResults:
        """Compute AHP weights using geometric mean method."""
        n = len(criteria)

        # Convert scale values to ratios
        ratio_comparisons = {
            (i, j): self.convert_scale_to_ratio(scale)
            for (i, j), scale in comparisons.items()
        }

        # Build pairwise matrix
        matrix = self.build_pairwise_matrix(n, ratio_comparisons)

        # Calculate weights using geometric mean
        geometric_means = np.power(np.prod(matrix, axis=1), 1.0 / n)
        weights = geometric_means / geometric_means.sum()

        # Calculate lambda_max for consistency
        weighted_sum = matrix @ weights
        lambda_max = np.mean(weighted_sum / weights)

        # Consistency Index (CI)
        ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0

        # Consistency Ratio (CR)
        ri = self.ri_values.get(n, 1.12)
        cr = ci / ri if ri > 0 else 0.0

        # Build weights dictionary
        weights_dict = {
            criterion.name: float(weights[criterion.index])
            for criterion in criteria
        }

        return AHPResults(
            weights=weights_dict,
            lambda_max=float(lambda_max),
            ci=float(ci),
            cr=float(cr)
        )


# ============================================================================
# DATA SOURCES (Single Responsibility - Data loading)
# ============================================================================

class DefaultQuestionnaireDataSource(IQuestionnaireDataSource):
    """Provides default questionnaire structure (Liskov Substitution)."""

    def get_criteria(self) -> List[Criterion]:
        """Return the 5 standard criteria."""
        criteria_names = [
            'Passenger Activity',
            'Service & Modes',
            'Location',
            'Population & Jobs',
            'Bus Terminal'
        ]
        return [
            Criterion(name=name, index=i)
            for i, name in enumerate(criteria_names)
        ]


class CSVQuestionnaireDataSource(IQuestionnaireDataSource):
    """Loads questionnaire structure from CSV file."""

    def __init__(self, csv_file):
        self.csv_file = csv_file

    def get_criteria(self) -> List[Criterion]:
        """Parse criteria from CSV file."""
        try:
            df = pd.read_csv(self.csv_file)

            # Expected CSV format: single column named 'Criterion' or 'Criteria'
            if 'Criterion' in df.columns:
                criteria_names = df['Criterion'].dropna().tolist()
            elif 'Criteria' in df.columns:
                criteria_names = df['Criteria'].dropna().tolist()
            elif len(df.columns) == 1:
                # If there's only one column, use it
                criteria_names = df.iloc[:, 0].dropna().tolist()
            else:
                st.error("CSV must have a column named 'Criterion' or 'Criteria'")
                return self._get_default_criteria()

            if not criteria_names or len(criteria_names) < 2:
                st.error("CSV must contain at least 2 criteria")
                return self._get_default_criteria()

            return [
                Criterion(name=str(name).strip(), index=i)
                for i, name in enumerate(criteria_names)
            ]
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")
            return self._get_default_criteria()

    def _get_default_criteria(self) -> List[Criterion]:
        """Return default criteria as fallback."""
        return DefaultQuestionnaireDataSource().get_criteria()


# ============================================================================
# QUESTIONNAIRE LOGIC (Single Responsibility - Business logic)
# ============================================================================

class QuestionnaireManager:
    """Manages questionnaire state and comparison generation."""

    def __init__(self, criteria: List[Criterion]):
        self.criteria = criteria
        self.comparisons = self._generate_comparisons()

    def _generate_comparisons(self) -> List[PairwiseComparison]:
        """Generate all pairwise comparisons (upper triangle)."""
        comparisons = []
        question_num = 1

        n = len(self.criteria)
        for i in range(n):
            for j in range(i + 1, n):
                comparisons.append(
                    PairwiseComparison(
                        criterion_a=self.criteria[i],
                        criterion_b=self.criteria[j],
                        question_number=question_num
                    )
                )
                question_num += 1

        return comparisons

    def get_total_questions(self) -> int:
        """Return total number of comparisons."""
        return len(self.comparisons)

    def get_comparison(self, index: int) -> Optional[PairwiseComparison]:
        """Get comparison by index."""
        if 0 <= index < len(self.comparisons):
            return self.comparisons[index]
        return None


# ============================================================================
# EXPORT SERVICE (Single Responsibility - Export logic)
# ============================================================================

class ExportService(IExportService):
    """Handles exporting results to various formats."""

    def export_to_csv(self, answers: Dict, results: AHPResults) -> bytes:
        """Export answers and results to CSV."""
        rows = []

        # Add answers
        rows.append(['ANSWERS', '', ''])
        rows.append(['Question', 'Comparison', 'Response'])
        for key, value in answers.items():
            rows.append([key, '', value])

        rows.append(['', '', ''])
        rows.append(['RESULTS', '', ''])
        rows.append(['Criterion', 'Weight', 'Percentage'])

        for criterion, weight in results.weights.items():
            rows.append([criterion, f"{weight:.4f}", f"{weight*100:.2f}%"])

        rows.append(['', '', ''])
        rows.append(['CONSISTENCY METRICS', '', ''])
        rows.append(['Lambda Max', f"{results.lambda_max:.4f}", ''])
        rows.append(['Consistency Index (CI)', f"{results.ci:.4f}", ''])
        rows.append(['Consistency Ratio (CR)', f"{results.cr:.4f}", ''])
        rows.append(['Status', 'Consistent' if results.is_consistent() else 'Review Needed', ''])

        df = pd.DataFrame(rows)
        return df.to_csv(index=False, header=False).encode('utf-8')

    def export_to_json(self, answers: Dict, results: AHPResults) -> bytes:
        """Export answers and results to JSON."""
        data = {
            'answers': answers,
            'results': {
                'weights': results.weights,
                'lambda_max': results.lambda_max,
                'consistency_index': results.ci,
                'consistency_ratio': results.cr,
                'is_consistent': results.is_consistent()
            }
        }
        return json.dumps(data, indent=2).encode('utf-8')


# ============================================================================
# PERSISTENCE SERVICE (Single Responsibility - Data persistence)
# ============================================================================

class PersistenceService:
    """Handles saving questionnaire results to persistent storage."""

    def __init__(self, results_file: str = "results.csv"):
        self.results_file = results_file

    def save_results(
        self,
        criteria: List[Criterion],
        answers: Dict,
        results: AHPResults
    ) -> bool:
        """Save questionnaire results to CSV file (append mode)."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Build row data
            row_data = {
                'timestamp': timestamp,
                'consistency_ratio': results.cr,
                'consistency_index': results.ci,
                'lambda_max': results.lambda_max,
                'is_consistent': results.is_consistent()
            }

            # Add weights for each criterion
            for criterion in criteria:
                row_data[f'weight_{criterion.name}'] = results.weights.get(criterion.name, 0)

            # Add answers for each comparison
            for key, value in answers.items():
                row_data[f'answer_{key}'] = value

            # Convert to DataFrame
            df = pd.DataFrame([row_data])

            # Append to file or create new file
            if os.path.exists(self.results_file):
                df.to_csv(self.results_file, mode='a', header=False, index=False)
            else:
                df.to_csv(self.results_file, mode='w', header=True, index=False)

            return True
        except Exception as e:
            # Silently fail - will be handled by caller
            print(f"Error saving results: {e}")  # Log to console
            return False


class GoogleSheetsPersistenceService:
    """Handles saving questionnaire results to Google Sheets (permanent storage)."""

    def __init__(self, sheet_name: str = "AHP Results"):
        self.sheet_name = sheet_name
        self.client = None
        self.sheet = None
        self.error_message = None  # Store error for debugging
        self._initialize_sheets()

    def _initialize_sheets(self):
        """Initialize Google Sheets connection using Streamlit secrets."""
        try:
            # Check if Google Sheets credentials are configured
            if "gcp_service_account" not in st.secrets:
                self.error_message = "Secret 'gcp_service_account' not found"
                print("Google Sheets credentials not found in secrets")
                return

            # Set up credentials with modern google-auth
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            credentials = Credentials.from_service_account_info(
                st.secrets["gcp_service_account"],
                scopes=scopes
            )

            self.client = gspread.authorize(credentials)

            # Open or create spreadsheet
            try:
                self.sheet = self.client.open(self.sheet_name).sheet1
            except gspread.SpreadsheetNotFound:
                # Create new spreadsheet
                spreadsheet = self.client.create(self.sheet_name)
                self.sheet = spreadsheet.sheet1
                # Share with your email (from secrets)
                if "admin_email" in st.secrets:
                    spreadsheet.share(st.secrets["admin_email"], perm_type='user', role='writer')

        except Exception as e:
            self.error_message = str(e)
            print(f"Error initializing Google Sheets: {e}")
            self.client = None
            self.sheet = None

    def save_results(
        self,
        criteria: List[Criterion],
        answers: Dict,
        results: AHPResults
    ) -> bool:
        """Save questionnaire results to Google Sheets."""
        if not self.sheet:
            return False

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Build row data
            row_data = {
                'timestamp': timestamp,
                'consistency_ratio': results.cr,
                'consistency_index': results.ci,
                'lambda_max': results.lambda_max,
                'is_consistent': results.is_consistent()
            }

            # Add weights for each criterion
            for criterion in criteria:
                row_data[f'weight_{criterion.name}'] = results.weights.get(criterion.name, 0)

            # Add answers for each comparison
            for key, value in answers.items():
                row_data[f'answer_{key}'] = value

            # Get or create headers
            existing_headers = self.sheet.row_values(1)
            headers = list(row_data.keys())

            if not existing_headers:
                # First row - add headers
                self.sheet.append_row(headers)
            elif existing_headers != headers:
                # Headers changed (different criteria) - update
                self.sheet.update('1:1', [headers])

            # Append data row
            values = [row_data[h] for h in headers]
            self.sheet.append_row(values)

            return True

        except Exception as e:
            print(f"Error saving to Google Sheets: {e}")
            return False

    def is_configured(self) -> bool:
        """Check if Google Sheets is properly configured."""
        return self.sheet is not None

    def get_spreadsheet_url(self) -> Optional[str]:
        """Get the URL of the Google Sheets spreadsheet."""
        if not self.sheet:
            return None
        try:
            spreadsheet = self.client.open(self.sheet_name)
            return spreadsheet.url
        except:
            return None


# ============================================================================
# UI COMPONENTS (Single Responsibility - UI rendering)
# ============================================================================

class UIRenderer:
    """Handles all UI rendering logic (Interface Segregation)."""

    @staticmethod
    def render_header():
        """Render app header."""
        st.set_page_config(
            page_title="AHP Questionnaire",
            page_icon="📊",
            layout="wide"
        )

        st.markdown("""
            <style>
            /* Main content area - light background with dark text */
            .main {
                background-color: #f8f9fa;
            }
            .main h1, .main h2, .main h3, .main h4, .main h5, .main h6,
            .main p, .main div, .main span, .main label {
                color: #262730 !important;
            }
            .main .stMarkdown {
                color: #262730;
            }

            /* Sidebar - keep default dark background with light text */
            [data-testid="stSidebar"] {
                background-color: #262730;
            }
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] div {
                color: #fafafa !important;
            }

            /* Buttons */
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 0.5rem 2rem;
            }

            /* Progress bar */
            .stProgress > div > div { background-color: #4CAF50; }
            </style>
        """, unsafe_allow_html=True)

        st.title("📊 Hub Prioritization Questionnaire")
        st.markdown("""
            Welcome! This questionnaire helps prioritize transportation hubs using
            the Analytic Hierarchy Process (AHP). You'll compare different criteria
            to determine their relative importance.
        """)

    @staticmethod
    def render_scale_guide():
        """Render the comparison scale guide."""
        with st.expander("ℹ️ How to answer", expanded=False):
            st.markdown("""
                **Understanding the Scale (-8 to +8):**

                - **0**: Both criteria are equally important
                - **Slide LEFT (negative -1 to -8)**: Left criterion is more important (further left = much more important)
                - **Slide RIGHT (positive +1 to +8)**: Right criterion is more important (further right = much more important)

                **Example:** If comparing "Passenger Activity" (LEFT) vs "Location" (RIGHT):
                - Move slider LEFT to **-5** if Passenger Activity is strongly more important
                - Keep at **0** if they're equally important
                - Move slider RIGHT to **+3** if Location is moderately more important
            """)

    @staticmethod
    def render_progress(current: int, total: int):
        """Render progress indicator."""
        progress = (current) / total
        st.progress(progress)
        st.caption(f"Question {current} of {total}")

    @staticmethod
    def render_comparison_question(
        comparison: PairwiseComparison,
        key: str,
        default_value: int = 0
    ) -> int:
        """Render a single comparison question."""
        st.markdown(f"### Question {comparison.question_number}")
        st.markdown(f"#### Which is more important?")

        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            st.info(f"**{comparison.criterion_a.name}**")

        with col2:
            st.markdown("<div style='text-align: center; padding-top: 10px; color: #262730;'><strong>vs</strong></div>",
                       unsafe_allow_html=True)

        with col3:
            st.success(f"**{comparison.criterion_b.name}**")

        value = st.slider(
            f"Select importance (-8 to +8)",
            min_value=-8,
            max_value=8,
            value=default_value,
            key=key,
            help=f"Move LEFT (negative): {comparison.criterion_a.name} is more important | "
                 f"Center (0): Equal importance | "
                 f"Move RIGHT (positive): {comparison.criterion_b.name} is more important"
        )

        # Show interpretation
        if value > 0:
            st.caption(f"✓ {comparison.criterion_b.name} is more important (strength: {value})")
        elif value < 0:
            st.caption(f"✓ {comparison.criterion_a.name} is more important (strength: {abs(value)})")
        else:
            st.caption(f"✓ Both are equally important")

        return value

    @staticmethod
    def render_results(results: AHPResults, criteria_names: List[str]):
        """Render results page."""
        st.success("✅ Questionnaire Complete!")

        # Consistency status
        st.markdown("### Consistency Check")
        if results.is_consistent():
            st.success(f"✓ Your answers are consistent! (CR = {results.cr:.3f} ≤ 0.10)")
        else:
            st.warning(f"⚠️ Your answers may need review (CR = {results.cr:.3f} > 0.10)")

        st.caption(f"Consistency Ratio (CR): {results.cr:.4f} | "
                  f"Consistency Index (CI): {results.ci:.4f} | "
                  f"Lambda Max: {results.lambda_max:.4f}")

        # Weights visualization
        st.markdown("### Priority Weights")

        col1, col2 = st.columns([3, 2])

        with col1:
            # Bar chart
            weights_df = pd.DataFrame({
                'Criterion': list(results.weights.keys()),
                'Weight': list(results.weights.values())
            })
            weights_df = weights_df.sort_values('Weight', ascending=True)

            st.bar_chart(weights_df.set_index('Criterion'))

        with col2:
            # Table
            display_df = pd.DataFrame({
                'Criterion': list(results.weights.keys()),
                'Weight': [f"{w:.4f}" for w in results.weights.values()],
                'Percentage': [f"{w*100:.2f}%" for w in results.weights.values()]
            })
            display_df = display_df.sort_values('Weight', ascending=False)
            st.dataframe(display_df, hide_index=True, width='stretch')


# ============================================================================
# APPLICATION CONTROLLER (Dependency Inversion - Depends on abstractions)
# ============================================================================

class AHPQuestionnaireApp:
    """
    Main application controller.
    Orchestrates the flow using dependency injection.
    """

    def __init__(
        self,
        data_source: IQuestionnaireDataSource,
        calculator: IAHPCalculator,
        export_service: IExportService,
        persistence_service: PersistenceService
    ):
        self.data_source = data_source
        self.calculator = calculator
        self.export_service = export_service
        self.persistence_service = persistence_service
        self.ui = UIRenderer()

    def initialize_session_state(self):
        """Initialize session state variables."""
        if 'current_question' not in st.session_state:
            st.session_state.current_question = 0

        if 'answers' not in st.session_state:
            st.session_state.answers = {}

        if 'completed' not in st.session_state:
            st.session_state.completed = False

        if 'criteria' not in st.session_state:
            st.session_state.criteria = self.data_source.get_criteria()

        if 'questionnaire_manager' not in st.session_state:
            st.session_state.questionnaire_manager = QuestionnaireManager(
                st.session_state.criteria
            )

    def run_questionnaire_flow(self):
        """Run the main questionnaire flow."""
        manager: QuestionnaireManager = st.session_state.questionnaire_manager
        total_questions = manager.get_total_questions()
        current_idx = st.session_state.current_question

        if current_idx < total_questions:
            # Show progress
            self.ui.render_progress(current_idx + 1, total_questions)

            # Get current comparison
            comparison = manager.get_comparison(current_idx)

            # Get previous answer if exists
            answer_key = f"q_{comparison.question_number}"
            default_value = st.session_state.answers.get(answer_key, 0)

            # Render question
            answer = self.ui.render_comparison_question(
                comparison,
                key=answer_key,
                default_value=default_value
            )

            # Save answer
            st.session_state.answers[answer_key] = answer

            # Navigation
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                if current_idx > 0:
                    if st.button("← Previous"):
                        st.session_state.current_question -= 1
                        st.rerun()

            with col3:
                if current_idx < total_questions - 1:
                    if st.button("Next →"):
                        st.session_state.current_question += 1
                        st.rerun()
                else:
                    if st.button("Finish 🎯"):
                        st.session_state.completed = True
                        st.rerun()

    def run_results_flow(self):
        """Run the results display flow."""
        manager: QuestionnaireManager = st.session_state.questionnaire_manager

        # Build comparisons dictionary for calculator
        comparisons_dict = {}
        for comparison in manager.comparisons:
            answer_key = f"q_{comparison.question_number}"
            scale_value = st.session_state.answers.get(answer_key, 0)

            i = comparison.criterion_a.index
            j = comparison.criterion_b.index
            comparisons_dict[(i, j)] = scale_value

        # Calculate results
        results = self.calculator.compute_weights(
            st.session_state.criteria,
            comparisons_dict
        )

        # Save results to persistent storage (once per completion)
        if 'results_saved' not in st.session_state:
            save_success = self.persistence_service.save_results(
                st.session_state.criteria,
                st.session_state.answers,
                results
            )
            st.session_state.results_saved = True
            if save_success:
                if isinstance(self.persistence_service, GoogleSheetsPersistenceService):
                    st.success("✅ Results saved to Google Sheets permanently!")
                else:
                    st.success("✅ Results saved to results.csv")
            else:
                st.warning("⚠️ Could not save results. Use download button below.")

        # Render results
        criteria_names = [c.name for c in st.session_state.criteria]
        self.ui.render_results(results, criteria_names)

        # Export options
        st.markdown("### Export Results")
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            csv_data = self.export_service.export_to_csv(
                st.session_state.answers,
                results
            )
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name="ahp_results.csv",
                mime="text/csv"
            )

        with col2:
            json_data = self.export_service.export_to_json(
                st.session_state.answers,
                results
            )
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name="ahp_results.json",
                mime="application/json"
            )

        # Reset button
        st.markdown("---")
        if st.button("🔄 Start New Questionnaire"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    def run(self):
        """Main application entry point."""
        self.ui.render_header()
        self.initialize_session_state()

        # Sidebar - display criteria information only
        with st.sidebar:
            st.markdown("### Questionnaire Criteria")
            st.caption("Criteria loaded from criteria.csv")
            st.markdown("---")

            for criterion in st.session_state.criteria:
                st.caption(f"• {criterion.name}")

            st.markdown("---")
            st.caption(f"**Total Criteria:** {len(st.session_state.criteria)}")
            st.caption(f"**Total Comparisons:** {len(st.session_state.criteria) * (len(st.session_state.criteria) - 1) // 2}")

            # Download accumulated results if file exists
            if os.path.exists("results.csv"):
                st.markdown("---")
                st.markdown("### 📥 Download Results")
                with open("results.csv", "rb") as f:
                    st.download_button(
                        label="Download results.csv",
                        data=f.read(),
                        file_name="results.csv",
                        mime="text/csv",
                        help="Download all accumulated questionnaire results"
                    )
                # Show file info
                try:
                    df = pd.read_csv("results.csv")
                    st.caption(f"Total responses: {len(df)}")
                except:
                    pass

            # Google Sheets link if configured
            if isinstance(self.persistence_service, GoogleSheetsPersistenceService):
                if self.persistence_service.is_configured():
                    st.markdown("---")
                    st.markdown("### 📊 Google Sheets")
                    url = self.persistence_service.get_spreadsheet_url()
                    if url:
                        st.success("✅ Connected to Google Sheets")
                        st.markdown(f"[📄 Open Results Spreadsheet]({url})")
                        st.caption("All results are saved here permanently")
                    else:
                        st.info("Google Sheets configured")

            # Info about results storage
            st.markdown("---")
            if isinstance(self.persistence_service, GoogleSheetsPersistenceService) and self.persistence_service.is_configured():
                st.info("📊 Results are automatically saved to Google Sheets.")
            else:
                st.info("📊 Results are saved to results.csv (download before app restarts).")

        # Scale guide
        self.ui.render_scale_guide()

        st.markdown("---")

        # Main flow
        if not st.session_state.completed:
            self.run_questionnaire_flow()
        else:
            self.run_results_flow()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Application entry point with dependency injection."""

    # Determine criteria source (CSV file or default)
    criteria_file = "criteria.csv"
    if os.path.exists(criteria_file):
        data_source = CSVQuestionnaireDataSource(criteria_file)
    else:
        st.warning(f"⚠️ {criteria_file} not found. Using default criteria.")
        data_source = DefaultQuestionnaireDataSource()

    # Create dependencies (Dependency Inversion)
    calculator = AHPCalculator()
    export_service = ExportService()

    # Use Google Sheets if configured, otherwise local CSV
    sheets_service = GoogleSheetsPersistenceService(sheet_name="AHP Questionnaire Results")
    if sheets_service.is_configured():
        persistence_service = sheets_service
        print("✓ Using Google Sheets for permanent storage")
        st.sidebar.success("✅ Google Sheets connected!")
    else:
        persistence_service = PersistenceService(results_file="results.csv")
        print("⚠ Using local CSV (ephemeral on Streamlit Cloud)")
        error_msg = "⚠️ Using local CSV (Google Sheets not configured)"
        if sheets_service.error_message:
            error_msg += f"\n\nError: {sheets_service.error_message}"
        st.sidebar.warning(error_msg)

    # Inject dependencies into app
    app = AHPQuestionnaireApp(
        data_source=data_source,
        calculator=calculator,
        export_service=export_service,
        persistence_service=persistence_service
    )

    # Run application
    app.run()


if __name__ == "__main__":
    main()
