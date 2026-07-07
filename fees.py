from database import connection, cursor


class Fees:
    def __init__(self):
        self.connection = connection
        self.cursor = cursor

    def generate_monthly_fee(self, batch_id, amount):
        self.cursor.execute(
            """
            INSERT INTO fee_structure(batch_id, amount)
            VALUES(%s, %s)
            """,
            (batch_id, amount)
        )
        self.connection.commit()

    def update_fee(self, fee_id, amount):
        self.cursor.execute(
            """
            UPDATE fee_structure
            SET amount=%s
            WHERE fee_id=%s
            """,
            (amount, fee_id)
        )
        self.connection.commit()

    def delete_fee(self, fee_id):
        self.cursor.execute(
            """
            DELETE FROM fee_structure
            WHERE fee_id=%s
            """,
            (fee_id,)
        )
        self.connection.commit()

    def display_fee_structure(self):
        self.cursor.execute(
            """
            SELECT fee_id, batch_id, amount
            FROM fee_structure
            ORDER BY fee_id DESC
            """
        )
        return self.cursor.fetchall()

    def make_payment(self, fee_id, student_id, amount, payment_date):
        self.cursor.execute(
            """
            INSERT INTO payments(fee_id, student_id, amount, payment_date)
            VALUES(%s,%s,%s,%s)
            """,
            (fee_id, student_id, amount, payment_date)
        )
        self.connection.commit()

    def payment_history(self, student_id):
        self.cursor.execute(
            """
            SELECT payment_id, fee_id, student_id, amount, payment_date
            FROM payments
            WHERE student_id=%s
            ORDER BY payment_date DESC
            """,
            (student_id,)
        )
        return self.cursor.fetchall()

    def total_paid(self, student_id):
        self.cursor.execute(
            """
            SELECT COALESCE(SUM(amount),0)
            FROM payments
            WHERE student_id=%s
            """,
            (student_id,)
        )
        return self.cursor.fetchone()[0]

    def pending_fee(self, student_id):
        """
        Sums the pending balance across every fee_structure row that
        applies to the student's batch (a batch can have several rows,
        e.g. one per month). The previous version grouped by amount and
        used fetchone(), which silently discarded all but one row/month
        whenever a student had more than one fee entry.
        """
        self.cursor.execute(
            """
            SELECT COALESCE(SUM(fee_amount - paid_amount), 0)
            FROM (
                SELECT
                    fee_structure.fee_id,
                    fee_structure.amount AS fee_amount,
                    COALESCE(SUM(payments.amount), 0) AS paid_amount
                FROM fee_structure
                JOIN students
                    ON students.batch_id = fee_structure.batch_id
                LEFT JOIN payments
                    ON payments.student_id = students.student_id
                    AND payments.fee_id = fee_structure.fee_id
                WHERE students.student_id = %s
                GROUP BY fee_structure.fee_id, fee_structure.amount
            ) AS per_fee
            """,
            (student_id,)
        )
        return self.cursor.fetchone()[0]

    def student_fee_status(self, student_id):
        paid = self.total_paid(student_id)
        pending = self.pending_fee(student_id)

        if pending <= 0:
            return "PAID"
        elif paid == 0:
            return "UNPAID"
        return "PARTIAL"

    def delete_payment(self, payment_id):
        self.cursor.execute(
            """
            DELETE FROM payments
            WHERE payment_id=%s
            """,
            (payment_id,)
        )
        self.connection.commit()
