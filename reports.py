from database import connection, cursor


class ReportsBackend:
    def __init__(self):
        self.connection = connection
        self.cursor = cursor

    def student_summary(self):
        self.cursor.execute("""
            SELECT
                COUNT(*) AS total_students,
                SUM(CASE WHEN status='Active' THEN 1 ELSE 0 END) AS active_students,
                SUM(CASE WHEN status='Inactive' THEN 1 ELSE 0 END) AS inactive_students
            FROM students
        """)
        return self.cursor.fetchone()

    def batch_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM batches")
        return self.cursor.fetchone()[0]

    def today_attendance_summary(self, today):
        self.cursor.execute("""
            SELECT
                COUNT(*) AS total_marked,
                SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) AS present,
                SUM(CASE WHEN status='ABSENT' THEN 1 ELSE 0 END) AS absent
            FROM attendance
            WHERE attendance_date=%s
        """, (today,))
        return self.cursor.fetchone()

    def fees_summary(self):
        self.cursor.execute("""
            SELECT
                COALESCE(SUM(total_fee), 0)
            FROM students
            WHERE status='Active'
        """)
        total_fee = self.cursor.fetchone()[0]

        self.cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM payments
        """)
        collected = self.cursor.fetchone()[0]

        pending = total_fee - collected

        return total_fee, collected, pending

    def recent_payments(self, limit=10):
        self.cursor.execute("""
            SELECT
                s.full_name,
                p.amount,
                p.payment_date,
                p.remarks
            FROM payments p
            JOIN students s ON p.student_id = s.student_id
            ORDER BY p.payment_date DESC, p.payment_id DESC
            LIMIT %s
        """, (limit,))
        return self.cursor.fetchall()
    
    def fees_summary(self):
     self.cursor.execute(
        """
        SELECT COALESCE(SUM(total_fee), 0)
        FROM students
        WHERE status='Active'
        """
    )
     total_fee = self.cursor.fetchone()[0]

     self.cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM payments
        """
    )
     collected = self.cursor.fetchone()[0]

     pending = total_fee - collected

     return total_fee, collected, pending
    
    def fee_defaulters(self, limit=10):
     self.cursor.execute(
        """
        SELECT
            s.full_name,
            s.total_fee,
            COALESCE(SUM(p.amount), 0) AS paid,
            s.total_fee - COALESCE(SUM(p.amount), 0) AS pending
        FROM students s
        LEFT JOIN payments p
            ON s.student_id = p.student_id
        WHERE s.status = 'Active'
        GROUP BY s.student_id, s.full_name, s.total_fee
        HAVING pending > 0
        ORDER BY pending DESC
        LIMIT %s
        """,
        (limit,)
    )

     return self.cursor.fetchall()
    
    def monthly_collection(self):
     self.cursor.execute(
        """
        SELECT
            DATE_FORMAT(payment_date, '%Y-%m') AS month,
            SUM(amount) AS total
        FROM payments
        GROUP BY month
        ORDER BY month
        """
    )
     return self.cursor.fetchall()