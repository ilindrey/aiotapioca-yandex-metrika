from io import StringIO


__all__ = ("ReportsAPIParser", "LogsAPIParser")


class ReportsAPIParser:  # noqa: PIE798
    @classmethod
    def _iter_transform_data(cls, data):
        for row in data["data"]:
            dimensions_data = [i["name"] for i in row["dimensions"]]
            metrics_data = row["metrics"]
            yield dimensions_data + metrics_data

    @classmethod
    def headers(cls, data):
        return data["query"]["dimensions"] + data["query"]["metrics"]

    @classmethod
    def values(cls, data):
        return list(cls._iter_transform_data(data))

    @classmethod
    def dicts(cls, data):
        columns = cls.headers(data)
        return [dict(zip(columns, row)) for row in cls._iter_transform_data(data)]

    @classmethod
    def columns(cls, data):
        cols = None
        for row in cls._iter_transform_data(data):
            if cols is None:
                cols = [[] for _ in range(len(row))]
            for i, col in enumerate(cols):
                col.append(row[i])
        return cols


class LogsAPIParser:  # noqa: PIE798
    @classmethod
    def _iter_line(cls, data):
        lines = StringIO(data)
        next(lines)  # skipping columns
        return (line.replace("\n", "") for line in lines)

    @classmethod
    def headers(cls, data):
        return data[: data.find("\n")].split("\t") if data else []

    @classmethod
    def lines(cls, data):
        return [line for line in data.split("\n")[1:] if line]

    @classmethod
    def values(cls, data):
        return [line.split("\t") for line in data.split("\n")[1:] if line]

    @classmethod
    def dicts(cls, data):
        return [
            dict(zip(cls.headers(data), line.split("\t"))) for line in data.split("\n")[1:] if line
        ]

    @classmethod
    def columns(cls, data):
        cols = [[] for _ in range(len(cls.headers(data)))]
        for line in cls._iter_line(data):
            values = line.split("\t")
            for i, col in enumerate(cols):
                col.append(values[i])
        return cols
