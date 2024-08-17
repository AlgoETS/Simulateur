import argparse
import os
import subprocess
import sys
import threading


def install_requirements():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--no-cache-dir'])
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


def seed_database():
    try:
        subprocess.check_call([sys.executable, 'manage.py', 'seed_database'])
    except subprocess.CalledProcessError as e:
        print(f"Failed to seed database: {e}")
        sys.exit(1)


def create_superuser(username, password):
    try:
        subprocess.check_call([
            sys.executable, 'manage.py', 'createsuperadmin',
            f'--username={username}',
            f'--password={password}',
            f'--email={username}@{password}.com'
        ])
    except subprocess.CalledProcessError as e:
        print(f"Failed to create superuser: {e}")
        sys.exit(1)


def install_requirements_cms():
    try:
        # Change directory to cms
        os.chdir('../cms')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        sys.exit(1)
    finally:
        # Change back to the original directory
        os.chdir('..')


def start_wagtail():
    try:
        # Set the correct PYTHONPATH
        pythonpath = os.path.abspath('..')
        os.environ['PYTHONPATH'] = pythonpath

        # Change directory to cms
        os.chdir('../cms')
        subprocess.check_call([sys.executable, 'manage.py', 'runserver', '8001'])
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Wagtail CMS: {e}")
        sys.exit(1)
    finally:
        # Change back to the original directory
        os.chdir('..')


def apply_migrations_cms():
    try:
        # Set the correct PYTHONPATH
        pythonpath = os.path.abspath('..')
        os.environ['PYTHONPATH'] = pythonpath

        # Change directory to cms
        os.chdir('../cms')
        subprocess.check_call([sys.executable, 'manage.py', 'migrate'])
    except subprocess.CalledProcessError as e:
        print(f"Failed to apply CMS migrations: {e}")
        sys.exit(1)
    finally:
        # Change back to the original directory
        os.chdir('..')


def create_superuser_cms(username, password):
    try:
        # Set the correct PYTHONPATH
        pythonpath = os.path.abspath('..')
        os.environ['PYTHONPATH'] = pythonpath

        # Change directory to cms
        os.chdir('../cms')
        subprocess.check_call([
            sys.executable, 'manage.py', 'createsuperuser',
            '--noinput',
            f'--username={username}',
            f'--email={username}@example.com'
        ])
        subprocess.run(
            [sys.executable, 'manage.py', 'shell'],
            input=f"from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username='{username}'); user.set_password('{password}'); user.save()",
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to create CMS superuser: {e}")
        sys.exit(1)
    finally:
        # Change back to the original directory
        os.chdir('..')


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
    parser.add_argument('--install-cms', action='store_true', help='Install and set up CMS requirements')
    parser.add_argument('--start-simulation', type=int, help='Start a simulation with the given ID')
    parser.add_argument('--create-superuser', nargs=2, metavar=('USERNAME', 'PASSWORD'),
                        help='Create a superuser with the given username and password')
    parser.add_argument('--cms', action='store_true', help='Start the Wagtail CMS server')
    parser.add_argument('--seed-database', action='store_true', help='Seed the database with initial data')
    parser.add_argument('-b', '--bind', default='0.0.0.0', help='Bind address')
    parser.add_argument('-p', '--port', default='8000', help='Port number')
    args = parser.parse_args()

    if args.install:
        # Install requirements
        install_requirements()
        # Apply migrations
        apply_migrations()
        create_superuser('admin', 'admin')
        seed_database()
        sys.exit(0)

    if args.install_cms:
        # Install CMS requirements and set up
        install_requirements_cms()
        apply_migrations_cms()
        sys.exit(0)

    if args.create_superuser:
        # Create superuser
        username, password = args.create_superuser
        create_superuser(username, password)

    # Start the Daphne server in a separate thread
    daphne_thread = threading.Thread(target=daphne_server, args=(args.bind, args.port))
    daphne_thread.start()

    # Start simulation if the argument is provided
    if args.start_simulation is not None:
        start_simulation_thread = threading.Thread(target=start_simulation, args=(args.start_simulation,))
        start_simulation_thread.start()

    if args.cms:
        # Start the Wagtail CMS server in a separate thread
        wagtail_thread = threading.Thread(target=start_wagtail)
        wagtail_thread.start()

    # Wait for threads to complete
    daphne_thread.join()
    if args.start_simulation is not None:
        start_simulation_thread.join()
    if args.cms:
        wagtail_thread.join()
