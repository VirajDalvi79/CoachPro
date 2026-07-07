from database import connection, cursor


class Batch:
    def __init__(self):
        self.connection = connection
        self.cursor = cursor

    # -----------------------------
    # CREATE
    # -----------------------------
    def create_batch(self, batch_name, start_time, end_time, classroom):
        self.cursor.execute(
            """
            INSERT INTO batches
            (batch_name, start_time, end_time, classroom)
            VALUES (%s, %s, %s, %s)
            """,
            (batch_name, start_time, end_time, classroom)
        )
        self.connection.commit()

    # -----------------------------
    # READ ALL
    # -----------------------------
    def display_all_batches(self):
        self.cursor.execute(
            """
            SELECT
                batch_id,
                batch_name,
                start_time,
                end_time,
                classroom
            FROM batches
            ORDER BY batch_name
            """
        )
        return self.cursor.fetchall()

    # -----------------------------
    # READ ONE
    # -----------------------------
    def get_batch_details(self, batch_id):
        self.cursor.execute(
            """
            SELECT
                batch_id,
                batch_name,
                start_time,
                end_time,
                classroom
            FROM batches
            WHERE batch_id=%s
            """,
            (batch_id,)
        )
        return self.cursor.fetchone()

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update_batch(
        self,
        batch_id,
        batch_name,
        start_time,
        end_time,
        classroom,
    ):
        self.cursor.execute(
            """
            UPDATE batches
            SET
                batch_name=%s,
                start_time=%s,
                end_time=%s,
                classroom=%s
            WHERE batch_id=%s
            """,
            (
                batch_name,
                start_time,
                end_time,
                classroom,
                batch_id,
            )
        )
        self.connection.commit()

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete_batch(self, batch_id):
        self.cursor.execute(
            """
            DELETE FROM batches
            WHERE batch_id=%s
            """,
            (batch_id,)
        )
        self.connection.commit()

    # -----------------------------
    # SEARCH
    # -----------------------------
    def search_batch(self, keyword):
        keyword = f"%{keyword}%"

        self.cursor.execute(
            """
            SELECT
                batch_id,
                batch_name,
                start_time,
                end_time,
                classroom
            FROM batches
            WHERE
                batch_name LIKE %s
                OR classroom LIKE %s
            ORDER BY batch_name
            """,
            (keyword, keyword)
        )

        return self.cursor.fetchall()

    # -----------------------------
    # STUDENTS OF A BATCH
    # -----------------------------
    def get_students_by_batch(self, batch_id):
        self.cursor.execute(
            """
            SELECT
                student_id,
                full_name,
                phone,
                status
            FROM students
            WHERE batch_id = %s
            ORDER BY full_name
            """,
            (batch_id,)
        )

        return self.cursor.fetchall()
