#!/usr/bin/env python3
"""Script that displays the upcoming launch"""

import requests

def get_upcoming_launch():
    """Fetch and display the next SpaceX launch"""

    url = 'https://api.spacexdata.com/v4/launches/upcoming'

    try:
        # Fetch upcoming launches
        response = requests.get(url)
        response.raise_for_status()
        launches = response.json()

        if not launches:
            print("No upcoming launches found.")
            return

        # Sort launches by date and get the nearest one
        upcoming_launch = sorted(launches, key=lambda x: x.get('date_unix', float('inf')))[0]

        # Get details of the rocket
        rocket_id = upcoming_launch.get('rocket')
        rocket_name = "Unknown"
        if rocket_id:
            rocket_url = f'https://api.spacexdata.com/v4/rockets/{rocket_id}'
            rocket_response = requests.get(rocket_url)
            rocket_response.raise_for_status()
            rocket = rocket_response.json()
            rocket_name = rocket.get('name', 'Unknown')

        # Get details of the launchpad
        launchpad_id = upcoming_launch.get('launchpad')
        launchpad_name = "Unknown"
        launchpad_locality = "Unknown"
        if launchpad_id:
            launchpad_url = f'https://api.spacexdata.com/v4/launchpads/{launchpad_id}'
            launchpad_response = requests.get(launchpad_url)
            launchpad_response.raise_for_status()
            launchpad = launchpad_response.json()
            launchpad_name = launchpad.get('name', 'Unknown')
            launchpad_locality = launchpad.get('locality', 'Unknown')

        # Get launch details
        name = upcoming_launch.get('name', 'Unknown')
        date_local = upcoming_launch.get('date_local', 'Unknown')

        # Display launch details
        print(
            "{} ({}) {} - {} ({})".format(
                name, date_local, rocket_name, launchpad_name, launchpad_locality
            )
        )

    except requests.RequestException as e:
        print(f"An error occurred while making an API request: {e}")
    except Exception as err:
        print(f"A general error occurred: {err}")


if __name__ == '__main__':
    get_upcoming_launch()

