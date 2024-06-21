import os
import alembic.config

def generate_db_path():
    # Проверка наличия дисков и создание папки BotNet
    for drive_letter in range(ord('C'), ord('Z') + 1):
        drive = f"{chr(drive_letter)}:\\"
        if os.path.exists(drive):
            botnet_folder = os.path.join(drive, 'BotNet')
            if not os.path.exists(botnet_folder):
                os.makedirs(botnet_folder)
            return os.path.join(botnet_folder, 'database.db')
    raise Exception("No available drives found.")

if __name__ == "__main__":
    db_path = generate_db_path()
    os.environ['DB_PATH'] = db_path

    alembic_args = [
        '--raiseerr',
        'upgrade', 'head'
    ]
    alembic.config.main(argv=alembic_args)
