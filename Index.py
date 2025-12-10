# - Main Page for IRCTCS Train Booking App [Simple Version - V1.0.0.04.10.25]
# - C:\Users\erlaa\Datasets-Py\Sprint\Sprint-Pro-1

import random
import json
import os

# File paths
USERDATA = "Userdata.json"
DATASET = "Dataset.json"

# ----------------- Utility Functions -----------------

def read_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def write_json(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

def generate_user_id():
    return "".join(map(str, random.choices(range(1, 10), k=7)))

# ----------------- Account Functions -----------------

def add_account(name, mobile):
    data = read_json(USERDATA)

    unique_id = generate_user_id()
    new_user = {
        "Name": name,
        "Mobile": str(mobile),
        "LoginId": unique_id,
        "Orders": []
    }

    data.append(new_user)
    write_json(USERDATA, data)

    return f"\n - Account Created [UserID : {unique_id}]"

def check_account(user_id, user_mobile):
    data = read_json(USERDATA)

    for user in data:
        if user["LoginId"] == user_id and user["Mobile"] == str(user_mobile):
            print(f"\n - {user['Name']}, Welcome To IRCTC..")
            return user["LoginId"]   # return only id
    return None

# ----------------- Show Trains ---------------

def show_trains():
    data = read_json(DATASET)
    for train in data:
        print("\n---------------- Train Details ----------------") 
        print(f" - Train Name : {train['TrainName']}") 
        print(f" - Train Number : {train['TrainNo']}") 
        print(f" - Route : {train['Source']} --> {train['Destination']}") 
        print(f" - Departure : {train['Departure']} | Arrival : {train['Arrival']}") 
        print(f" - Duration : {train['Duration']}") 
        print(f" - Sleeper Seats : {train['Seats (Sleeper)']} | Fare : ₹{train['Fare (Sleeper)']}") 
        print(f" - AC Seats : {train['Seats (AC)']} | Fare : ₹{train['Fare (AC)']}")

# ---------------- Book Train -----------------

def book_train(user_id, train_no, train_coach, noof_seats):
    trains_data = read_json(DATASET)
    users_data = read_json(USERDATA)

    # Find user
    user_index = None
    for i in range(len(users_data)):
        if users_data[i]["LoginId"] == user_id:
            user_index = i
            break

    if user_index is None:
        return "\n - User not found in records."

    # Find train
    train = None
    for t in trains_data:
        if t["TrainNo"] == train_no:
            train = t
            break

    if train is None:
        return "\n - Train Not Found"

    if train_coach.upper() == "SLP":
        seat_type = "Seats (Sleeper)"
        fare_type = "Fare (Sleeper)"
    elif train_coach.upper() == "AC":
        seat_type = "Seats (AC)"
        fare_type = "Fare (AC)"
    else:
        return "\n - Invalid Coach. Try Again."

    if train[seat_type] >= noof_seats:
        total_amount = train[fare_type] * noof_seats
        print("\n - Your", noof_seats, "Tickets are Available || Total Amount : ₹", total_amount)

        train[seat_type] -= noof_seats

        order = {
            "Train_Name": train["TrainName"],
            "Train_No": train["TrainNo"],
            "Coach": train_coach.upper(),
            "Tickets Booked": noof_seats,
            "Price": total_amount
        }

        users_data[user_index]["Orders"].append(order)

        write_json(USERDATA, users_data)
        write_json(DATASET, trains_data)

        return "\n - Tickets Confirmed & SMS sent to your Mobile Number."
    else:
        return "\n - Not Enough Tickets Available."

# ----------------- Show Orders -----------------

def show_orders(user_id):
    users_data = read_json(USERDATA)
    user_index=None
    for i in range(0,len(users_data)):
        if users_data[i]["LoginId"]==user_id :
            user_index=i
    user_details=users_data[user_index]["Orders"]
    print("\n - Total Bookings : ",len(user_details))
    
    for i in range(0,len(user_details)):
        print(f"\n - Ticket [{i+1}] -- | {user_details[i]} |")
    

# ----------------- Main Menu -----------------

def main():
    print("\n -- IRCTC Train Booking App -- \n")
    choice = input(" . [0] Create Account || [1] Login Account : ").strip()

    if choice == "0":
        user_name = input("\n . Enter Full Name : ").strip()
        user_mobile = input("\n . Enter Mobile : ").strip()
        print(add_account(user_name, user_mobile))

    elif choice == "1":
        user_id = input("\n . Enter User ID : ").strip()
        user_mobile = input("\n . Enter Mobile : ").strip()
        login_id = check_account(user_id, user_mobile)

        if not login_id:
            print("\n - User Not Found")
            return

        while True:
            select = input("\n . [1] Show Trains || [2] Book A Ticket || [3] Your Orders || [0] Exit : ").strip()
            if select == "1":
                show_trains()
            elif select == "2":
                show_trains()
                train_no = input("\n - Enter Train No : ").strip()
                train_coach = input("\n - [SLP] Sleeper || [AC] AC : ").strip()
                try:
                    noof_seats = int(input("\n - Enter No Of Tickets : "))
                except ValueError:
                    print("\n - Invalid seat number.")
                    continue
                print(book_train(login_id, train_no, train_coach, noof_seats))
            elif select == "3":
                show_orders(login_id)
            elif select == "0":
                print("\n - Thanks For Visiting IRCTC APP.")
                break
            else:
                print("\n - Invalid Option. Try Again..")
    else:
        print("\n - Invalid Option. Try Again..")

# ----------------- Run -----------------

if __name__ == "__main__":
    main()
