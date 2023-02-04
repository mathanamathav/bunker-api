class AttendanceUpdateInProcessException(Exception):
    def __init__(self, message="Attendance not yet updated"):
        self.message = message
        super().__init__(self.message)


class InvalidUsernameOrPasswordException(Exception):
    def __init__(self, message="username or password is invalid"):
        self.message = message
        super().__init__(self.message)


class ScrappingError(Exception):
    def __init__(self, message="Status code is not 200"):
        self.message = message
        super().__init__(self.message)


class NoTimeTableDataException(Exception):
    def __init__(self, message="Time table data does not exist"):
        self.message = message
        super().__init__(self.message)


class NoSemResultsAvailable(Exception):
    def __init__(self, message="Semester exam results not yet published"):
        self.message = message
        super().__init__(self.message)
