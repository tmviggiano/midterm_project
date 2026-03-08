from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutosaveObserver, LoggingObserver
from app.operations import OperationFactory
from colorama import Fore, Back, Style, init

init()

def calculator_repl():

    try:

        calc = Calculator()
        calc.add_observer(AutosaveObserver(calc))
        calc.add_observer(LoggingObserver())

        operations_list = ', '.join(OperationFactory.get_operations())

        print("Calculator started. Type 'help' for commands.")

        while True:
            try:
                command = input(Fore.RESET + "\nEnter command: ").lower().strip()

                if command == 'help':
                    print(Fore.YELLOW + "\nAvailable commands:")
                    print(f"{operations_list} - Perform calculations")
                    
                    print("  history - Show calculation history")
                    print("  clear - Clear calculation history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last undone calculation")
                    print("  save - Save calculation history to file")
                    print("  load - Load calculation history from file")
                    print("  exit - Exit the calculator")
                    continue
                
                if command == 'exit':
                    try:
                        calc.save_history()
                        print(Fore.GREEN + "History saved successfully")
                    except Exception as e:
                        print(Fore.RED + f"Warning: Could not save history! Reason: {e}")
                    print(Fore.GREEN + "Goodbye!")
                    #We were on a:
                    break
                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print(Fore.RED +"No calculations in history!")
                    else:
                        print( Fore.YELLOW + "\nCalculation history:")
                        for i, entry in enumerate(history,1):
                            print(f"{i}. {entry}")
                    continue
                if command == 'clear':
                    calc.clear_history()
                    print(Fore.YELLOW + "History cleared")
                    continue

                if command == 'undo':
                    if calc.undo():
                        print(Fore.YELLOW + "Operation undone")
                    else:
                        print(Fore.RED + "Nothing to undo")
                    continue

                if command == 'redo':
                    if calc.redo():
                        print(Fore.YELLOW + "Operation redone")
                    else:
                        print(Fore.RED + "Nothing to redo")
                    continue

                if command == 'save':
                    try:
                        calc.save_history()
                        print(Fore.BLUE + "History saved successfully")
                    except Exception as e:
                        print(Fore.RED + f"Error saving history: {e}")
                    continue

                if command == 'load':
                    try:
                        calc.load_history()
                        print(Fore.BLUE + "History loaded successfully")
                    except Exception as e:
                        print(Fore.RED + f"Error loading history: {e}")
                    continue

                if command in operations_list:

                    try:
                        print(Fore.CYAN +"\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() in ['cancel', 'abort']:
                            print(Fore.RED + "Operation cancelled")
                            continue
                        b = input("Second number: ")
                        if b.lower()in ['cancel', 'abort']:
                            print(Fore.RED + "Operation cancelled")
                            continue
                        calc.set_operation(command)
                        result = calc.perform_operation(a,b)
                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(Fore.GREEN + f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        print(Fore.RED + f"Error: {e}")
                    except Exception as e:
                        print(Fore.RED + f"Unexpected error: {e}")
                    continue

                print(Fore.RED + f"Unknown command: '{command}'. Type 'help' for list of available commands")
            except KeyboardInterrupt:
                print(Fore.RED + "\nOperation cancelled")
                continue
            except EOFError:
                print( Fore.RED + "\nInput terminated. Exiting...")
                break
            except Exception as e:
                print(Fore.RED + f"Error: {e}")
                continue
    except Exception as e:
        print(Fore.RED + f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise