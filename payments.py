from database import connection, cursor


class Payments:

    def __init__(self):
        self.connection = connection
        self.cursor = cursor

    # ------------------------------------
    # RECORD PAYMENT
    # ------------------------------------

    def record_payment(
        self,
        student_id,
        amount,
        payment_date,
        remarks,
    ):

        self.cursor.execute(
            """
            INSERT INTO payments
            (
                student_id,
                amount,
                payment_date,
                remarks
            )
            VALUES
            (
                %s,%s,%s,%s
            )
            """,
            (
                student_id,
                amount,
                payment_date,
                remarks,
            ),
        )

        self.connection.commit()

    # ------------------------------------
    # PAYMENT HISTORY
    # ------------------------------------

    def payment_history(
        self,
        student_id,
    ):

        self.cursor.execute(
            """
            SELECT

                payment_id,
                amount,
                payment_date,
                remarks

            FROM payments

            WHERE student_id=%s

            ORDER BY payment_date DESC
            """,
            (student_id,),
        )

        return self.cursor.fetchall()

    # ------------------------------------
    # TOTAL PAID
    # ------------------------------------

    def total_paid(
        self,
        student_id,
    ):

        self.cursor.execute(
            """
            SELECT
                IFNULL(
                    SUM(amount),
                    0
                )

            FROM payments

            WHERE student_id=%s
            """,
            (student_id,),
        )

        return self.cursor.fetchone()[0]

    # ------------------------------------
    # DELETE PAYMENT
    # ------------------------------------

    def delete_payment(
        self,
        payment_id,
    ):

        self.cursor.execute(
            """
            DELETE FROM payments

            WHERE payment_id=%s
            """,
            (payment_id,),
        )

        self.connection.commit()

    # ------------------------------------
    # EDIT PAYMENT
    # ------------------------------------

    def update_payment(
        self,
        payment_id,
        amount,
        payment_date,
        remarks,
    ):

        self.cursor.execute(
            """
            UPDATE payments

            SET

                amount=%s,
                payment_date=%s,
                remarks=%s

            WHERE payment_id=%s
            """,
            (
                amount,
                payment_date,
                remarks,
                payment_id,
            ),
        )

        self.connection.commit()

    def delete_payment(self, payment_id):

     self.cursor.execute(
        """
        DELETE FROM payments
        WHERE payment_id = %s
        """,
        (payment_id,)
    )

     self.connection.commit()    

     