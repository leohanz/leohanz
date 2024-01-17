ticket_counter = 1
def load_user_data():
    try:
        with open('user_data.txt', 'r') as file:
            lines = file.readlines()
            return {line.split(',')[0]: line.split(',')[1].strip() for line in lines}
    except FileNotFoundError:
        return {}

def save_user_data(user_data):
    with open('user_data.txt', 'w') as file:
        for username, password in user_data.items():
            file.write(f"{username},{password}\n")

def signup():
    print("Sign Up")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user_data = load_user_data()

    if username in user_data:
        print("Username already exists. Please choose another.")
        return

    user_data[username] = password
    save_user_data(user_data)

    print("Sign up successful. You can now log in.")

def login():
    print("Log In")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user_data = load_user_data()

    if username in user_data and user_data[username] == password:
        print(f"Welcome, {username}!")
        return True
    else:
        print("Invalid username or password. Please try again.")

def load_concert_data(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            return [(line.split(',')[0], line.split(',')[1], line.split(',')[2], float(line.split(',')[3].strip())) for line in lines]
    except FileNotFoundError:
        return []

def display_concert_info(filename):
    concert_data = load_concert_data(filename)

    if not concert_data:
        print("No concert information available.")
    else:
        print("\nConcert Information:")
        concerts = {}

        for concert in concert_data:
            concert_name, artist_name, date, base_price = concert[0], concert[1], concert[2], concert[3]

            if (concert_name, artist_name) not in concerts:
                concerts[(concert_name, artist_name)] = {'dates': [date], 'base_price': base_price}
            else:
                concerts[(concert_name, artist_name)]['dates'].append(date)

        for i, (concert_key, data) in enumerate(concerts.items(), start=1):
            concert_name, artist_name = concert_key
            print(f"Record {i}:")
            print(f"Concert Name: {concert_name}")
            print(f"Artist: {artist_name}")
            print(f"Base Price: ${data['base_price']}")
            print("Dates:")
            for date in data['dates']:
                print(f" - {date}")
            print("-" * 20)
        return concerts

def select_seat():
    print("Available seat types:")
    seat_types = ["VIP", "Premium", "Standard", "Economy"]
    seat_costs = {'VIP': 50, 'Premium': 30, 'Standard': 20, 'Economy': 10}

    for i, seat_type in enumerate(seat_types, start=1):
        print(f"{i}. {seat_type} - Additional Price: ${seat_costs[seat_type]}")

    while True:
        try:
            seat_choice = int(input("Choose the type of seat (1 to 4): "))
            if 1 <= seat_choice <= 4:
                selected_seat_type = seat_types[seat_choice - 1]
                additional_price = seat_costs[selected_seat_type]
                print(f"Seat type selected: {selected_seat_type} - Additional Price: ${additional_price}")
                return selected_seat_type
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def select_concert(filename, tickets):
    global ticket_counter  # Declare the variable as global
    concert_data = load_concert_data(filename)

    if not concert_data:
        print("No concert information available.")
    else:
        print("\nAvailable Concerts:")
        concert_data = display_concert_info(filename)

        while True:
            try:
                concert_choice = int(input("Select a concert (1 to {}): ".format(len(concert_data))))
                if 1 <= concert_choice <= len(concert_data):
                    selected_concert = list(concert_data.keys())[concert_choice - 1]
                    base_price = concert_data[selected_concert]['base_price']

                    # Check if the selected concert has multiple dates
                    if len(concert_data[selected_concert]['dates']) > 1:
                        print(f"\nConcert {selected_concert[0]} by {selected_concert[1]} has multiple dates. Please select a date:")
                        for j, date in enumerate(concert_data[selected_concert]['dates'], start=1):
                            print(f"{j}. {date}")

                        while True:
                            try:
                                date_choice = int(input("Select a date (1 to {}): ".format(len(concert_data[selected_concert]['dates']))))
                                if 1 <= date_choice <= len(concert_data[selected_concert]['dates']):
                                    selected_date = concert_data[selected_concert]['dates'][date_choice - 1]
                                    print(f"You have selected {selected_concert[0]} by {selected_concert[1]} on {selected_date}.")

                                    # Call the select_seat function
                                    seat_type = select_seat()
                                    total_price = base_price + calculate_additional_cost(seat_type)
                                    print(f"Selected Concert: {selected_concert[0]} by {selected_concert[1]}, Date: {selected_date}, Seat Type: {seat_type}, Total Price: ${total_price}")

                                    # Use the current value of the counter as the ticket number
                                    ticket_number = ticket_counter
                                    ticket_counter += 1  # Increment the counter for the next ticket

                                    tickets.append({
                                        'ticket_number': ticket_number,
                                        'concert': selected_concert,
                                        'date': selected_date,
                                        'seat_type': seat_type,
                                        'total_price': total_price
                                    })

                                    another_ticket = input("Do you want to buy another ticket? (yes/no): ").lower()
                                    if another_ticket.lower() != 'yes':
                                        return
                                    break
                                else:
                                    print("Invalid choice. Please enter a valid number.")
                            except ValueError:
                                print("Invalid input. Please enter a valid number.")
                    else:
                        seat_type = select_seat()
                        total_price = base_price + calculate_additional_cost(seat_type)
                        selected_date = concert_data[selected_concert]['dates'][0]
                        print(f"Selected Concert: {selected_concert[0]} by {selected_concert[1]}, Date: {selected_date}, Seat Type: {seat_type}, Total Price: ${total_price}")

                        # Use the current value of the counter as the ticket number
                        ticket_number = ticket_counter
                        ticket_counter += 1  # Increment the counter for the next ticket

                        tickets.append({
                            'ticket_number': ticket_number,
                            'concert': selected_concert,
                            'date': selected_date,
                            'seat_type': seat_type,
                            'total_price': total_price
                        })

                        another_ticket = input("Do you want to buy another ticket? (yes/no): ").lower()
                        if another_ticket.lower() != 'yes':
                            return
                        break
                else:
                    print("Invalid choice. Please enter a number between 1 and {}.".format(len(concert_data)))
            except ValueError:
                print("Invalid input. Please enter a valid number.")



def calculate_additional_cost(seat_type):
    # Define additional costs for each seat type
    seat_costs = {'VIP': 50, 'Premium': 30, 'Standard': 20, 'Economy': 10}

    # Return the additional cost for the selected seat type
    return seat_costs.get(seat_type, 0)

def view_tickets(tickets):
    if not tickets:
        print("No tickets purchased yet.")
        return

    print("\nYour Purchased Tickets:")
    for i, ticket in enumerate(tickets, start=1):
        print(f"Ticket {i}:")
        print(f"Concert: {ticket['concert'][0]} by {ticket['concert'][1]}")
        print(f"Date: {ticket['date']}")
        print(f"Seat Type: {ticket['seat_type']}")
        print(f"Total Price: ${ticket['total_price']}")
        print("-" * 20)

def make_payment(tickets):
    if not tickets:
        print("No tickets purchased yet.")
        return

    print("\nYour Purchased Tickets:")
    total_price = 0

    for i, ticket in enumerate(tickets, start=1):
        print(f"Ticket {i}:")
        print(f"Concert: {ticket['concert'][0]} by {ticket['concert'][1]}")
        print(f"Date: {ticket['date']}")
        print(f"Seat Type: {ticket['seat_type']}")
        print(f"Total Price: ${ticket['total_price']}")
        print("-" * 20)

        total_price += ticket['total_price']

    # Calculate tax (6%)
    tax = 0.06 * total_price
    total_price_with_tax = total_price + tax

    print(f"\nTotal Price: ${total_price}")
    print(f"Tax (6%): ${tax}")
    print(f"Total Price with Tax: ${total_price_with_tax}")

    # Ask the user to pay
    while True:
        try:
            payment_amount = float(input("Enter the amount you want to pay: $"))
            if payment_amount >= total_price_with_tax:
                change = payment_amount - total_price_with_tax
                if change > 0:
                    print(f"Payment successful. Your change: ${change:.2f}")
                else:
                    print("Payment successful. Thank you!")
                break
            else:
                print("Insufficient payment. Please enter an amount equal to or greater than the total price.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")


def update_ticket(tickets):
    view_tickets(tickets)
    if not tickets:
        print("No tickets to update.")
        return

    try:
        ticket_number_to_update = int(input("Enter the ticket number you want to update: "))
        for ticket in tickets:
            if ticket['ticket_number'] == ticket_number_to_update:
                print(f"Updating Ticket {ticket['ticket_number']}:")
                print(f"Concert: {ticket['concert'][0]} by {ticket['concert'][1]}")
                print(f"Date: {ticket['date']}")
                print(f"Seat Type: {ticket['seat_type']}")
                print(f"Total Price: ${ticket['total_price']}")

                # Retrieve the base price from concert data
                concert_data = load_concert_data("concerts.txt")
                selected_concert = ticket['concert']
                base_price = next(item[3] for item in concert_data if item[0] == selected_concert[0] and item[1] == selected_concert[1])

                # Ask the user for a new seat type
                new_seat_type = select_seat()
                new_total_price = base_price + calculate_additional_cost(new_seat_type)

                # Update the ticket information
                ticket['seat_type'] = new_seat_type
                ticket['total_price'] = new_total_price

                print("Ticket updated successfully.")
                return

        print(f"No ticket found with ticket number {ticket_number_to_update}.")
    except ValueError:
        print("Invalid input. Please enter a valid ticket number.")


def delete_ticket(tickets):
    view_tickets(tickets)
    if not tickets:
        print("No tickets to delete.")
        return

    try:
        ticket_number_to_delete = int(input("Enter the ticket number you want to delete: "))
        for ticket in tickets:
            if ticket['ticket_number'] == ticket_number_to_delete:
                print(f"Deleting Ticket {ticket['ticket_number']}:")
                print(f"Concert: {ticket['concert'][0]} by {ticket['concert'][1]}")
                print(f"Date: {ticket['date']}")
                print(f"Seat Type: {ticket['seat_type']}")
                print(f"Total Price: ${ticket['total_price']}")

                # Confirm deletion
                confirm_delete = input("Do you want to delete this ticket? (yes/no): ").lower()
                if confirm_delete == 'yes':
                    tickets.remove(ticket)
                    print("Ticket deleted successfully.")
                    return
                else:
                    print("Ticket not deleted.")
                    return

        print(f"No ticket found with ticket number {ticket_number_to_delete}.")
    except ValueError:
        print("Invalid input. Please enter a valid ticket number.")


def main():
    user_authenticated = False  # Flag to track user authentication
    filename = "concerts.txt"
    tickets = []  # Array to store ticket details

    while True:
        print("\nConcert Ticket Booking System")

        if user_authenticated:
            print("1. Display Concert Info")
            print("2. Buy Concert Ticket")
            print("3. View My Tickets")
            print("4. Update Ticket")
            print("5. Delete Ticket")
            print("6. Make Payment")
            print("7. Logout")
            print("8. Exit")
        else:
            print("1. Sign Up")
            print("2. Log In")
            print("3. Exit")

        choice = input("Select an option: ")

        if user_authenticated:
            if choice == '1':
                display_concert_info(filename)
            elif choice == '2':
                # Allow the user to buy multiple tickets
                select_concert(filename, tickets)
            elif choice == '3':
                view_tickets(tickets)
            elif choice == '4':
                update_ticket(tickets)
            elif choice == '5':
                delete_ticket(tickets)
            elif choice == '6':
                make_payment(tickets)
                break
            elif choice == '7':
                print("Logging out.")
                user_authenticated = False
            elif choice == '8':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            if choice == '1':
                signup()
                user_authenticated = login()
            elif choice == '2':
                user_authenticated = login()
            elif choice == '3':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
