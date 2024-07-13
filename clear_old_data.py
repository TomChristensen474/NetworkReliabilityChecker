from db_connector import create_connection

def remove_data_before_last_x_days(days: int):
    connection = create_connection("networy_history.db")

    if connection:
        cursor = connection.cursor()

        cursor.execute(f"DELETE FROM network_history WHERE time < datetime('now', '-{days} days')")

        connection.commit()
        connection.close()

remove_data_before_last_x_days(3)