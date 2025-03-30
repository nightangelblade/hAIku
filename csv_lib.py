import csv


class OutputCSVColumns:
    SOURCE = "source"
    DATE = "date"
    LINE_1 = "line_1"
    LINE_2 = "line_2"
    LINE_3 = "line_3"

    @classmethod
    def all_columns(cls):
        """Return a list of all column names."""
        return [
            cls.SOURCE,
	    cls.DATE,
            cls.LINE_1,
            cls.LINE_2,
            cls.LINE_3,
        ]
    
def save_csv_data(csv_file_path, fieldnames, rows, delimiter):
    with open(
        csv_file_path, "a", encoding="utf-8", newline=""
    ) as csvfile:  # Note: "a" for append mode opens for writing and creates file if doesn't exist
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            delimiter=delimiter,
            quoting=csv.QUOTE_MINIMAL,
        )

        # Write header if file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        for row in rows:
            writer.writerow(row)