from logic.Room import Room
from logic.Person import Person


class Meeting:
    """
    A class representing a meeting with details such as date, time, attendees, room, and description.
    """

    def __init__(self, month: int, day: int, start: int = 0, end: int = 23, attendees: list = None, room: 'Room' = None,
                 description: str = ""):
        """
        Constructor for the Meeting class.

        :param month: The month of the meeting (1-12).
        :param day: The day of the meeting (1-31).
        :param start: The start time of the meeting (0-23). Defaults to 0.
        :param end: The end time of the meeting (0-23). Defaults to 23.
        :param attendees: A list of Person objects attending the meeting. Defaults to an empty list.
        :param room: The Room object where the meeting takes place. Defaults to None.
        :param description: A description of the meeting. Defaults to an empty string.
        """
        self.month = month
        self.day = day
        self.start = start
        self.end = end
        self.attendees = attendees if attendees is not None else []
        self.room = room
        self.description = description

    def add_attendee(self, attendee: 'Person') -> None:
        """
        Adds an attendee to the meeting.

        :param attendee: The Person object to add to the meeting.
        """
        self.attendees.append(attendee)

    def remove_attendee(self, attendee: 'Person') -> None:
        """
        Removes an attendee from the meeting.

        :param attendee: The Person object to remove from the meeting.
        """
        self.attendees.remove(attendee)

    def __str__(self) -> str:
        """
        Returns information about the meeting as a formatted string.

        :return: A string containing the meeting details.
        """
        info = f"Month: {self.month}, Day: {self.day}, Time slot: {self.start} - {self.end}, Room No: {self.room.get_id() if self.room else 'N/A'}: {self.description}\nAttending: "

        if self.attendees:
            info += ", ".join(attendee.get_name() for attendee in self.attendees)
        else:
            info += "No attendees"

        return info

    def get_month(self) -> int:
        """ Retrieves the month of the meeting. """
        return self.month

    def set_month(self, month: int) -> None:
        """ Sets the month of the meeting. """
        self.month = month

    def get_day(self) -> int:
        """ Retrieves the day of the meeting. """
        return self.day

    def set_day(self, day: int) -> None:
        """ Sets the day of the meeting. """
        self.day = day

    def get_start_time(self) -> int:
        """ Retrieves the start time of the meeting. """
        return self.start

    def set_start_time(self, start: int) -> None:
        """ Sets the start time of the meeting. """
        self.start = start

    def get_end_time(self) -> int:
        """ Retrieves the end time of the meeting. """
        return self.end

    def set_end_time(self, end: int) -> None:
        """ Sets the end time of the meeting. """
        self.end = end

    def get_attendees(self) -> list:
        """ Retrieves the list of attendees. """
        return self.attendees

    def get_room(self) -> 'Room':
        """ Retrieves the room where the meeting takes place. """
        return self.room

    def set_room(self, room: 'Room') -> None:
        """ Sets the room for the meeting. """
        self.room = room

    def get_description(self) -> str:
        """ Retrieves the meeting description. """
        return self.description

    def set_description(self, description: str) -> None:
        """ Sets the meeting description. """
        self.description = description
