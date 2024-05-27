import src.Homeworks.homework1.task1.Registry as Registry
import src.Homeworks.homework2.Actions as Actions
from src.Homeworks.homework2.Performed_command_storage import PerformedCommandStorage


def write_info(act_registry: Registry.Registry) -> str:
    result_str = "Available commands:\n" "1.info\n" "2.exit\n" "3.cancel\n"
    for i, action in enumerate(act_registry.registry.keys()):
        result_str += f"{i + 4}. {action}\n"
    return result_str


def main() -> None:
    user_request = ""
    user_collection = eval(input("input your collection([1, 2, 3], e.t.c): "))
    info = write_info(Actions.ACTIONS_REGISTRY)
    command_storage = PerformedCommandStorage(user_collection)
    print(info)
    while user_request != "exit":
        user_request = input("Enter your request: ")
        if user_request == "exit":
            print("End programme")
            break
        elif user_request == "info":
            print(info + f"Your collection: {user_collection}")
        elif user_request == "cancel":
            try:
                command_storage.cancel()
            except ValueError as error:
                print(error)
            else:
                print("Your collection: ", user_collection)
        else:
            action, *arguments = user_request.split(" ")
            arguments = map(int, arguments)
            try:
                command_storage.apply(Actions.ACTIONS_REGISTRY.dispatch(action)(*arguments))
            except ValueError as error:
                print(error)
            except TypeError:
                print("Wrong number of arguments")
            except Exception as error:
                print(f"Unexpected error: {error}")
            finally:
                print(f"Your collection: {user_collection}")


if __name__ == "__main__":
    main()
