def remove_data_before_last_x_days(days: int, connection):
    if connection:
        cursor = connection.cursor()

        cursor.execute(
            f"DELETE FROM network_history WHERE `datetime` < datetime('now', '-{days} day')"
        )
        connection.commit()
