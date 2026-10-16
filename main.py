import json

import request_manager as rm
import access_workflow as workflow


DATA_FILE = "requests.json"


def display_menu():
    print("\n=== CAMPUS ACCESS ===")
    print("1. Create request")
    print("2. View request")
    print("3. Approve request")
    print("4. Issue card")
    print("5. Return card")
    print("6. List requests")
    print("7. Save requests")
    print("8. Reload requests")
    print("9. Quit")


def create_request():
    fellow_id = input("Fellow ID: ")
    card_type = input(
        "Card type (visitor/student/staff): "
    ).strip().lower()

    request = rm.create_request(fellow_id, card_type)
    print("Request created:", request)


def view_request():
    request_id = input("Request ID: ").strip()
    request = rm.get_request(request_id)

    if request is None:
        print("Request not found.")
    else:
        print(request)


def approve_card():
    request_id = input("Request ID: ").strip()
    approved_by = input("Approver ID: ").strip()

    request = workflow.approve_request(request_id, approved_by)
    print("Request approved:", request)


def issue_card():
    request_id = input("Request ID: ").strip()

    request = workflow.issue_request(request_id)
    print("Card issued:", request)


def return_card():
    request_id = input("Request ID: ").strip()

    request = workflow.return_request(request_id)
    print("Card returned:", request)


def list_requests():
    if not rm.requests:
        print("No requests found.")
        return

    for request in rm.requests:
        print(request)


def save_requests():
    rm.save_requests(DATA_FILE)
    print(f"Requests saved to {DATA_FILE}.")


def reload_requests():
    rm.load_requests(DATA_FILE)
    print(f"Requests loaded from {DATA_FILE}.")


def main():
    actions = {
        "1": create_request,
        "2": view_request,
        "3": approve_card,
        "4": issue_card,
        "5": return_card,
        "6": list_requests,
        "7": save_requests,
        "8": reload_requests,
    }

    while True:
        display_menu()
        choice = input("Choose an option (1-9): ").strip()

        if choice == "9":
            print("Goodbye!")
            break

        action = actions.get(choice)

        if action is None:
            print("Invalid option. Please choose from 1 to 9.")
            continue

        try:
            action()
        except (ValueError, OSError, json.JSONDecodeError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
