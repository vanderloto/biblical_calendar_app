"""Run script for Biblical Calendar Web Backend.

This script creates an isolated environment and runs the Flask app.
"""

import subprocess
import sys
import os
import venv

def create_venv():
    """Create virtual environment if it doesn't exist."""
    venv_path = os.path.join(os.path.dirname(__file__), 'venv')
    if not os.path.exists(venv_path):
        print("📦 Creating virtual environment...")
        venv.create(venv_path, with_pip=True)
    return venv_path

def get_venv_python(venv_path):
    """Get path to Python executable in venv."""
    if os.name == 'nt':  # Windows
        return os.path.join(venv_path, 'Scripts', 'python.exe')
    else:  # Unix-like
        return os.path.join(venv_path, 'bin', 'python')

def install_requirements(python_exe):
    """Install requirements with compatible numpy version."""
    print("🔧 Installing compatible dependencies...")
    
    # Install numpy first with compatible version
    subprocess.check_call([
        python_exe, "-m", "pip", "install", "numpy<2.0", "--upgrade"
    ])
    
    # Install other requirements
    subprocess.check_call([
        python_exe, "-m", "pip", "install", "-r", "requirements.txt"
    ])

def setup_path():
    """Setup Python path for imports."""
    src_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src')
    src_path = os.path.abspath(src_path)
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

def main():
    """Main entry point."""
    # Create isolated venv
    venv_path = create_venv()
    python_exe = get_venv_python(venv_path)
    
    # Check if dependencies are installed
    try:
        result = subprocess.run([
            python_exe, "-c", "import numpy; import skyfield; print('Dependencies OK')"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            install_requirements(python_exe)
            
    except Exception:
        install_requirements(python_exe)
    
    # Run the app with venv python
    print("🚀 Starting Biblical Calendar Web Backend...")
    env = os.environ.copy()
    src_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src')
    env['PYTHONPATH'] = os.path.abspath(src_path)
    
    subprocess.run([python_exe, "app.py"], env=env)

if __name__ == "__main__":
    main()