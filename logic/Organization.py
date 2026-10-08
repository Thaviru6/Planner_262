from logic.Person import Person
from logic.Room import Room


class Organization:
    """
    This class initializes and stores a list of employees and rooms available for meetings.
    It helps to offload initialization from the main interface.
    """

    def __init__(self):
        """
        Default constructor - initializes a predefined set of employees and rooms.
        """
        self.employees = [
            Person("Justin Gardener"),
            Person("Ashley Matthews"),
            Person("Mary Jane Cook"),
            Person("Rose Austin"),
            Person("Mike Smith"),
            Person("Helen West"),
            Person("Steven Lewis"),
            Person("Edith Cowan"),
            Person("Mark Colin"),
            Person("Jacquie Martin"),
            Person("Jaci Johnston"),
            Person("Travis Colin"),
            Person("Ashley Martin")
        ]

        self.rooms = [
            Room("JO18.330"),
            Room("JO7.221"),
            Room("JO15.236"),
            Room("JO1.230"),
            Room("JO34.536"),
            Room("JO19.230"),
            Room("ML5.123"),
            Room("ML18.330"),
            Room("ML21.520"),
            Room("ML13.213"),
            Room("ML21.310"),
            Room("ML13.218")
        ]

    def get_employees(self) -> list:
        """
        Retrieves the list of employees.

        :return: A list of Person objects.
        """
        return self.employees

    def get_rooms(self) -> list:
        """
        Retrieves the list of rooms.

        :return: A list of Room objects.
        """
        return self.rooms

    def get_room(self, id: str) -> 'Room':
        """
        Searches for and retrieves a room by its ID.

        :param id: The ID of the room to retrieve.
        :return: The requested Room object.
        :raises Exception: If the room does not exist.
        """
        for room in self.rooms:
            if room.get_id() == id:
                return room
        raise Exception("Requested room does not exist")

    def get_employee(self, name: str) -> 'Person':
        """
        Searches for and retrieves an employee by their name.

        :param name: The name of the person to retrieve.
        :return: The requested Person object.
        :raises Exception: If the person does not exist.
        """
        for employee in self.employees:
            if employee.get_name() == name:
                return employee
        raise Exception("Requested employee does not exist")
