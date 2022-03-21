
from aiotapioca.serializers import SimpleSerializer


class StatsSerializer(SimpleSerializer):

    def _iter_transform_data(self, data):
        for row in data["data"]:
            dimensions_data = [i["name"] for i in row["dimensions"]]
            metrics_data = row["metrics"]
            yield dimensions_data + metrics_data

    def to_values(self, data):
        return list(self._iter_transform_data(data))

    def to_columns(self, data, **kwargs):
        columns = None
        for row in self._iter_transform_data(data):
            if columns is None:
                columns = [[] for _ in range(len(row))]
            for i, col in enumerate(columns):
                col.append(row[i])
        return columns

    def to_dicts(self, data):
        columns = data["query"]["dimensions"] + data["query"]["metrics"]
        return [
            dict(zip(columns, row))
            for row in self._iter_transform_data(data)
        ]
