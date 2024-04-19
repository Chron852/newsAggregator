import requests

base_url = "http://127.0.0.1:8000/"
session = requests.Session()


def login(url):
    while True:
        global base_url
        if url == "local":
            base_url = "http://127.0.0.1:8000/"
        elif not url or not isinstance(url, str) or 'http' not in url:
            print("Invalid URL")
            break
        else:
            base_url = url

        login_url = base_url + "api/login"
        credentials = input("Enter your username and password (separated by a space, enter exit to exit): ").split()

        # check the validation of the input
        if len(credentials) == 1 and credentials[0] == 'exit':
            break
        if len(credentials) != 2:
            print("Invalid input. Please provide both username and password separated by a space.")
            continue

        # add input to payload and send it by json
        payload = {
            "username": credentials[0],
            "password": credentials[1]
        }

        response = session.post(login_url, json=payload)
        if response.status_code == 200:
            print(response.content.decode())
            break  # login successfully, exit the loop
        else:
            print('Login failed. Please check your username and password.')


def logout():
    logout_url = base_url + "api/logout"
    response = session.post(logout_url)
    if response.status_code == 200:
        print(response.content.decode())
    else:
        print("Logout failed.")


def post():
    post_url = base_url + "api/stories"

    # get information by input
    headline = input("Enter the headline: ")
    category = input("Enter the category(pol, art, tech, trivial): ")
    region = input("Enter the region(uk, eu, w): ")
    details = input("Enter the details: ")

    # add information to payload and send it by json
    payload = {
        "headline": headline,
        "category": category,
        "region": region,
        "details": details
    }
    response = session.post(post_url, json=payload)
    if response.status_code == 201:
        print(response.content.decode())
    elif response.status_code == 503:
        print(response.content.decode())
    else:
        print("Failed to post news story.")


def news(key, category, region, date):
    url = "https://newssites.pythonanywhere.com/api/directory"
    response = session.get(url)
    if response.status_code != 200:
        print(response.content.decode())
    agencies = response.json()

    if key == "*":
        for index, agency in enumerate(agencies):
            get_url = f"{agency['url'].rstrip('/')}/api/stories"

            # add it to payload and send it by json
            payload = {
                "category": category,
                "region": region,
                "date": date
            }

            response = session.get(get_url, json=payload)
            if response.status_code == 200:
                # get stories
                news_stories = response.json()['stories']
                print("News stories:")
                for story in news_stories:
                    print(f"Headline: {story['headline']}")
                    print(f"Category: {story['story_cat']}")
                    print(f"Region: {story['story_region']}")
                    print(f"Details: {story['story_details']}")
                    print("-------------------")
            elif response.status_code == 503 or response.status_code == 404:
                print(response.content.decode())
            else:
                print("Failed to retrieve news stories.")
    else:
        get_url = base_url + "api/stories"

        # add it to payload and send it by json
        payload = {
            "category": category,
            "region": region,
            "date": date
        }

        response = session.get(get_url, json=payload)
        if response.status_code == 200:
            # get stories
            news_stories = response.json()['stories']
            print("News stories:")
            for story in news_stories:
                print(f"Headline: {story['headline']}")
                print(f"Category: {story['story_cat']}")
                print(f"Region: {story['story_region']}")
                print(f"Details: {story['story_details']}")
                print("-------------------")
        elif response.status_code == 503 or response.status_code == 404:
            print(response.content.decode())
        else:
            print("Failed to retrieve news stories.")


def list_services():
    list_url = base_url + "api/directory"
    response = session.get(list_url)
    if response.status_code == 200:
        services = response.json()['agency_list']
        print("News services in the directory:")
        for service in services:
            print(f"Agency name: {service['agency_name']}")
            print(f"Url: {service['url']}")
            print(f"Agency_code: {service['agency_code']}")
            print("-------------------")
    elif response.status_code == 500:
        print(response.content.decode())
    else:
        print("Failed to retrieve news services.")


def delete(story_key):
    delete_url = base_url + "api/stories/" + story_key
    payload = {
        "key": story_key
    }
    response = session.delete(delete_url, json=payload)
    if response.status_code == 200:
        print("News story deleted successfully.")
    elif response.status_code == 503:
        print(response.content.decode())
    else:
        print("Failed to delete news story.")


def command_line_interface():
    while True:
        command = input(
            """
╔══════════════════════════════════════╗
║           Available Commands         ║
╠══════════════════════════════════════╣
║ login [url]                          ║
║ logout                               ║
║ post                                 ║
║ news [-id=] [-cat=] [-reg=] [-date=] ║
║ list                                 ║
║ delete [key]                         ║
║ exit                                 ║
╚══════════════════════════════════════╝

Enter a command: 
"""
        )
        if command.startswith("login"):
            url = command.split()
            if len(url) == 2:
                login(url[1])
            else:
                print("Invalid command.")
        elif command == "logout":
            logout()
        elif command == "post":
            post()
        elif command.startswith("news"):
            args = command[1:]

            key = next((arg.split('=')[1] for arg in args if arg.startswith('-id=')), None)
            category = next((arg.split('=')[1] for arg in args if arg.startswith('-cat=')), '*')
            region = next((arg.split('=')[1] for arg in args if arg.startswith('-reg=')), '*')
            date = next((arg.split('=')[1] for arg in args if arg.startswith('-date=')), '*')
            news(key, category, region, date)
        elif command == "list":
            list_services()
        elif command.startswith("delete"):
            story_key = command.split()[1]
            delete(story_key)
        elif command == "exit":
            break
        else:
            print("Invalid command. Please try again.")


# Run the command line interface
command_line_interface()
