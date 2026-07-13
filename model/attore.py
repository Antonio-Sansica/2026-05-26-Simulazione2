from dataclasses import dataclass, field
from datetime import date


@dataclass
class Attore:

    id: str
    name: str
    height: int
    date_of_birth: date
    known_for_movies: str
    movies: set = field(default_factory=set)

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        if isinstance(other, Attore):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

