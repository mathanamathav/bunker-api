def map_course_name_with_code(data):
    res = {}
    for course in data:
        res[course.course_code] = course.course_title
    return res
