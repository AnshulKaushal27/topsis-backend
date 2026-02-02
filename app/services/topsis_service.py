import sys
import tempfile
import os
from topsis_anshul.topsis import main as topsis_main


def run_topsis_service(
    uploaded_csv_path: str,
    weights: str,
    impacts: str
) -> str:
    """
    Runs TOPSIS using the existing CLI-style main() function.
    Returns path to the generated output CSV.
    """

    # Create a temporary output file
    temp_dir = tempfile.mkdtemp()
    output_csv_path = os.path.join(temp_dir, "topsis_result.csv")

    # Backup original sys.argv
    original_argv = sys.argv.copy()

    try:
        # Mimic CLI arguments
        sys.argv = [
            "topsis",
            uploaded_csv_path,
            weights,
            impacts,
            output_csv_path
        ]

        # Call the existing TOPSIS main()
        topsis_main()

    finally:
        # Restore original sys.argv
        sys.argv = original_argv

    return output_csv_path
