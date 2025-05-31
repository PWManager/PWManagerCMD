import os
import platform
import sys
import colorama
from datetime import datetime

def set_console_title(title):
    system = platform.system()
    if system == "Windows":
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    elif system in ["Linux", "Darwin"]:
        sys.stdout.write(f"\x1b]2;{title}\x07")
        sys.stdout.flush()
        
class MessageTypes:
    def print_success(self, message):
        print(colorama.Fore.GREEN + message + colorama.Style.RESET_ALL)
    
    def print_error(self, message):
        print(colorama.Fore.RED + message + colorama.Style.RESET_ALL)
    
    def print_warning(self, message):
        print(colorama.Fore.YELLOW + message + colorama.Style.RESET_ALL)
        
    def print_info(self, message):
        print(colorama.Fore.BLUE + message + colorama.Style.RESET_ALL)
    
    def print_debug(self, message):
        print(colorama.Fore.MAGENTA + message + colorama.Style.RESET_ALL)
        
    def print_custom(self, message, color):
        print(color + message + colorama.Style.RESET_ALL)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def wget(url, save_path):
    try:
        import wget
        wget.download(url, out=save_path)
        msgtypes.print_success(f"\nФайл успешно загружен и сохранен как {save_path}")
    except Exception as e:
        msgtypes.print_error(f"Ошибка при загрузке файла: {e}")

def show_help():
    help_text = """
Доступные команды:
    help    - Показать это сообщение
    clear   - Очистить экран
    pwd     - Показать текущий путь
    ls      - Показать содержимое текущей директории
    cd      - Сменить директорию
    echo    - Вывести текст
    exit    - Выйти из программы
    sudo inlinepython - Выполнить Python код
    """
    print(help_text)

def list_directory():
    try:
        items = os.listdir(path)
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                print(colorama.Fore.BLUE + item + "/" + colorama.Style.RESET_ALL)
            else:
                print(item)
    except Exception as e:
        msgtypes.print_error(f"Ошибка при чтении директории: {e}")

set_console_title("PWManagerCMD")

if os.name == "nt":
    path = f"C:\\Users\\{os.getlogin()}"
else:
    path = os.path.expanduser("~")
    
os.chdir(path)

exit_ = False

msgtypes = MessageTypes()

print("Welcome to the PWManagerCMD shell")

try:
    while not exit_:
        cmd = input(f"{path}$> ").strip()
        
        if cmd == "exit":
            exit_ = True
            
        elif cmd == "help":
            show_help()
            
        elif cmd == "clear":
            clear_screen()
            
        elif cmd == "pwd":
            print(path)
            
        elif cmd == "ls":
            list_directory()
            
        elif cmd.startswith("echo "):
            print(cmd[5:])
            
        elif cmd.startswith("wget "):
            try:
                url, save_path = cmd.split(maxsplit=1)[1].split(maxsplit=1)
                wget(url, save_path)
            except ValueError:
                msgtypes.print_error("Please specify URL and save path")
            except Exception as e:
                msgtypes.print_error(f"Error: {e}")
            
        elif cmd.startswith("cd"):
            try:
                todir = cmd.split(maxsplit=1)[1]
                if todir == "..":
                    new_path = os.path.dirname(path)
                else:
                    new_path = os.path.abspath(os.path.join(path, todir))
                
                if os.path.isdir(new_path):
                    os.chdir(new_path)
                    path = new_path
                else:
                    msgtypes.print_error(f"Directory not found: {new_path}")
            except IndexError:
                msgtypes.print_info("Please specify directory")
            except Exception as e:
                msgtypes.print_error(f"Error: {e}")

        elif cmd.startswith("sudo inlinepython"):
            python_code = cmd.split(maxsplit=2)[2]
            msgtypes.print_warning("Warning: If you use the 'Inline Python' function, you take full responsibility!")
            try:
                result = eval(python_code.replace("\\n", "\n"))
                if result is not None:
                    print(result)
            except Exception as e:
                msgtypes.print_error(f"Python Error: {e}")
                
        elif cmd.startswith("inlinepython"):
            msgtypes.print_error("Error: 'inlinepython' command requires 'sudo' prefix.")
            
        else:
            os.system(cmd)
            
except KeyboardInterrupt:
    exit_ = True