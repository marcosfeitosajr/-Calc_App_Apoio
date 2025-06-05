import math
from dataclasses import dataclass

@dataclass
class PotCalculator:
    """Perform POT UNI calculations."""
    maxNsd: float
    Vxd: float

    def calculate(self):
        pi = math.pi
        maxNsd = self.maxNsd
        Vxd = self.Vxd
        minNsd = maxNsd / 10  # N
        maxad = 0.02  # rad
        VySd = maxNsd / 10  # N
        VxySd = VySd  # N
        fc = 27.5
        tPTFE = 8
        resistencia_PTFE = 46
        d_PTFE = 0.00225
        resistencia_cmstrip = 55
        d_cmstrip = 0.0088
        fek = 60
        yMe = 1.3
        PEL = fek / yMe
        d_el = 0.00408
        fy = 250
        M_elasticidade_aco = 200000
        d_aco = 0.00785
        d_inox = 0.008
        e_inox = 2
        D = round(math.sqrt((maxNsd * 4 * yMe) / (fek * pi)), 0) + 1
        espessura = round(3.33 * maxad * D, 2)
        if espessura < D / 15:
            tmin = round(D / 15, 0) + 1
        else:
            tmin = round(espessura, 0) + 1
        if D > 600:
            CM_t = 6.35
        else:
            CM_t = 0.1875 * 25.4
        yM = 1
        if 0.01 * D > 3:
            ad = 0.01 * D
        else:
            ad = 3
        if ad > 10:
            ad = 10
        b = round(tmin / 1.75, 0) + 1
        H = round(tmin + b * 0.5 + (maxad * 0.5 * D) * ad, 0) + 1
        B = round((D * tmin * PEL + VxySd) / ((fy / yM) * 2 * H), 0) + 1
        if D < 300:
            T = 12.7
            solda = 6
        elif 300 < D < 600:
            T = 15.875
            solda = 8
        elif 600 < D < 1000:
            T = 19.05
            solda = 10
        else:
            T = 25.4
            solda = 12
        cateto_a = D / 2
        cateto_o = cateto_a * math.sin(maxad)
        Dref = 2 * (math.sqrt(cateto_a ** 2 + cateto_o ** 2) + B)
        hp = round(H - tmin + ad + (maxad * 0.5 * Dref), 0) + 1
        T_PTFE_PAD = hp - tPTFE / 2
        Dpiston = D
        Ls = Dpiston
        Ws1 = round(VySd / resistencia_cmstrip / Ls, 0)
        Ws = Ws1
        FOS = 1.5
        Cavidade_assento_guia = tPTFE / 2
        raio_inox = 3 * e_inox
        Tgu = round(Ws + tPTFE + Cavidade_assento_guia + raio_inox, 0) + 1
        Lgu = Dpiston
        h1 = Tgu - (Ws / 2)
        Gmax = fy / FOS
        Ma = round(VySd * h1, 2)
        Wgu = ((Ma * 32.174 * 12 * 0.5) / (Gmax * Lgu ** 3)) * Lgu / 2
        if 2 * Wgu > Dpiston:
            Dpiston = 2 * Wgu + 1
        Dmin_PTFE = round(2 * math.sqrt((maxNsd / resistencia_PTFE) / pi), 0) + 1
        Abip = pi * Dmin_PTFE ** 2 / 4
        Abip = Abip / 2
        a = math.degrees(math.asin(2 * Wgu / Dpiston))
        a = 180 - a
        r = 6 * math.sqrt(10 * pi * Abip * a) / (pi * a)
        dPTFE = round(2 * r, 0) + 1
        Dpiston = dPTFE + 20
        Lgu = Dpiston - 5
        h1 = Tgu - (Ws / 2)
        Gmax = fy / FOS
        Ma = round(VySd * h1, 2)
        Wgu = round(((Ma * 32.174 * 12 * 0.5) / (Gmax * Lgu ** 3)) * Lgu / 2, 0)
        gap = 1.5
        Wgu2 = Wgu + 2 * (e_inox + CM_t + gap)
        chanfro = 4
        Dal = D - chanfro * 2
        hDal = 5
        chanf = (Dpiston - Dal) / 2
        a_chanf = 15
        hchanf = math.sin(math.radians(a_chanf)) * (Dpiston / 2 - Dal / 2)
        Hdex = tPTFE * 3 / 2
        if H - tmin > b:
            hDal_rec = H - tmin - b - chanfro + hDal
        else:
            hDal_rec = 0
        hpistao = round(hp + hchanf + hDal_rec, 0) + 1
        arad = math.asin(2 * Wgu / Dpiston)
        adeg = math.degrees(arad)
        angPTFE = 90 - adeg / 2
        aredPTFE = math.radians(angPTFE)
        Lgu = math.sin(aredPTFE) * (Dpiston / 2) * 2
        LOL = 50
        Lpres = 0
        Wsp = Dpiston + 5
        Lsp = Ls + 2 * Vxd + LOL + Lpres + 5
        fb_ref = 0.7 * fc
        A2 = Wsp * Lsp
        A1 = 1 / A2 * (maxNsd / (0.6 * 0.85 * fc)) ** 2
        fb = 0.35 * fc * math.sqrt(A2 / A1)
        if fb > fb_ref:
            A1 = maxNsd / (0.6 * 1.7 * fc)
            fb = 0.35 * fc * math.sqrt(A2 / A1)
        n = (Wsp - (math.sqrt((pi * (dPTFE ** 2) / 4)))) / 2
        Tspm = round(2 * n * math.sqrt(fb / fy), 0) + 1
        cavidade = Tgu - tPTFE - Cavidade_assento_guia + 3
        Tsp = Tspm + cavidade
        Ltotal_inox = dPTFE + pi * raio_inox ** 2 / 2 + 2 * (Ws1 + 1.5)
        L_inox = round(Ws1 + pi * raio_inox * 2 / 4 + (dPTFE - Wgu2 - 2 * (raio_inox - e_inox)) / 2, 0) + 3
        chanfro_inox = round((Wgu2 + 2 * (raio_inox - e_inox)) / 2 - (Ws1 + 2 * pi * raio_inox / 4) + L_inox - dPTFE / 4, 0)
        peso_elastomero = pi * D ** 2 / 4 * tmin * d_el
        vol_anel = (pi * ((2 * B + D) ** 2 - D ** 2) / 4 * H)
        vol_fundo = pi * (D + B + B + solda + solda + 6) ** 2 / 4 * T
        vol_solda = pi * ((2 * (B + solda) + D) ** 2 - (2 * B + D) ** 2) / 8 * solda
        peso_pote = (vol_anel + vol_fundo + vol_solda) * d_aco
        vol_corpo1 = pi * D ** 2 / 4 * b
        vol_corpo2 = (pi * (D ** 2 - (D - 2 * chanfro) ** 2) / 4 * chanfro * 0.5) + ((pi * (D - 2 * chanfro) ** 2) / 4 * chanfro)
        hDal_vol = hpistao - (tPTFE * 1.5) - b - chanfro - hchanf
        vol_corpo3 = pi * Dal ** 2 / 4 * hDal_vol
        vol_corpo4 = (pi * (Dpiston ** 2 - Dal ** 2) / 4 * hchanf * 0.5) + ((pi * Dal ** 2) / 4 * hchanf)
        vol_corpo5 = pi * Dpiston ** 2 / 4 * Hdex
        a = a_chanf
        sina = math.sin(math.radians(a))
        r = Dpiston / 2
        vol_corpo6sub = -((a * pi * r ** 2 / 360) - (r * 2 * sina)) / 100 * tPTFE * 1.5 * 2
        vol_corpo7 = Wgu * Lgu * tPTFE * 0.5
        vol_corpo8 = pi * Dpiston ** 2 / 4 * tPTFE * 0.5
        vol_corpo9sub = -Abip * tPTFE
        vol_corpo10sub = -Wgu * 20 * tPTFE * 2
        vol_pistao = vol_corpo1 + vol_corpo2 + vol_corpo3 + vol_corpo4 + vol_corpo5 + vol_corpo6sub + vol_corpo7 + vol_corpo8 + vol_corpo9sub + vol_corpo10sub
        peso_pistao = vol_anel * d_aco
        peso_guia = Wgu * Tgu * Lgu * d_aco
        peso_Cmstrip = Ws1 * Lgu * CM_t * d_cmstrip * 2
        peso_inox = (L_inox * Lsp - chanfro_inox ** 2) * e_inox * d_inox * 2
        peso_ptfe = Abip * tPTFE * d_PTFE
        peso_placa_sup = (Wsp * Tsp - Wgu2 * cavidade) * Lsp * d_aco
        peso_total = peso_elastomero + peso_pote + peso_pistao + peso_guia + peso_Cmstrip + peso_inox + peso_placa_sup
        return {
            "T_total": T + tmin + hpistao + (tPTFE / 2) + e_inox + Tsp,
            "peso_total": round(peso_total / 1000, 2),
            "D": D,
            "tmin": tmin,
            "peso_elastomero": round(peso_elastomero / 1000, 2),
            "B": B,
            "H": H,
            "T": T,
            "solda": solda,
            "peso_pote": round(peso_pote / 1000, 2),
            "Dpiston": Dpiston,
            "hpistao": hpistao,
            "Dal": Dal,
            "chanfro": chanfro,
            "a_chanf": a_chanf,
            "hchanf": round(hchanf, 2),
            "Hdex": Hdex,
            "dPTFE": dPTFE,
            "Wgu": Wgu,
            "Tgu": Tgu,
            "Lgu": round(Lgu, 2),
            "b": b,
            "peso_pistao": round(peso_pistao / 1000, 2),
            "peso_guia": round(peso_guia / 1000, 2),
            "peso_ptfe": round(peso_ptfe / 1000, 2),
            "Ws1": Ws1,
            "CM_t": CM_t,
            "peso_Cmstrip": round(peso_Cmstrip / 1000, 2),
            "e_inox": e_inox,
            "L_inox": L_inox,
            "Lsp": Lsp,
            "chanfro_inox": chanfro_inox,
            "raio_inox": raio_inox,
            "peso_inox": round(peso_inox / 1000, 2),
            "Wsp": Wsp,
            "Tsp": Tsp,
            "Wgu2": Wgu2,
            "cavidade": cavidade,
            "peso_placa_sup": round(peso_placa_sup / 1000, 2),
        }

