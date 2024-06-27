from engine import console
from engine import menu
from engine import functions as fc
from engine.models import Account, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telethon import TelegramClient, errors, functions
import asyncio
import os
import alembic.config

class BotNet:
    def __init__(self):
        self.exit = False
        self.db_path, self.session_path = self.generate_paths()
        os.environ['DB_PATH'] = self.db_path  # Установка переменной окружения
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        self.Session = sessionmaker(bind=self.engine)

    def generate_paths(self):
        # Проверка наличия дисков и создание папки BotNet
        for drive_letter in range(ord('C'), ord('Z') + 1):
            drive = f"{chr(drive_letter)}:\\"
            if os.path.exists(drive):
                botnet_folder = os.path.join(drive, 'BotNet')
                if not os.path.exists(botnet_folder):
                    os.makedirs(botnet_folder)
                
                session_folder = os.path.join(botnet_folder, 'sessions')
                if not os.path.exists(session_folder):
                    os.makedirs(session_folder)
                
                db_path = os.path.join(botnet_folder, 'database.db')
                return db_path, session_folder
        raise Exception("No available drives found.")

    def run_alembic_migrations(self):
        alembic_args = [
            '--raiseerr',
            'upgrade', 'head'
        ]
        alembic.config.main(argv=alembic_args)

    async def main(self):
        while not self.exit:
            fc.clear_console()
            self.print_menu(menu.main_menu)
            answer = self.get_user_choice()

            fc.clear_console()
            await self.handle_choice(answer)

    def print_menu(self, menu):
        print("=" * 30)
        print(menu)
        print("=" * 30)

    def get_user_choice(self):
        try:
            return int(input("Ваш выбор >> "))
        except ValueError:
            return -1  # Неверный выбор

    async def handle_choice(self, choice):
        if choice == 0:
            await console.log("Досвидания!")
            self.exit = True
        elif choice == 1:
            while True:
                fc.clear_console()
                self.print_menu(menu.control_accounts)
                answer = self.get_user_choice()
                if await self.handle_account_choice(answer):
                    break
        elif choice == 2:
            while True:
                fc.clear_console()
                self.print_menu(menu.functions_menu)
                answer = self.get_user_choice()
                if await self.handle_functions_choice(answer):
                    break
        else:
            await console.warning("Неверный выбор. Пожалуйста, попробуйте снова.")

    async def handle_account_choice(self, choice):
        if choice == 0:
            return True  # Возвращаемся в главное меню
        
        elif choice == 1:
            fc.clear_console()
            await console.log("Список аккаунтов...")
            async with self.Session() as session:
                accounts = session.query(Account).all()
                if accounts:
                    for account in accounts:
                        status = "Работает" if account.status else "Не работает"
                        print(f"[{account.id}] {account.username} | {account.first_name} {account.last_name} | {status}")
                else:
                    print("Нет добавленных аккаунтов.")
            input("\nНажмите Enter для продолжения...")
        elif choice == 2:
            fc.clear_console()
            await console.log("Добавление аккаунта...")
            app_id = input("Введите app_id >> ")
            hash_id = input("Введите hash_id >> ")
            phone_number = input("Введите номер телефона (с кодом страны, например +37258109748) >> ")
            session_file = os.path.join(self.session_path, f"{phone_number}.session")
            client = TelegramClient(session_file, int(app_id), hash_id)

            async with client:
                try:
                    await client.connect()
                    if not await client.is_user_authorized():
                        await client.send_code_request(phone_number)
                        code = input("Введите код, полученный по SMS: ")
                        try:
                            await client.sign_in(phone_number, code)
                        except errors.SessionPasswordNeededError:
                            password = input('Введите пароль: ')
                            await client.sign_in(password=password)
                    
                    me = await client.get_me()
                    username = me.username
                    user_id = me.id
                    first_name = me.first_name
                    last_name = me.last_name

                    print(f"Телеграм аккаунт для пользователя {username} зарегистрирован.")
                    async with self.Session() as session:
                        new_account = Account(
                            app_id=app_id,
                            hash_id=hash_id,
                            username=username,
                            user_id=user_id,
                            first_name=first_name,
                            last_name=last_name,
                            status=True
                        )
                        session.add(new_account)
                        await session.commit()
                        await console.log("Аккаунт добавлен.")
                except Exception as e:
                    await console.error(f"Ошибка регистрации: {e}")
            input("\nНажмите Enter для продолжения...")
        elif choice == 3:
            fc.clear_console()
            await console.log("Удаление аккаунта...")
            account_id = int(input("Введите id аккаунта для удаления >> "))
            async with self.Session() as session:
                account_to_delete = session.query(Account).filter(Account.id == account_id).first()
                if account_to_delete:
                    session.delete(account_to_delete)
                    await session.commit()
                    await console.log("Аккаунт удален.")
                else:
                    await console.error("Аккаунт не найден.")
            input("\nНажмите Enter для продолжения...")
        else:
            await console.warning("Неверный выбор. Пожалуйста, попробуйте снова.")
            return False
        return False

    async def handle_functions_choice(self, choice):
        if choice == 0:
            return True  # Возвращаемся в главное меню

        elif choice == 1:
            fc.clear_console()
            await console.log("Подписка на канал...")
            channel = input("Введите username или ссылку на канал >> ")

            async def process_account(account, channel):
                session_file = os.path.join(self.session_path, f"{account.username}.session")
                client = TelegramClient(session_file, int(account.app_id), account.hash_id)
                async with client:
                    try:
                        await client.connect()
                        if not await client.is_user_authorized():
                            print(f"Аккаунт {account.username} не авторизован.")
                            return
                        await client(functions.channels.JoinChannelRequest(channel))
                        print(f"Аккаунт {account.username} подписался на {channel}.")
                    except errors.FloodWaitError as e:
                        print(f"Аккаунт {account.username} попал в флуд-контроль. Нужно подождать {e.seconds} секунд.")
                    except errors.TelegramAPIError as e:
                        print(f"Ошибка с аккаунтом {account.username}: {e}")
                    except Exception as e:
                        print(f"Неизвестная ошибка с аккаунтом {account.username}: {e}")

            async with self.Session() as session:
                accounts = session.query(Account).all()
                if accounts:
                    tasks = [process_account(account, channel) for account in accounts]
                    await asyncio.gather(*tasks)
                else:
                    print("Нет добавленных аккаунтов.")

            input("\nНажмите Enter для продолжения...")
        else:
            await console.warning("Неверный выбор. Пожалуйста, попробуйте снова.")
            return False
        return False

    async def start(self):
        await console.log("Иницилизация БД...")
        self.run_alembic_migrations()
        await console.log("Иницилизация BotNet завершена.")
        await self.main()

client = BotNet()

if __name__ == "__main__":
    asyncio.run(client.start())
