from UserList import UserList


class GeoJsonFeatureList(UserList):
    @property
    def __geo_interface__(self):
        return dict(
            type="FeatureCollection",
            features=[f.__geo_interface__ for f in self]
        )