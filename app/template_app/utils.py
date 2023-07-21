def map_course_name_with_code(data):
    res = {}
    for course in data:
        res[course.course_code] = course.course_title
    return res


def get_last_updated_date(data):
    return data[0].attendance_percentage_to
