def down(o, omin, omax):
    return (omax-o)/(omax-omin)

def up(o, omin, omax):
    return(o-omin)/(omax-omin)

class Permintaan():
    minimal = 2049
    maximal = 7493
    median = 4861

    def turun(self, o):
        if o >= self.median:
            return 0
        elif o <= self.minimal:
            return 1
        else :
            return down(o, self.minimal, self.median)
    
    def naik(self, o):
        if o >= self.maximal:
            return 1
        elif o <= self.median:
            return 0
        else :
            return up(o, self.median  , self.maximal)
    
    def tetap(self, o):
        if o >= self.maximal or o <= self.minimal:
            return 0
        elif self.minimal < o < self.median:
            return up(o, self.minimal, self.median)
        elif self.median < o < self.maximal:
            return down(o, self.median, self.maximal)
        else :
            return 1

class Persediaan():
    minimal = 550
    maximal = 1285

    def sedikit(self, k):
        if k >= self.maximal:
            return 0
        elif k <= self.minimal:
            return 1
        else :
            return down(k, self.minimal, self.maximal)
    
    def banyak(self, k):
        if k >= self.maximal:
            return 1
        elif k <= self.minimal:
            return 0
        else :
            return up(k, self.minimal, self.maximal)

class Produksi():
    minimal = 3719
    maximal = 6769
    permintaan = 0
    persediaan = 0

    def _berkurang(self, m):
        return self.maximal - m*(self.maximal - self.minimal)

    def _bertambah(self, m):
        return m*(self.maximal - self.minimal) + self.minimal

    def _inferensi(self, pmt=Permintaan(), psd=Persediaan()):
        result = []
        #1
        r1 = min(pmt.turun(self.permintaan), psd.banyak(self.persediaan))
        y1 = self._berkurang(r1)
        result.append((r1, y1))
        #2
        r2 = min(pmt.turun(self.permintaan), psd.sedikit(self.persediaan))
        y2 = self._berkurang(r2)
        result.append((r2, y2))
        #3
        r3 = min(pmt.naik(self.permintaan), psd.banyak(self.persediaan))
        y3 = self._bertambah(r3)
        result.append((r3, y3))
        #4
        r4 = min(pmt.naik(self.permintaan), psd.sedikit(self.persediaan))
        y4 = self._bertambah(r4)
        result.append((r4, y4))
        #5
        r5 = min(pmt.tetap(self.permintaan), psd.sedikit(self.persediaan))
        y5 = self._bertambah(r5)
        result.append((r5, y5))
        #6
        r6 = min(pmt.tetap(self.permintaan), psd.banyak(self.persediaan))
        y6 = self._berkurang(r6)
        result.append((r6, y6))
        return result

    def defuzifikasi(self, data_inferensi=[]):
        data_inferensi = data_inferensi if data_inferensi else self._inferensi()
        per_r_y = 0
        per_r = 0
        for data in data_inferensi:
            per_r_y += data[0] * data[1]
            per_r += data[0]
        return per_r_y/per_r