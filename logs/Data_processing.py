import pandas as pd
import random
import logging
import string
import matplotlib.pyplot as plt


# -------------------------------------------------
# Function to generate a random log entry
# -------------------------------------------------
def generate_log_entry():
    """
    Generates a random log entry with a timestamp,
    log level, action, and user.
    """
    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    log_level = random.choice(["INFO", "DEBUG", "ERROR", "WARNING"])
    action = random.choice(["Login", "Logout", "Data Request", "FileUpload", "Download", "Error"])
    user = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    return f"{timestamp} - {log_level} - {action} - User: {user}"


# -------------------------------------------------
# Function to write logs to a file
# -------------------------------------------------
def write_logs_to_file(log_filename, num_entries=100):
    """
    Writes the specified number of log entries to a file.
    """
    try:
        with open(log_filename, 'w') as file:
            for _ in range(num_entries):
                log = generate_log_entry()
                file.write(log + '\n')

        print(f"Logs successfully written to '{log_filename}'")

    except Exception as e:
        logging.error(f"Error in write_logs_to_file: {e}")
        print("An error occurred while writing logs.")


# -------------------------------------------------
# Function to load and process log data
# -------------------------------------------------
def load_and_process_logs(log_filename="generated_logs.txt"):
    """
    Loads and processes logs from the file,
    cleans timestamps, and sets index.
    """
    try:
        df = pd.read_csv(
            log_filename,
            sep=' - ',
            header=None,
            names=["Timestamp", "Log_level", "Action", "User"],
            engine='python'
        )

        # Clean timestamp
        df['Timestamp'] = df['Timestamp'].str.strip()
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

        # Remove invalid timestamps
        df = df.dropna(subset=['Timestamp'])

        if df.empty:
            print("No valid log data found.")
            return None

        # Set Timestamp as index for time-based analysis
        df.set_index('Timestamp', inplace=True)

        print("Log data loaded and processed successfully.")
        print(df.head())

        return df

    except Exception as e:
        print(f"Error processing log file: {e}")
        return None


# -------------------------------------------------
# Function to analyze log data
# -------------------------------------------------
def analyze_data(df):
    """
    Performs basic statistical analysis on log data.
    """
    try:
        if df is None or df.empty:
            print("No data available for analysis.")
            return None

        log_level_counts = df['Log_level'].value_counts()
        action_counts = df['Action'].value_counts()

        log_count = len(df)
        unique_users = df['User'].nunique()

        logs_per_day = df.resample('D').size()
        average_logs_per_day = logs_per_day.mean()
        max_logs_per_day = logs_per_day.max()

        print("\n--- Log Analysis Summary ---")
        print("\nLog Level Counts:\n", log_level_counts)
        print("\nAction Counts:\n", action_counts)
        print(f"\nTotal Number of Logs: {log_count}")
        print(f"Unique Users: {unique_users}")
        print(f"Average Logs per Day: {average_logs_per_day}")
        print(f"Maximum Logs per Day: {max_logs_per_day}")

        return {
            "log_level_counts": log_level_counts,
            "action_counts": action_counts,
            "log_count": log_count,
            "unique_users": unique_users,
            "average_logs_per_day": average_logs_per_day,
            "max_logs_per_day": max_logs_per_day
        }

    except Exception as e:
        print(f"Error analyzing data: {e}")
        return None


# -------------------------------------------------
# Function to visualize trends using Matplotlib
# -------------------------------------------------
def visualize_trends(df):
    """
    Visualizes log frequency trends over time.
    """
    try:
        logs_by_day = df.resample('D').size()

        plt.figure(figsize=(10, 5))
        plt.plot(logs_by_day.index, logs_by_day.values, marker='o')
        plt.title("Log Frequency Over Time")
        plt.xlabel("Date")
        plt.ylabel("Number of Logs")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error visualizing data: {e}")


# -------------------------------------------------
# Main Execution
# -------------------------------------------------
if __name__ == "__main__":

    log_filename = "generated_logs.txt"

    # Step 1: Generate and write logs
    write_logs_to_file(log_filename, num_entries=200)

    # Step 2: Load and process logs
    df_logs = load_and_process_logs(log_filename)

    # Step 3: Analyze data
    if df_logs is not None:
        analyze_data(df_logs)

        # Step 4: Visualize trends
        visualize_trends(df_logs)
