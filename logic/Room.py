from logic.Calendar import Calendar
from logic.ConflictException import ConflictsException


class Room:
    """
    A class representing a room with an associated calendar to manage meetings.
    """

    def __init__(self, id: str = ""):
        """
        Constructor for Room class. Initializes the room with an ID and an empty calendar.

        :param id: The unique identifier for the room.
        """
        self.id = id
        self.calendar = Calendar()

    def get_id(self) -> str:
        """
        Retrieves the unique identifier of the room.

        :return: The room's ID as a string.
        """
        return self.id

    def add_meeting(self, meeting: 'Meeting') -> None:
        """
        Adds a meeting to the room's calendar.

        :param meeting: The Meeting object to add to the calendar.
        :raises ConflictsException: If there is a scheduling conflict.
        """
        try:
            self.calendar.add_meeting(meeting)
        except ConflictsException as e:
            raise ConflictsException(f"Conflict for room {self.id}:\n{e}")

    def print_agenda(self, month: int, day: int = None) -> str:
        """
        Prints the agenda for a specified month or a specific day in that month.

        :param month: The month for which to retrieve the agenda (1-12).
        :param day: (Optional) The day for which to retrieve the agenda (1-31).
        :return: A formatted string containing the agenda.
        """
        if day is None:
            return self.calendar.print_agenda(month)
        return self.calendar.print_agenda(month, day)

    def is_busy(self, month: int, day: int, start: int, end: int) -> bool:
        """
        Checks whether the room is busy during a given time frame.

        :param month: The month of the meeting (1-12).
        :param day: The day of the meeting (1-31).
        :param start: The start time of the meeting (0-23).
        :param end: The end time of the meeting (0-23).
        :return: True if the room is occupied during the specified time frame, otherwise False.
        :raises ConflictsException: If the input time values are invalid.
        """
        return self.calendar.is_busy(month, day, start, end)

    def get_meeting(self, month: int, day: int, index: int) -> 'Meeting':
        """
        Retrieves a specific meeting from the room's calendar.

        :param month: The month of the meeting (1-12).
        :param day: The day of the meeting (1-31).
        :param index: The index of the meeting in the list for that day.
        :return: The Meeting object at the specified date and index.
        """
        return self.calendar.get_meeting(month, day, index)

    def remove_meeting(self, month: int, day: int, index: int) -> None:
        """
        Removes a meeting from the room's calendar.

        :param month: The month of the meeting (1-12).
        :param day: The day of the meeting (1-31).
        :param index: The index of the meeting in the list for that day.
        """
        self.calendar.remove_meeting(month, day, index)
