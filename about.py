# Get to know about the user.
def about_user():
    user_data = {}

    details = ""

    user_data["goal"] = input("Please enter your goal for the weekend: ")
    user_data["goal_productivity"] = input(
        "Please enter details about your goal breakdown throughout the month or week: "
    )
    user_data["goal_breakdown"] = input(
        "Please enter details about your goal breakdown throughout the month or week: "
    )

    for key, value in user_data.items():
        details = details + f"{key}: {value} \n"
    # print(user_data)
    print(details)

    return details
