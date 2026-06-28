from dataclasses import dataclass
from datetime import date


@dataclass
class Attore:
    id: int
    name: str
    height: int
    date_of_birth: date
    known_for_movies: str


    @property
    def eta(self):
        oggi = date.today()
        anno_nascita= self.date_of_birth.year
        mese_nascita=self.date_of_birth.month
        giorno_nascita=self.date_of_birth.day

        eta = oggi.year - anno_nascita

        if(oggi.month, oggi.day) < (mese_nascita, giorno_nascita):
            eta -= 1
        return eta

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        if isinstance(other, Attore):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
