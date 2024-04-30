import streamlit as st
import requests
import asyncio
import websockets
from concurrent.futures import ThreadPoolExecutor


BASE_URL = "http://localhost:8000"
executor = ThreadPoolExecutor()


def register_player(player_name):
    """Register player to the gaming platform.

    Args:
        player_name (str): player name (always unique)
    """
    uri = f"{BASE_URL}/players/{player_name}"
    response = requests.put(uri)
    return response.json()


def get_player(player_name):
    """Send a request to the server to register a player.

    Args:
        player_name (str): player name (always unique)
    """
    uri = f"{BASE_URL}/players/{player_name}"
    response = requests.get(uri)
    if response.status_code == 200:
        return response.json()
    else:
        return None


async def connect_to_server(player_name):
    async with websockets.connect(
        f"ws://localhost:8000/players/{player_name}/ws"
    ) as websocket:
        while True:
            message = await websocket.recv()
            st.write(f"Received message from server: {message}")


def main():
    st.title("Multiplayer Game Client")
    player_name = st.text_input("Enter your player name:")
    if st.button("Register"):
        if player_name:
            st.write(register_player(player_name))
        else:
            st.write("Please enter a player name.")
    if st.button("Lookup"):
        if player_name:
            st.write(get_player(player_name))
        else:
            st.write("Please enter a player name.")
    if st.button("Play"):
        if player_name:
            asyncio.run(connect_to_server(player_name))
        else:
            st.write("Please enter a player name.")


if __name__ == "__main__":
    main()


# st.title("Game Matchmaking System")

# # Player registration
# with st.form("Player Registration"):
#     player_name = st.text_input("Enter your player name to register:")
#     submit_button = st.form_submit_button("Register")

# if submit_button:
#     result = register_player(player_name)
#     if "message" in result:
#         st.success(result["message"])
#     else:
#         st.error("Failed to register player")

# # Player actions
# # st.subheader("Player Actions")
# # action_player_name = st.text_input("Enter your player name to play or check status:")
# # if st.button("Play Game"):
# #     play_response = play_game(action_player_name)
# #     st.write(play_response)

# if st.button("Connect to Game"):
#     player_name = "example_player_name"
#     uri = f"{BASE_URL}/ws/play/{player_name}"
#     start_websocket_client(uri)
#     st.write("starting websoclket")

# if st.button("Check Status"):
#     player_info = get_player(player_name)
#     if player_info:
#         st.json(player_info)
#     else:
#         st.error("Player not found or there was an error fetching the details.")
