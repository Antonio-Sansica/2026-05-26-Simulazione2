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
        return f"[{self.id}] {self.name}"

    def __eq__(self, other):

        if isinstance(other, Attore):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)


    @property
    def eta(self):

        oggi = date.today()

        anno_nascita = self.date_of_birth.year
        mese_nascita = self.date_of_birth.month
        giorno_nascita = self.date_of_birth.day


        eta_calcolata = oggi.year - anno_nascita

        if (oggi.month, oggi.day) < (mese_nascita, giorno_nascita):
            eta_calcolata -= 1

        return eta_calcolata
