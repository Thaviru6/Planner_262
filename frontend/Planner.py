from logic.ConflictException import ConflictsException
from logic.Meeting import Meeting
from logic.Organization import Organization


class Planner:
    """
    A class representing a meeting scheduling interface.
    It allows users to schedule meetings, book vacations, check availability, and view agendas.
    """

    def __init__(self):
        """
        Constructor that sets up the organization data structure.
        """
        self.org = Organization()

    @staticmethod
    def main():
        """
        Driver for the calendar system. Initializes the menu.
        """
        menu = Planner()
        menu.main_menu()

    def main_menu(self):
        """
        Displays the main menu and handles user input for menu options.
        """
        print("Welcome to the Meeting Scheduling Interface.")
        user_input = 999
        while user_input != 0:
            print("\n1. Check agenda for a person")
            print("2. Check agenda for a room")
            print("3. Check person availability")
            print("4. Check room availability")
            print("5. Book vacation dates")
            print("6. Schedule a meeting")
            print("0. Exit\n")

            try:
                user_input = int(self.input_output("Please enter a number corresponding to an option: "))
                if user_input == 1:
                    self.check_agenda_person()
                elif user_input == 2:
                    self.check_agenda_room()
                elif user_input == 3:
                    self.check_employee_availability()
                elif user_input == 4:
                    self.check_room_availability()
                elif user_input == 5:
                    self.sched_vac()
                elif user_input == 6:
                    self.sched_meet()

                elif user_input == 0:
                    print("Exiting")
                    exit()
                else:
                    print("Please enter a number from 0 - 6")
            except ValueError:
                print("Please enter a valid number from 0 - 6")

    def input_output(self, message: str) -> str:
        """
        Displays a prompt to the user and returns the entered string.

        :param message: A string message to display.
        :return: The user input as a string.
        """
        return input(message + "\n")

    def sched_vac(self):
        """
        Allows the user to schedule vacation time for an employee.
        """
        successful = True
        name = self.input_output("Enter the name of the employee: ")
        try:
            employee = self.org.get_employee(name)
        except Exception as e:
            print(e)
            return

        start_month = int(self.input_output("Enter the start month (1-12): "))
        start_day = int(self.input_output("Enter the start day (1-31): "))
        end_month = int(self.input_output("Enter the end month (1-12): "))
        end_day = int(self.input_output("Enter the end day (1-31): "))

        for month in range(start_month, end_month + 1):
            for day in range(start_day if month == start_month else 1, (end_day + 1) if month == end_month else 31):
                try:
                    employee.add_meeting(Meeting(month, day, 0, 23, [employee], None, "Vacation"))
                except ConflictsException as e:
                    successful = False
                    print(e)
                    return

        if successful:
            print("Vacation is now booked!")

    def sched_meet(self):
        """
        Allows the user to schedule a meeting by entering relevant details.
        """
        successful = True
        month = int(self.input_output("Enter the month of the meeting (1-12): "))
        day = int(self.input_output("Enter the day of the meeting (1-31): "))
        start_time = int(self.input_output("Enter the starting hour of the meeting (0-23): "))
        end_time = int(self.input_output("Enter the ending hour of the meeting (0-23): "))

        print("The rooms open at that time are:")
        for room in self.org.get_rooms():
            try:
                if not room.is_busy(month, day, start_time, end_time):
                    print(room.get_id())
            except ConflictsException as e:
                print(e)
                return

        selected_room = None
        while not selected_room:
            room_id = self.input_output("Enter the desired room ID, or type 'cancel' to cancel: ")
            if room_id.lower() == "cancel":
                return
            try:
                selected_room = self.org.get_room(room_id)
            except Exception as e:
                print(e)

        print("The people available to attend at that time are:")
        for person in self.org.get_employees():
            try:
                if not person.is_busy(month, day, start_time, end_time):
                    print(person.get_name())
            except ConflictsException as e:
                print(e)
                return

        attendees = []
        while True:
            name = self.input_output("Enter a person's name, or type 'done' when finished: ")
            if name.lower() == "done":
                break
            try:
                attendees.append(self.org.get_employee(name))
            except Exception as e:
                print(e)

        description = self.input_output("Enter a description for the meeting: ")
        meeting = Meeting(month, day, start_time, end_time, attendees, selected_room, description)
        try:
            selected_room.add_meeting(meeting)
            for attendee in attendees:
                attendee.add_meeting(meeting)
        except ConflictsException as e:
            successful = False
            print(e)

        if successful:
            print("Meeting is now booked!")

    def check_room_availability(self):
        """
        Allows the user to check the availability of a room at a given time.
        """
        month = int(self.input_output("Enter the month (1-12): "))
        day = int(self.input_output("Enter the day (1-31): "))
        start_time = int(self.input_output("Enter the starting hour (0-23): "))
        end_time = int(self.input_output("Enter the ending hour (0-23): "))

        print("The rooms available at the specified time are:")
        for room in self.org.get_rooms():
            try:
                if not room.is_busy(month, day, start_time, end_time):
                    print(room.get_id())
            except ConflictsException as e:
                print(e)

    def check_employee_availability(self):
        """
        Allows the user to check the availability of an employee at a given time.
        """
        month = int(self.input_output("Enter the month (1-12): "))
        day = int(self.input_output("Enter the day (1-31): "))
        start_time = int(self.input_output("Enter the starting hour (0-23): "))
        end_time = int(self.input_output("Enter the ending hour (0-23): "))

        print("The people available at that time are:")
        for person in self.org.get_employees():
            try:
                if not person.is_busy(month, day, start_time, end_time):
                    print(person.get_name())
            except ConflictsException as e:
                print(e)

    def check_agenda_room(self):
        """
        Allows the user to check the agenda of a specific room.
        """
        room_id = self.input_output("Enter the Room ID: ")
        try:
            room = self.org.get_room(room_id)
        except Exception as e:
            print(e)
            return

        month = int(self.input_output("Enter the month (1-12): "))
        day = self.input_output("Enter the day (1-31), or 'all' for the entire month: ")

        if day.lower() == "all":
            print(room.print_agenda(month))
        else:
            print(room.print_agenda(month, int(day)))

    def check_agenda_person(self):
        """
        Allows the user to check the agenda of a specific person.
        """
        name = self.input_output("Enter the person's name: ")
        try:
            person = self.org.get_employee(name)
        except Exception as e:
            print(e)
            return

        month = int(self.input_output("Enter the month (1-12): "))
        day = self.input_output("Enter the day (1-31), or 'all' for the entire month: ")

        if day.lower() == "all":
            print(person.print_agenda(month))
        else:
            print(person.print_agenda(month, int(day)))


if __name__ == "__main__":
    Planner.main()
