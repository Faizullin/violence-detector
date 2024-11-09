from django.db import connection
import os
import shutil
import subprocess
import sys


def remigrate(use_psotgre):

    def delete_migrations_folders(root_folder, exclude_dirs):
        exclude_dirs = [os.path.normpath(d) for d in exclude_dirs]
        for root, dirs, files in os.walk(root_folder):
            ok = True
            for j in exclude_dirs:
                if root.startswith(j) or root.startswith(os.path.join('.', j)):
                    ok = False
                    break
            if ok:
                for dir_name in dirs:
                    if dir_name == 'migrations':
                        folder_path = os.path.join(root, dir_name)
                        print(f"Cleaning folder: {folder_path}")
                        for subroot, subdirs, subfiles in os.walk(folder_path):
                            for i in subdirs:
                                shutil.rmtree(os.path.join(subroot, i))
                            for i in subfiles:
                                os.remove(os.path.join(subroot, i))

                            with open(os.path.join(subroot, '__init__.py'), 'w'):
                                pass
                        break


    def delete_db(root_folder):
        db_path = os.path.join(root_folder, 'db.sqlite3')
        if os.path.exists(db_path):
            os.remove(db_path)
        if use_psotgre:
            with connection.cursor() as cursor:
                cursor.execute("""
                    DO $$ DECLARE
                    r RECORD;
                    BEGIN
                        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                        END LOOP;
                    END $$;
                """)
        print('Successfully dropped all tables')


    root_folder = "."
    delete_db(root_folder)
    delete_migrations_folders(root_folder, exclude_dirs=['.venv'],)

    if '-n' in sys.argv:
        sys.exit()

    win = os.name == 'nt'
    python_cmd = 'py' if win else 'python3'

    subprocess.run([python_cmd, 'manage.py', 'makemigrations'])
    subprocess.run([python_cmd, 'manage.py', 'migrate'])
    seed_command = f"from seeding.seed import seed; seed({str(use_psotgre)});"
    if win:
        subprocess.run([python_cmd, 'manage.py', 'shell', '-c', seed_command])
    else:
        subprocess.run(
            f'echo "{seed_command}" | {python_cmd} manage.py shell', shell=True)
