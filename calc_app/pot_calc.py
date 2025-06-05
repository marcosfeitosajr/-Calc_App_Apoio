import math
import streamlit as st


def run_calculation(maxNsd: float, Vxd: float) -> None:
    """Execute the POT UNI calculation and display results via Streamlit."""
    pi = math.pi

    # Carga mínima vertical
    minNsd = maxNsd / 10  # N

    # Deslocamento angular
    maxad = 0.02  # rad

    # Carga transversal
    VySd = maxNsd / 10  # N

    # Total carga transversal + vertical
    VxySd = VySd  # N

    # Propriedades dos Materiais
    # Concreto
    fc = 27.5  # m/mm²

    # PTFE
    tPTFE = 8  # mm
    resistencia_PTFE = 46  # N/mm² -referência Planilha ASSHTO-
    d_PTFE = 0.00225  # g/mm³

    # CM Strip
    resistencia_cmstrip = 55  # N/mm²
    d_cmstrip = 0.0088  # g/mm³

    # Elastômero
    fek = 60  # N/mm²
    yMe = 1.3
    PEL = fek / yMe  # N/mm²
    d_el = 0.00408

    # Aço
    fy = 250  # N/mm²
    M_elasticidade_aco = 200000  # N/mm²
    d_aco = 0.00785  # g/mm³

    # Inox
    d_inox = 0.008  # g/mm³
    e_inox = 2  # mm

    # Dimensionamento dos componentes
    D = round(math.sqrt((maxNsd * 4 * yMe) / (fek * pi)), 0) + 1  # mm

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
    Ma = round(VySd * h1, 2)  # Nmm
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
    Ma = round(VySd * h1, 2)  # Nmm
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

    LOL = 50  # mm
    Lpres = 0  # mm
    Wsp = Dpiston + 5
    Lsp = Ls + 2 * Vxd + LOL + Lpres + 5
    fb_ref = 0.7 * fc
    A2 = Wsp * Lsp
    A1 = 1 / A2 * (maxNsd / (0.6 * 0.85 * fc)) ** 2
    fb = 0.35 * fc * math.sqrt(A2 / A1)
    if fb > fb_ref:
        A1 = maxNsd / (0.6 * 1.7 * fc)
        fb = 0.35 * fc * math.sqrt(A2 / A1)
    n = ((Wsp - (math.sqrt((pi * (dPTFE ** 2) / 4)))) / 2)
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

    st.markdown('### Dimensões gerais')
    st.write('A altura total do aparelho é {} mm'.format(T + tmin + hpistao + (tPTFE / 2) + e_inox + Tsp))
    st.write('O peso total do aparelho é {} kg'.format(round(peso_total / 1000, 2)))
    st.write('')
    st.image('Imagem3.png')

    st.markdown('### 1 - Elastômero')
    st.write('O Dp = {} mm'.format(D))
    st.write('A espessura é hr = {} mm'.format(tmin))
    st.write('O peso do elastômero é {} kg'.format(round(peso_elastomero / 1000, 2)))
    st.write('')

    st.image('Imagem5.png')
    st.markdown('### 2 - Pote')
    st.write('O diâmetro interno Dp = {} mm'.format(D))
    st.write('O diâmetro externo no pote é Dpot = {} mm'.format(2 * B + D))
    st.write('A espessura do anel do pote é tw = {} mm'.format(B))
    st.write('A profundidade do Dp é hp1 = {} mm'.format(H))
    st.write('O diâmetro do fundo do pote é Wpot = {} mm'.format(D + B + B + solda + solda + 6))
    st.write('A espessura do fundo do pote é tb = {} mm'.format(T))
    st.write('O cordão de solda é w = {} mm'.format(solda))
    st.write('O peso do pote é {} kg'.format(round(peso_pote / 1000, 2)))
    st.write('')

    st.markdown('### 3 - Pistão')
    st.write('O diâmetro de contato é Dp = {} mm'.format(D))
    st.write('A altura do diâmetro de contato é hw = {} mm'.format(b))
    st.write('O diâmetro externo do pistão é Dmp = {} mm'.format(Dpiston))
    st.write('A altura total do pistão é hp4 = {} mm'.format(hpistao))
    st.write('O diâmetro de alívio é Dal = {} mm'.format(Dal))
    st.write('O chanfro inferior do diâmetro de alívio é hDal = {} mm'.format(chanfro))
    st.write('A altura do chanfro de alívio é de ch = {} mm'.format(chanfro))
    st.write('O ângulo do chanfro superior é ach = {}°'.format(a_chanf))
    st.write('A altura do chanfro superior é sch = {} mm'.format(round(hchanf, 2)))
    st.write('A altura do diâmetro externo é hDmp = {} mm'.format(Hdex))
    st.write('O diâmetro de acomodação do PTFE bipartido é DPTFE = {} mm'.format(dPTFE))
    st.write('A profundidade de acomodação do PTFE é aPTFE = {} mm'.format(tPTFE / 2))
    st.write('O canal da guia será Wgu = {} mm'.format(Wgu))
    st.write('A profundidade do canal da guia a partir do topo do pistão é tWgu = {} mm'.format(tPTFE))
    st.write('O peso do pistão é {} kg'.format(round(peso_pistao / 1000, 2)))
    st.write('')

    st.markdown('### 4 - Bipartido de PTFE')
    st.write('O diâmetro do PTFE bipartido é DPTFE = {} mm'.format(dPTFE))
    st.write('A espessura do PTFE bipartido é tPTFE = {} mm'.format(tPTFE))
    st.write('O peso dos 2 PTFE bipartido é {} kg'.format(round(peso_ptfe / 1000, 2)))
    st.write('')

    st.image('Imagem4.png')
    st.markdown('### 5 - Guia')
    st.write('A altura da guia é Tgu = {} mm'.format(Tgu))
    st.write('A largura da guia é Wgu = {} mm'.format(Wgu))
    st.write('O comprimento da guia é Lgu = {} mm'.format(round(Lgu, 2)))
    st.write('O peso da guia é {} kg'.format(round(peso_guia / 1000, 2)))
    st.write('')

    st.markdown('### 6 - CM Strip')
    st.write('A espessura do CM Strip é CM_t = {} mm'.format(round(CM_t, 2)))
    st.write('A largura do CM Strip é Ws1 = {} mm'.format(Ws1))
    st.write('O comprimento do CM Strip é Lgu = {} mm'.format(Lgu))
    st.write('O peso dos 2 CM Strip é {} kg'.format(round(peso_Cmstrip / 1000, 2)))
    st.write('')

    st.markdown('### 7 - Placa deslizante de inox')
    st.write('A espessura do inox é e_i = {} mm'.format(e_inox))
    st.write('O comprimento do inox dobrado (perímetro externo) é L_i = {} mm'.format(L_inox))
    st.write('O comprimento do inox é Lsp = {} mm'.format(Lsp))
    st.write('O chanfro dos cantos do inox é ch_i = {} mm'.format(chanfro_inox))
    st.write('O raio externo da dobra do inox é r_i = {} mm'.format(raio_inox))
    st.write('O peso dos 2 inox é {} kg'.format(round(peso_inox / 1000, 2)))
    st.write('')

    st.markdown('### 8 - Placa superior')
    st.write('A largura da placa superior é Wsp = {} mm'.format(Wsp))
    st.write('O comprimento da placa superior é Lsp = {} mm'.format(Lsp))
    st.write('A espessura da placa superior é Tsp = {} mm'.format(Tsp))
    st.write('A largura do canal da placa superior é Wgu2 = {} mm'.format(Wgu2))
    st.write('A profunidade do canal da placa superior é Csp = {} mm'.format(cavidade))
    st.write('O peso da placa superior é {} kg'.format(round(peso_placa_sup / 1000, 2)))
    st.write('')
