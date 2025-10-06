from lxml import etree

# Đọc file XML
tree = etree.parse("sv.xml")

# 1. Lấy tất cả sinh viên
students = tree.xpath("/school/student")
print("Tất cả sinh viên:", len(students))

# 2. Tên tất cả sinh viên
names = tree.xpath("/school/student/name/text()")
print("Tên sinh viên:", names)

# 3. ID tất cả sinh viên
ids = tree.xpath("/school/student/id/text()")
print("ID sinh viên:", ids)

# 4. Ngày sinh SV01
dob_sv01 = tree.xpath("/school/student[id='SV01']/date/text()")
print("Ngày sinh SV01:", dob_sv01)

# 5. Các khóa học
courses = tree.xpath("/school/enrollment/course/text()")
print("Các khóa học:", courses)

# 6. Thông tin sinh viên đầu tiên
first_student = tree.xpath("/school/student[1]")[0]
print("Sinh viên đầu tiên:", etree.tostring(first_student, pretty_print=True).decode())

# 7. Mã sinh viên học Vatly203
vatly_ids = tree.xpath("/school/enrollment[course='Vatly203']/studentRef/text()")
print("SV học Vatly203:", vatly_ids)

# 8. Tên SV học Toan101
toan_names = tree.xpath("/school/student[id=/school/enrollment[course='Toan101']/studentRef]/name/text()")
print("SV học Toan101:", toan_names)

# 9. Tên SV học Vatly203
vatly_names = tree.xpath("/school/student[id=/school/enrollment[course='Vatly203']/studentRef]/name/text()")
print("SV học Vatly203:", vatly_names)

# 10. Ngày sinh SV01 (lặp lại)
print("Ngày sinh SV01:", dob_sv01)

# 11. Tên và ngày sinh SV sinh năm 1997
names_1997 = tree.xpath("/school/student[starts-with(date,'1997')]/name/text()")
dates_1997 = tree.xpath("/school/student[starts-with(date,'1997')]/date/text()")
print("SV sinh năm 1997:", list(zip(names_1997, dates_1997)))

# 12. Tên SV sinh trước 1998
names_before_1998 = tree.xpath("/school/student[substring(date,1,4) < '1998']/name/text()")
print("SV sinh trước 1998:", names_before_1998)

# 13. Đếm tổng số sinh viên
count = tree.xpath("count(/school/student)")
print("Tổng số SV:", int(count))

# 14. SV chưa đăng ký môn nào (sau khi thêm SV04, SV05 vào XML)
unregistered = tree.xpath("/school/student[not(id=/school/enrollment/studentRef)]/name/text()")
print("SV chưa đăng ký môn:", unregistered)

# 15. <date> sau <name> của SV01
date_after_name = tree.xpath("/school/student[id='SV01']/name/following-sibling::date[1]/text()")
print("Date sau name SV01:", date_after_name)

# 16. <id> trước <name> của SV02
id_before_name = tree.xpath("/school/student[id='SV02']/name/preceding-sibling::id[1]/text()")
print("ID trước name SV02:", id_before_name)

# 17. <course> của SV03
course_sv03 = tree.xpath("/school/enrollment[studentRef='SV03']/course/text()")
print("Course của SV03:", course_sv03)

# 18. SV có họ Trần
tran_students = tree.xpath("/school/student[starts-with(name,'Trần')]/name/text()")
print("SV họ Trần:", tran_students)

# 19. Năm sinh SV01
year_sv01 = tree.xpath("substring(/school/student[id='SV01']/date/text(),1,4)")
print("Năm sinh SV01:", year_sv01)