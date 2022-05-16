from io import StringIO

# Reports API


def iter_transform_data(data):
    for row in data["data"]:
        dimensions_data = [i["name"] for i in row["dimensions"]]
        metrics_data = row["metrics"]
        yield dimensions_data + metrics_data


def get_reports_headers(data):
    return data["query"]["dimensions"] + data["query"]["metrics"]


class ReportsAPIParser:
    @staticmethod
    def headers(data):
        return get_reports_headers(data)

    @staticmethod
    def values(data):
        return list(iter_transform_data(data))

    @staticmethod
    def dicts(data):
        columns = get_reports_headers(data)
        return [dict(zip(columns, row)) for row in iter_transform_data(data)]

    @staticmethod
    def columns(data):
        cols = None
        for row in iter_transform_data(data):
            if cols is None:
                cols = [[] for _ in range(len(row))]
            for i, col in enumerate(cols):
                col.append(row[i])
        return cols


# Logs API


def iter_line(data):
    f = StringIO(data)
    next(f)  # skipping columns
    return (line.replace("\n", "") for line in f)


def get_logs_headers(data):
    return data[: data.find("\n")].split("\t") if data else []


class LogsAPIParser:
    @staticmethod
    def headers(data):
        return get_logs_headers(data)

    @staticmethod
    def lines(data):
        return [line for line in data.split("\n")[1:] if line]

    @staticmethod
    def values(data):
        return [line.split("\t") for line in data.split("\n")[1:] if line]

    @staticmethod
    def dicts(data):
        return [
            dict(zip(get_logs_headers(data), line.split("\t")))
            for line in data.split("\n")[1:]
            if line
        ]

    @staticmethod
    def columns(data):
        cols = [[] for _ in range(len(get_logs_headers(data)))]
        for line in iter_line(data):
            values = line.split("\t")
            for i, col in enumerate(cols):
                col.append(values[i])
        return cols
