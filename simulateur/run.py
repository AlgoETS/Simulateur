import sys
import os
import subprocess
import argparse
import threading

def install_requirements():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        sys.exit(1)

def apply_migrations():
    try:
        subprocess.check_call([sys.executable, 'manage.py', 'makemigrations'])
        subprocess.check_call([sys.executable, 'manage.py', 'migrate'])
    except subprocess.CalledProcessError as e:
        print(f"Failed to apply migrations: {e}")
        sys.exit(1)

def start_simulation(simulation_id):
    try:
        subprocess.check_call([sys.executable, 'manage.py', 'start_simulation', str(simulation_id)])
    except subprocess.CalledProcessError as e:
        print(f"Failed to start simulation: {e}")
        sys.exit(1)

def daphne_server(bind, port):
    import django
    # Set the Django settings module environment variable
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simulateur.settings")

    # Set the command-line arguments for Daphne
    sys.argv = ['daphne', 'simulateur.asgi:application', '-b', bind, '-p', port]

    # Set up Django
    django.setup()

    # Run Daphne
    from daphne.cli import CommandLineInterface
    CommandLineInterface.entrypoint()

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the Daphne server with optional steps.')
    parser.add_argument('--quick', action='store_true', help='Skip installing requirements and applying migrations')
    parser.add_argument('--install', action='store_true', help='Only install requirements')
    parser.add_argument('--start-simulation', type=int, help='Start a simulation with the given ID')
    parser.add_argument('-b', '--bind', default='0.0.0.0', help='Bind address')
    parser.add_argument('-p', '--port', default='8000', help='Port number')
    args = parser.parse_args()

    if args.install:
        # Only install requirements and exit
        install_requirements()
        sys.exit(0)

    if not args.quick:
        # Install requirements
        install_requirements()

        # Apply migrations
        apply_migrations()

    # Start the Daphne server in a separate thread
    daphne_thread = threading.Thread(target=daphne_server, args=(args.bind, args.port))
    daphne_thread.start()

    # Start simulation if the argument is provided
    if args.start_simulation is not None:
        start_simulation_thread = threading.Thread(target=start_simulation, args=(args.start_simulation,))
        start_simulation_thread.start()

    # Wait for threads to complete
    daphne_thread.join()
    if args.start_simulation is not None:
        start_simulation_thread.join()
