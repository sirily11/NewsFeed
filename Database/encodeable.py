class Encodeable:

    def to_json(self) -> dict:
        raise NotImplementedError()

    @staticmethod
    def from_json(msg):
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__()
