from database import connection, cursor


class Attendance:
    def __init__(self):
        self.connection = connection
        self.cursor = cursor

    def mark_attendance(self, student_id, attendance_date, status):

     self.cursor.execute(
        """
        SELECT attendance_id
        FROM attendance
        WHERE student_id=%s
        AND attendance_date=%s
        """,
        (student_id, attendance_date)
    )

     existing = self.cursor.fetchone()

     if existing:

        self.cursor.execute(
            """
            UPDATE attendance
            SET status=%s
            WHERE student_id=%s
            AND attendance_date=%s
            """,
            (
                status,
                student_id,
                attendance_date
            )
        )

     else:
 
        self.cursor.execute(
            """
            INSERT INTO attendance
            (
                student_id,
                attendance_date,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                student_id,
                attendance_date,
                status
            )
        )

        self.connection.commit()

    def get_attendance_by_date(self, attendance_date):

     self.cursor.execute(
        """
        SELECT
            student_id,
            attendance_date,
            status
        FROM attendance
        WHERE attendance_date=%s
        """,
        (attendance_date,)
    )

     return self.cursor.fetchall()

    
    def get_attendance(self, student_id, attendance_date):

     self.cursor.execute(
        """
        SELECT status
        FROM attendance
        WHERE student_id=%s
        AND attendance_date=%s
        """,
        (
            student_id,
            attendance_date
        )
    )

     return self.cursor.fetchone()

    def get_student_attendance(self, student_id):
        self.cursor.execute(
            """
            SELECT student_id, attendance_date, status
            FROM attendance
            WHERE student_id = %s
            ORDER BY attendance_date DESC
            """,
            (student_id,)
        )
        return self.cursor.fetchall()

    def attendance_percentage(self, student_id):
        self.cursor.execute(
            """
            SELECT
                COUNT(*) AS total_days,
                SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS present_days
            FROM attendance
            WHERE student_id = %s
            """,
            (student_id,)
        )
        result = self.cursor.fetchone()
        total_days, present_days = result[0], result[1]

        if total_days == 0:
            return 0

        return (present_days / total_days) * 100

    def edit_attendance(self, student_id, attendance_date, status):
        self.cursor.execute(
            """
            UPDATE attendance
            SET status = %s
            WHERE student_id = %s AND attendance_date = %s
            """,
            (status, student_id, attendance_date)
        )
        self.connection.commit()

    def delete_attendance(self, student_id, attendance_date):
        self.cursor.execute(
            """
            DELETE FROM attendance
            WHERE student_id = %s AND attendance_date = %s
            """,
            (student_id, attendance_date)
        )
        self.connection.commit()
    
    def get_history_with_names(self, attendance_date):

     self.cursor.execute(
        """
        SELECT

            a.attendance_id,
            s.full_name,
            a.attendance_date,
            a.status

        FROM attendance a

        JOIN students s

            ON a.student_id=s.student_id

        WHERE a.attendance_date=%s

        ORDER BY s.full_name
        """,
        (attendance_date,)
    )

     return self.cursor.fetchall()
    
    # -----------------------------------
# TOGGLE STATUS
# -----------------------------------

    def toggle_status(
     self,
     attendance_id,
    new_status,
): 

     self.cursor.execute(
        """
        UPDATE attendance
        SET status=%s
        WHERE attendance_id=%s
        """,
        (
            new_status,
            attendance_id,
        ),
    )

     self.connection.commit()


    # -----------------------------------
# DELETE RECORD
# -----------------------------------

    def delete_by_id(
    self,
    attendance_id,
):

     self.cursor.execute(
        """
        DELETE FROM attendance
        WHERE attendance_id=%s
        """,
        (attendance_id,),
    )

     self.connection.commit() 


    def attendance_summary(self, attendance_date):

     self.cursor.execute(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) AS present,
            SUM(CASE WHEN status='Absent' THEN 1 ELSE 0 END) AS absent
        FROM attendance
        WHERE attendance_date=%s
        """,
        (attendance_date,)
    )

     return self.cursor.fetchone()
    
    def get_all_history_with_names(self):
     self.cursor.execute(
        """
        SELECT
            a.attendance_id,
            s.full_name,
            a.attendance_date,
            a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        ORDER BY a.attendance_date DESC, s.full_name
        """
    )
     return self.cursor.fetchall()