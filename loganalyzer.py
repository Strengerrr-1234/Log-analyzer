import re
import os
from collections import defaultdict


class LogAnalyzer:
    def __init__(self, log_file_path):
        """
        Initialize the LogAnalyzer.

        Parameters:
        - log_file_path: Path to the log file to analyze
        """
        self.log_file_path = log_file_path

    def parse_logs(self):
        """
        Parse the log file and extract meaningful information.

        Returns:
        - logs: List of parsed log entries
        """
        logs = []

        if not os.path.exists(self.log_file_path):
            raise FileNotFoundError(f"Log file not found: {self.log_file_path}")

        log_entry_pattern = r"^(\S+) (\S+) (\S+) \[(.*?)\] \"(.*?)\" (\d{3}) (\d+|-)"

        with open(self.log_file_path, 'r') as file:
            for line in file:
                match = re.match(log_entry_pattern, line)
                if match:
                    logs.append({
                        "ip": match.group(1),
                        "user_id": match.group(2),
                        "username": match.group(3),
                        "timestamp": match.group(4),
                        "request": match.group(5),
                        "status": int(match.group(6)),
                        "size": int(match.group(7)) if match.group(7).isdigit() else 0,
                    })
        return logs

    def analyze_logs(self):
        """
        Analyze the logs to generate insights.

        Returns:
        - analysis: Dictionary containing analysis results
        """
        logs = self.parse_logs()

        status_count = defaultdict(int)
        total_size = 0
        ip_access_count = defaultdict(int)

        for log in logs:
            status_count[log["status"]] += 1
            total_size += log["size"]
            ip_access_count[log["ip"]] += 1

        most_frequent_ip = max(ip_access_count, key=ip_access_count.get, default=None)

        analysis = {
            "total_requests": len(logs),
            "status_count": dict(status_count),
            "total_data_transferred": total_size,
            "most_frequent_ip": most_frequent_ip,
            "most_frequent_ip_count": ip_access_count.get(most_frequent_ip, 0)
        }
        return analysis

    def display_analysis(self):
        """
        Display the analysis results.
        """
        analysis = self.analyze_logs()

        print("\nLog Analysis Report:")
        print(f"Total Requests: {analysis['total_requests']}")
        print("Status Codes:")
        for status, count in analysis['status_count'].items():
            print(f"  {status}: {count}")
        print(f"Total Data Transferred: {analysis['total_data_transferred']} bytes")
        print(f"Most Frequent IP: {analysis['most_frequent_ip']} ({analysis['most_frequent_ip_count']} requests)")


# Example Usage
if __name__ == "__main__":
    log_file = "access.log"  # Replace with the path to your log file

    analyzer = LogAnalyzer(log_file)
    try:
        analyzer.display_analysis()
    except FileNotFoundError as e:
        print(e)