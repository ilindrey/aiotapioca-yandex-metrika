from io import StringIO
from aiotapioca.serializers import SimpleSerializer


class StatsSerializer(SimpleSerializer):
    def _iter_transform_data(self, data):
        for row in data["data"]:
            dimensions_data = [i["name"] for i in row["dimensions"]]
            metrics_data = row["metrics"]
            yield dimensions_data + metrics_data

    def to_headers(self, data):
        return data["query"]["dimensions"] + data["query"]["metrics"]

    def to_values(self, data):
        return list(self._iter_transform_data(data))

    def to_dicts(self, data):
        columns = self.to_headers(data)
        return [dict(zip(columns, row)) for row in self._iter_transform_data(data)]

    def to_columns(self, data):
        columns = None
        for row in self._iter_transform_data(data):
            if columns is None:
                columns = [[] for _ in range(len(row))]
            for i, col in enumerate(columns):
                col.append(row[i])
        return columns


class LogsAPISerializer(SimpleSerializer):
    def _iter_line(self, text):
        f = StringIO(text)
        next(f)  # skipping columns
        return (line.replace("\n", "") for line in f)

    def to_headers(self, data):
        return data[: data.find("\n")].split("\t") if data else []

    def to_lines(self, data):
        return [line for line in data.split("\n")[1:] if line]

    def to_values(self, data):
        return [line.split("\t") for line in data.split("\n")[1:] if line]

    def to_dicts(self, data):
        return [
            dict(zip(self.to_headers(data), line.split("\t")))
            for line in data.split("\n")[1:]
            if line
        ]

    def to_columns(self, data):
        columns = [[] for _ in range(len(self.to_headers(data)))]
        for line in self._iter_line(data):
            values = line.split("\t")
            for i, col in enumerate(columns):
                col.append(values[i])
        return columns
