from pydantic import BaseModel


class AttendanceModel(BaseModel):
    course_code: str
    total_hours: int
    exemption_hours: int
    total_absent: int
    total_present: int
    percentage_of_attendance: int
    percentage_with_exemp: int
    percentage_with_exemp_med: int
    attendance_percentage_from: str
    attendance_percentage_to: str
    remark: dict


class TimeTableModel(BaseModel):
    course_code: str
    course_title: str
    programme: str
    sem_no: str


class SemMarkModel(BaseModel):
    latest_sem_no: int
    latest_sem_cgpa: float
