from database import connection, cursor


class Marks:
    def __init__(self):
        self.connection = connection
        self.cursor = cursor



    def get_all_exams(self):
        self.cursor.execute(
            """
            SELECT exam_id, exam_name, exam_date, total_marks, batch_id
            FROM exams
            ORDER BY exam_date DESC
            """
        )
        return self.cursor.fetchall()

    def get_subjects_by_batch(self, batch_id):
        self.cursor.execute(
            """
            SELECT subject_id, subject_name
            FROM subjects
            WHERE batch_id=%s
            ORDER BY subject_name
            """,
            (batch_id,)
        )
        return self.cursor.fetchall()

    def get_students_by_batch(self, batch_id):
        self.cursor.execute(
            """
            SELECT student_id, full_name
            FROM students
            WHERE batch_id=%s
            AND status='Active'
            ORDER BY full_name
            """,
            (batch_id,)
        )
        return self.cursor.fetchall()

    def get_existing_mark(self, student_id, exam_id, subject_id):
        self.cursor.execute(
            """
            SELECT marks_obtained
            FROM marks
            WHERE student_id=%s
            AND exam_id=%s
            AND subject_id=%s
            """,
            (student_id, exam_id, subject_id)
        )
        return self.cursor.fetchone()

    def save_or_update_marks(self, student_id, exam_id, subject_id, marks_obtained):
        existing = self.get_existing_mark(student_id, exam_id, subject_id)

        if existing:
            self.update_marks(student_id, exam_id, subject_id, marks_obtained)
        else:
            self.add_marks(student_id, exam_id, subject_id, marks_obtained)    

    def add_marks(self, student_id, exam_id, subject_id, marks_obtained):
        self.cursor.execute(
            """
            INSERT INTO marks(student_id, exam_id, subject_id, marks_obtained)
            VALUES(%s,%s,%s,%s)
            """,
            (student_id, exam_id, subject_id, marks_obtained)
        )
        self.connection.commit()

    def update_marks(self, student_id, exam_id, subject_id, marks_obtained):
        self.cursor.execute(
            """
            UPDATE marks
            SET marks_obtained=%s
            WHERE student_id=%s
            AND exam_id=%s
            AND subject_id=%s
            """,
            (marks_obtained, student_id, exam_id, subject_id)
        )
        self.connection.commit()

    def delete_marks(self, student_id, exam_id, subject_id):
        self.cursor.execute(
            """
            DELETE FROM marks
            WHERE student_id=%s
            AND exam_id=%s
            AND subject_id=%s
            """,
            (student_id, exam_id, subject_id)
        )
        self.connection.commit()

    def get_student_marks(self, student_id):
        self.cursor.execute(
            """
            SELECT student_id, exam_id, subject_id, marks_obtained
            FROM marks
            WHERE student_id=%s
            """,
            (student_id,)
        )
        return self.cursor.fetchall()

    def get_exam_results(self, exam_id):
        self.cursor.execute(
            """
            SELECT student_id, exam_id, subject_id, marks_obtained
            FROM marks
            WHERE exam_id=%s
            ORDER BY marks_obtained DESC
            """,
            (exam_id,)
        )
        return self.cursor.fetchall()

    def calculate_total_marks(self, student_id, exam_id):
        self.cursor.execute(
            """
            SELECT SUM(marks_obtained)
            FROM marks
            WHERE student_id=%s
            AND exam_id=%s
            """,
            (student_id, exam_id)
        )
        return self.cursor.fetchone()[0]

    def subject_wise_average(self, subject_id):
        self.cursor.execute(
            """
            SELECT AVG(marks_obtained)
            FROM marks
            WHERE subject_id=%s
            """,
            (subject_id,)
        )
        return self.cursor.fetchone()[0]

    def calculate_percentage(self, student_id, exam_id):
        self.cursor.execute(
            """
            SELECT
            SUM(marks_obtained),
            exams.total_marks

            FROM marks

            JOIN exams
            ON marks.exam_id = exams.exam_id

            WHERE marks.student_id=%s
            AND marks.exam_id=%s

            GROUP BY exams.total_marks
            """,
            (student_id, exam_id)
        )

        result = self.cursor.fetchone()

        if result:
            obtained = result[0]
            total = result[1]
            return (obtained / total) * 100

        return 0

    def topper_of_exam(self, exam_id):
        self.cursor.execute(
            """
            SELECT student_id,
            SUM(marks_obtained) AS total

            FROM marks

            WHERE exam_id=%s

            GROUP BY student_id

            ORDER BY total DESC

            LIMIT 1
            """,
            (exam_id,)
        )

        return self.cursor.fetchone()

    def calculate_grade(self, percentage):
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B"
        elif percentage >= 60:
            return "C"
        elif percentage >= 40:
            return "D"
        return "Fail"
    

    def get_all_exams(self):
     self.cursor.execute(
        """
        SELECT exam_id, exam_name, exam_date, total_marks, batch_id
        FROM exams
        ORDER BY exam_date DESC
        """
    )
     return self.cursor.fetchall()

    
    def get_subjects(self, batch_id):

     self.cursor.execute("""
        SELECT
            subject_id,
            subject_name
        FROM subjects
        WHERE batch_id=%s
        ORDER BY subject_name
    """, (batch_id,))

     return self.cursor.fetchall()
    
    def get_students(self, batch_id):

     self.cursor.execute("""
        SELECT
            student_id,
            full_name
        FROM students
        WHERE batch_id=%s
        AND status='Active'
        ORDER BY full_name
    """, (batch_id,))

     return self.cursor.fetchall()
    

    def create_exam(self, exam_name, exam_date, total_marks, batch_id):
     self.cursor.execute(
        """
        INSERT INTO exams (exam_name, exam_date, total_marks, batch_id)
        VALUES (%s, %s, %s, %s)
        """,
        (exam_name, exam_date, total_marks, batch_id)
    )
     self.connection.commit()


    def create_subject(self, subject_name, batch_id):
     self.cursor.execute(
        """
        INSERT INTO subjects (subject_name, batch_id)
        VALUES (%s, %s)
        """,
        (subject_name, batch_id)
    )
     self.connection.commit()

    def get_exam_results_with_names(self, exam_id):
     self.cursor.execute(
        """
        SELECT
            s.full_name,
            sub.subject_name,
            m.marks_obtained
        FROM marks m
        JOIN students s ON m.student_id = s.student_id
        JOIN subjects sub ON m.subject_id = sub.subject_id
        WHERE m.exam_id = %s
        ORDER BY s.full_name, sub.subject_name
        """,
        (exam_id,)
    )
     return self.cursor.fetchall() 
    
    def create_exam(self, exam_name, exam_date, total_marks, batch_id):
     self.cursor.execute(
        """
        INSERT INTO exams (exam_name, exam_date, total_marks, batch_id)
        VALUES (%s, %s, %s, %s)
        """,
        (exam_name, exam_date, total_marks, batch_id)
    )
     self.connection.commit()


    def update_exam(self, exam_id, exam_name, exam_date, total_marks, batch_id):
     self.cursor.execute(
        """
        UPDATE exams
        SET exam_name=%s,
            exam_date=%s,
            total_marks=%s,
            batch_id=%s
        WHERE exam_id=%s
        """,
        (exam_name, exam_date, total_marks, batch_id, exam_id)
    )
     self.connection.commit()


    def delete_exam(self, exam_id):
     self.cursor.execute(
        """
        DELETE FROM exams
        WHERE exam_id=%s
        """,
        (exam_id,)
    )
     self.connection.commit()


    def get_exam_details(self, exam_id):
      self.cursor.execute(
        """
        SELECT exam_id, exam_name, exam_date, total_marks, batch_id
        FROM exams
        WHERE exam_id=%s
        """,
        (exam_id,)
    )
      return self.cursor.fetchone()


    def search_exams(self, keyword):
     like = f"%{keyword}%"

     self.cursor.execute(
        """
        SELECT exam_id, exam_name, exam_date, total_marks, batch_id
        FROM exams
        WHERE exam_name LIKE %s
        ORDER BY exam_date DESC
        """,
        (like,)
    )

     return self.cursor.fetchall()
    
    def get_all_subjects(self):
     self.cursor.execute(
        """
        SELECT subject_id, subject_name, batch_id
        FROM subjects
        ORDER BY subject_name
        """
    )
     return self.cursor.fetchall()


    def update_subject(self, subject_id, subject_name, batch_id):
     self.cursor.execute(
        """
        UPDATE subjects
        SET subject_name=%s,
            batch_id=%s
        WHERE subject_id=%s
        """,
        (subject_name, batch_id, subject_id)
    )
     self.connection.commit()


    def delete_subject(self, subject_id):
     self.cursor.execute(
        """
        DELETE FROM subjects
        WHERE subject_id=%s
        """,
        (subject_id,)
    )
     self.connection.commit()


    def get_subject_details(self, subject_id):
     self.cursor.execute(
        """
        SELECT subject_id, subject_name, batch_id
        FROM subjects
        WHERE subject_id=%s
        """,
        (subject_id,)
    )
     return self.cursor.fetchone()


    def search_subjects(self, keyword):
     like = f"%{keyword}%"

     self.cursor.execute(
        """
        SELECT subject_id, subject_name, batch_id
        FROM subjects
        WHERE subject_name LIKE %s
        ORDER BY subject_name
        """,
        (like,)
    )
     return self.cursor.fetchall()