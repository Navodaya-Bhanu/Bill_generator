import json
import requests
import smtplib

# Fetch item data from API link
def fetch_items_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except Exception as e:
        print(f"Failed to fetch item data from API: {e}")
        return []

# Display available items
def display_items(items):
    print("Available Items:")
    for item in items:
        print(f"{item['id']}. {item['name']} - ₹{item['price']}")

# Select items
def select_items(items):
    selected_items = []
    while True:
        try:
            item_id = int(input("Enter the item ID to add to cart (0 to finish): "))
            if item_id == 0:
                break
            quantity = int(input("Enter quantity: "))
            item = next((item for item in items if item["id"] == item_id), None)
            if item:
                selected_items.append({"name": item["name"], "price": item["price"], "quantity": quantity})
            else:
                print("Item not found.")
        except ValueError:
            print("Invalid input. Try again.")
    return selected_items

# Calculate bill with GST
def calculate_bill(selected_items):
    total = sum(item["price"] * item["quantity"] for item in selected_items)
    gst = total * 0.18  # Assuming 18% GST
    grand_total = total + gst
    return total, gst, grand_total

# Save bill to a text file
def save_bill_to_file(bill_details):
    try:
        with open("bill.txt", "w") as file:
            file.write(bill_details)
        print("Bill saved to 'bill.txt'.")
    except Exception as e:
        print(f"Failed to save bill to file: {e}")

# Send bill via email
def send_email_bill(to_email, bill_details):
    try:
        sender_email = "chandunavoday@gmail.com"
        sender_password = "atgw smtc vmnd erug"
        
        # Construct email as a simple string
        subject = "Your Supermarket Bill"
        message = f"Subject: {subject}\n\n{bill_details}"
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message)
        print("Bill sent via email successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main program
def main():
    api_url = "http://demo9238079.mockable.io/dummmy"
    items = fetch_items_from_api(api_url)

    if not items:
        print("No items fetched. Exiting.")
        return

    display_items(items)
    selected_items = select_items(items)
    total, gst, grand_total = calculate_bill(selected_items)

    # Display bill details
    print("\nBill Details:")
    for item in selected_items:
        print(f"{item['name']} - rs{item['price']} x {item['quantity']} = rs{item['price'] * item['quantity']}")
    print(f"Total: rs{total}")
    print(f"GST (18%): rs{gst}")
    print(f"Grand Total: rs{grand_total}")

    # Prepare bill details for sending or saving
    bill_details = f"Bill Details:\n"
    for item in selected_items:
        bill_details += f"{item['name']} - rs{item['price']} x {item['quantity']} = rs{item['price'] * item['quantity']}\n"
    bill_details += f"Total: rs{total}\n"
    bill_details += f"GST (18%): rs{gst}\n"
    bill_details += f"Grand Total: rs{grand_total}\n"

    # Provide options to send or save the bill
    choice = input("Send bill via (1) Email or (2) Save as File? ")
    if choice == "1":
        to_email = input("Enter email address: ")
        send_email_bill(to_email, bill_details)
    elif choice == "2":
        save_bill_to_file(bill_details)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
