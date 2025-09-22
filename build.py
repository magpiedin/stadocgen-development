import sys
import yaml
import os
import runpy
from flask_frozen import Freezer

# Add the generator directory to the Python path to allow imports
sys.path.insert(0, 'shared-generator')

from app import create_app

def build_standard(standard_name):
    """
    Builds the static site for a single standard.
    """
    print(f"--- Building site for: {standard_name} ---")

    # --- Load Configuration ---
    config_path = f"configs/{standard_name}.yaml"
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"ERROR: Configuration file not found at {config_path}")
        return
    except yaml.YAMLError as e:
        print(f"ERROR: Could not parse YAML file {config_path}: {e}")
        return

    # --- Run Pre-build Transformation Scripts ---
    if 'build_scripts' in config:
        print("--- Running pre-build scripts ---")

        # Prepare an environment for the scripts to run in
        run_env = os.environ.copy()
        if 'validation' in config and 'headings_file' in config['validation']:
            run_env['VALIDATION_HEADINGS_FILE'] = config['validation']['headings_file']

        for script_path in config['build_scripts']:
            try:
                print(f"  - Executing: {script_path}")
                runpy.run_path(script_path, init_globals=run_env)
            except Exception as e:
                print(f"ERROR: Failed to execute build script {script_path}: {e}")
                return
        print("--- Pre-build scripts complete ---")

    # --- Create the Flask App ---
    app = create_app(config)

    # --- Configure the Freezer ---
    project_root = os.path.abspath(os.path.dirname(__file__))
    destination = os.path.join(project_root, 'output', standard_name)

    app.config['FREEZER_DESTINATION'] = destination
    app.config['FREEZER_RELATIVE_URLS'] = True
    freezer = Freezer(app)

    # --- Explicitly register a URL generator ---
    @freezer.register_generator
    def url_generator():
        for route in config.get('routes', []):
            yield route['path']

    # --- Build the Site ---
    try:
        print(f"Freezing site to {app.config['FREEZER_DESTINATION']}...")
        freezer.freeze()
        print("--- Build complete! ---")
    except Exception as e:
        print(f"ERROR: An error occurred during the freezing process: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build.py <standard_name>")
        print("Example: python build.py dwc")
        sys.exit(1)

    standard_to_build = sys.argv[1]
    build_standard(standard_to_build)
