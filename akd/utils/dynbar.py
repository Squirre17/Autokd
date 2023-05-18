# dynamic bar
from tqdm import tqdm

class Dynbar(tqdm):
    def update_to(self, b = 1, bsize = 1, tsize = None) -> None:
        if tsize is not None:
            self.total = tsize
        return self.update(b * bsize - self.n)  # also sets self.n = b * bsize