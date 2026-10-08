from logic.Calendar import Calendar
from logic.ConflictException import ConflictsException


class Person:
    """
    A class representing a person with an associated calendar to manage meetings.
    """

    def __init__(self, name: str = ""):
        """
        Constructor for Person class. Initializes the person with a name and an empty calendar.

        :param name: The name of the person.
        """
        self.name = name
        self.calendar = Calendar()

    def get_name(self) -> str:
        """
        Retrieves the name of the person.

        :return: The person's name as a string.
        """
        return self.name

    def add_meeting(self, meeting: 'Meeting') -> None:
        """
        Adds a meeting to the person's calendar.

        :param meeting: The Meeting object to add to the calendar.
        :raises ConflictsException: If there is a scheduling conflict.
        """
        try:
            self.calendar.add_meeting(meeting)
        except ConflictsException as e:
            raise ConflictsException(f"Conflict for attendee {self.name}:\n{e}")

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
        Checks whether the person is busy during a given time frame.

        :param month: The month of the meeting (1-12).
        :param day: The day of the meeting (1-31).
        :param start: The start time of the meeting (0-23).
        :param end: The end time of the meeting (0-23).
        :return: True if the person is occupied during the specified time frame, otherwise False.
        :raises ConflictsException: If the input time values are invalid.
        """
        return self.calendar.is_busy(month, day, start, end)

    def get_meeting(self, month: int, day: int, index: int) -> 'Meeting':
        """
        Retrieves a specific meeting from the person's calendar.

        :param month: The month of the meeting (1-12).
        :param day: The day of the meeting (1-31).
        :param index: The index of the meeting in the list for that day.
        :return: The Meeting object at the specified date and index.
        """
        return self.calendar.get_meeting(month, day, index)

    def remove_meeting(self, month: int, day: int, index: int) -> None:
        """
        Removes a meeting from the person's calendar.

        :param month: The month of the meeting (1-12).
        :param day: The day of the meeting (1-31).
        :param index: The index of the meeting in the list for that day.
        """
        self.calendar.remove_meeting(month, day, index)
