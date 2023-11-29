import logging
from webexteamssdk import WebexTeamsAPI

class SendToWebexTeams:
    """
    Class for sending messages to a Webex Teams room.
    """

    def __init__(self, webex_token, room_id, sendwebex):
        """
        Initialize the SendToWebexTeams object.

        Args:
            webex_token (str): Webex Teams API access token.
            room_id (str): Room ID where messages will be sent.
        """
        self.webex_api = WebexTeamsAPI(access_token=webex_token)
        self.room_id = room_id
        self.sendwebex = sendwebex

    def send_to_webex_room(self, message, sendwebex):
        """
        Send a message to the specified Webex Teams room.

        Args:
            message (str): The message to be sent.

        Raises:
            Exception: If there is an error while sending the message.
        """
        if sendwebex == 'yes':
            try:
                self.webex_api.messages.create(roomId=self.room_id, text=message)
                logging.info(f"Message sent to Webex Teams room {self.room_id}")
            except Exception as e:
                logging.error(f"Error sending message to Webex Teams room {self.room_id}: {e}")
                raise
        else:
            logging.info("sendwebex is 'no', not sending to webex.")

