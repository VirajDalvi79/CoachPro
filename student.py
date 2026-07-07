from database import connection, cursor


class Students:
    def __init__(self):
        self.connection = connection
        self.cursor = cursor

    def create_student(
    self,
    full_name,
    phone,
    father_name,
    mother_name,
    parent_phone,
    batch_id,
    admission_date,
    remarks,
    total_fee,
):

     self.cursor.execute(
        """
        INSERT INTO students
        (
            full_name,
            phone,
            father_name,
            mother_name,
            parent_phone,
            batch_id,
            admission_date,
            remarks,
            total_fee
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """,
        (
            full_name,
            phone,
            father_name,
            mother_name,
            parent_phone,
            batch_id,
            admission_date,
            remarks,
            total_fee,
        ),
    )

     self.connection.commit()

    def display_all_students(self):
        self.cursor.execute(
            """
            SELECT student_id, full_name, phone, batch_id, status
            FROM students
            ORDER BY full_name
            """
        )
        return self.cursor.fetchall()

    def search_student(self, keyword):
        """Same column shape as display_all_students so the UI table
        doesn't need to reconfigure itself between browse/search states."""
        like = f"%{keyword}%"
        self.cursor.execute(
            """
            SELECT student_id, full_name, phone, batch_id, status
            FROM students
            WHERE student_id = %s
               OR full_name LIKE %s
               OR phone LIKE %s
               OR father_name LIKE %s
               OR mother_name LIKE %s
               OR parent_phone LIKE %s
            ORDER BY full_name
            """,
            (keyword, like, like, like, like, like)
        )
        return self.cursor.fetchall()

    def deactivate_student(self, student_id):
        self.cursor.execute(
            "UPDATE students SET status = 'Inactive' WHERE student_id = %s",
            (student_id,)
        )
        self.connection.commit()

    def get_student_details(self, student_id):
        """Full row — used to pre-fill the Edit Student form."""
        self.cursor.execute(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,)
        )
        return self.cursor.fetchone()

    def update_student(
    self,
    full_name,
    phone,
    father_name,
    mother_name,
    parent_phone,
    batch_id,
    admission_date,
    remarks,
    total_fee,
    student_id,
):

     self.cursor.execute(
        """
        UPDATE students

        SET

            full_name=%s,
            phone=%s,
            father_name=%s,
            mother_name=%s,
            parent_phone=%s,
            batch_id=%s,
            admission_date=%s,
            remarks=%s,
            total_fee=%s

        WHERE student_id=%s
        """,
        (
            full_name,
            phone,
            father_name,
            mother_name,
            parent_phone,
            batch_id,
            admission_date,
            remarks,
            total_fee,
            student_id,
        ),
    )
     self.connection.commit()
