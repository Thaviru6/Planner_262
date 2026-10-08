from logic.ConflictException import ConflictsException


class Calendar:
    """
    A calendar class to manage meetings, indexed by month and day.
    """

    def __init__(self):
        """
        Default constructor, builds a calendar and initializes each day to an empty list.
        Order of access is month, day, meetingNumber.
        We want to tie 1 to January, 2 to February, etc.,
        so we will index 1-12 for months, 1-31 for days.
        Times are indexed 0 - 23.
        Need to check bounds when adding a meeting.
        """
        from logic.Meeting import Meeting
        self.occupied = {month: {day: [] for day in range(0, 32)} for month in range(0, 13)}

        # Not every month should have 31 days. Hack-ish method of handling it.
        self.occupied[2][29].append(Meeting(2, 29, description="Day does not exist"))
        self.occupied[2][30].append(Meeting(2, 30, description="Day does not exist"))
        self.occupied[2][31].append(Meeting(2, 31, description="Day does not exist"))
        self.occupied[4][31].append(Meeting(4, 31, description="Day does not exist"))
        self.occupied[6][31].append(Meeting(6, 31, description="Day does not exist"))
        self.occupied[9][31].append(Meeting(9, 31, description="Day does not exist"))
        self.occupied[11][30].append(Meeting(11, 31, description="Day does not exist"))
        self.occupied[11][31].append(Meeting(11, 31, description="Day does not exist"))

    def is_busy(self, month: int, day: int, start: int, end: int) -> bool:
        """
        Check whether a meeting is scheduled during a particular time frame.

        :param month: The month of the meeting (1-12)
        :param day: The day of the meeting (1-31)
        :param start: The start time of the meeting (0-23)
        :param end: The end time of the meeting (0-23)
        :return: True if the time slot is occupied, False otherwise.
        """
        busy = False

        self.check_times(month, day, start, end)

        for to_check in self.occupied[month][day]:
            if start >= to_check.get_start_time() and start <= to_check.get_end_time():
                busy = True
            elif end >= to_check.get_start_time() and end <= to_check.get_end_time():
                busy = True
        return busy

    @staticmethod
    def check_times(m_month: int, m_day: int, m_start: int, m_end: int) -> None:
        """
        Basic error checking on numbers.

        :param m_month: The month of the meeting (1-12)
        :param m_day: The day of the meeting (1-31)
        :param m_start: The start time of the meeting (0-23)
        :param m_end: The end time of the meeting (0-23)
        :raises ConflictsException: If any of the values are invalid.
        """
        if m_day < 1 or m_day > 30:
            raise ConflictsException("Day does not exist.")
        if m_month < 1 or m_month >= 12:
            raise ConflictsException("Month does not exist.")
        if m_start < 0 or m_start >= 23:
            raise ConflictsException("Illegal hour.")
        if m_end < 0 or m_end > 23:
            raise ConflictsException("Illegal hour.")
        if m_start > m_end:
            raise ConflictsException("Meeting starts before it ends.")

    def add_meeting(self, to_add: 'Meeting') -> None:
        """
        Adds a meeting to the calendar.

        :param to_add: A Meeting object to add to the calendar.
        :raises ConflictsException: If an invalid date or time is entered or a scheduling conflict occurs.
        """
        m_month = to_add.get_month()
        m_day = to_add.get_day()
        m_start = to_add.get_start_time()
        m_end = to_add.get_end_time()

        self.check_times(m_month, m_day, m_start, m_end)

        # Check if the date exists in the calendar
        if m_month not in self.occupied:
            self.occupied[m_month] = {}
        if m_day not in self.occupied[m_month]:
            self.occupied[m_month][m_day] = []

        # Check whether a meeting is already scheduled at this time
        that_day = self.occupied[m_month][m_day]
        booked = False
        conflict = None

        for to_check in that_day:
            if to_check.get_description() != "Day does not exist":
                # Does the start time fall between this meeting's start and end times?
                if m_start >= to_check.get_start_time() and m_start <= to_check.get_end_time():
                    booked = True
                    conflict = to_check
                # Does the end time fall between this meeting's start and end times?
                elif m_end >= to_check.get_start_time() and m_end <= to_check.get_end_time():
                    booked = True
                    conflict = to_check

        if booked:
            raise ConflictsException(
                f"Overlap with another item - {conflict.get_description()} "
                f"- scheduled from {conflict.get_start_time()} and {conflict.get_end_time()}"
            )
        else:
            self.occupied[m_month][m_day].append(to_add)

    def clear_schedule(self, month: int, day: int) -> None:
        """
        Clears all meetings for a given day by replacing the existing list with an empty list.

        :param month: The month for which the schedule should be cleared (1-12).
        :param day: The day for which the schedule should be cleared (1-31).
        """
        self.occupied[month][day] = []

    def print_agenda(self, month: int) -> str:
        """
        Prints the agenda for a given month in string format.

        :param month: The month of the meeting (1-12)
        :return: A formatted string with all meetings in the specified month.
        """
        if month not in self.occupied or not any(self.occupied[month].values()):
            return "No Meetings booked for this month.\n\n"

        agenda = f"Agenda for {month}:\n"
        for day, meetings in self.occupied[month].items():
            for meeting in meetings:
                agenda += str(meeting) + "\n"

        return agenda

    def print_agenda(self, month: int, day: int) -> str:
        """
        Prints the agenda for a given day in string format.

        :param month: The month of the meeting (1-12)
        :param day: The day of the meeting (1-31)
        :return: A formatted string with all meetings on the specified date.
        """
        if month not in self.occupied or day not in self.occupied[month] or not self.occupied[month][day]:
            return "No Meetings booked on this date.\n\n"

        agenda = f"Agenda for {month}/{day} are as follows:\n"
        for meeting in self.occupied[month][day]:
            agenda += str(meeting) + "\n"

        return agenda

    def get_meeting(self, month: int, day: int, index: int) -> 'Meeting':
        """
        Retrieves a specific meeting from the calendar at the given date and index.

        :param month: The month of the meeting (1-12).
        :param day: The day of the meeting (1-31).
        :param index: The index of the meeting in the list.
        :return: The meeting object at the specified date and index.
        :raises IndexError: If the index is out of range for the given date.
        """
        return self.occupied[month][day][index]

    def remove_meeting(self, month: int, day: int, index: int) -> None:
        """
        Removes a meeting from the calendar at the specified date and index.

        :param month: The month of the meeting (1-12).
        :param day: The day of the meeting (1-31).
        :param index: The index of the meeting to be removed in the list.
        :raises IndexError: If the index is out of range for the given date.
        """
        del self.occupied[month][day][index]
