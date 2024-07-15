import random
import operator
import numpy as np

# definiramo možne operacije
operacije = [operator.add, operator.sub, operator.mul, operator.truediv]
operator_string = ['+', '-', '*', '/']

# določimo ciljno vrednost in število operacij za dosego ciljne vrednosti
ciljna_vrednost = 39
stevilo_clenov = 5
max_vrednost = 100
min_vrednost = 1

# dolocimo hyperparametre
velikost_populacije = 100
stevilo_generacij = 1000
faktor_mutacije = 0.01

# postavimo populacijo
def init_populacije(velikost, stevilo_clenov):  # kot argument prejme velikost populacije in stevilo clenov v enacbi
    populacija = []
    for i in range(velikost):
        posamezniki = []    # inicializiramo posameznikov, kolikor je velika populacija
        for j in range(stevilo_clenov):
            clen = (random.choice(operacije), random.randint(min_vrednost, max_vrednost))   # Clen v enacbi je nakljucen znotraj meje
            #clen je tuple, ki vsebuje naključen operator in naključno vrednost za operatorjem
            posamezniki.append(clen)
        populacija.append(posamezniki)
    return populacija   # nakoncu imamo list tuplov, ki držijo operator in vrednost

def fitness(posameznik):
    try:
        rating = posameznik[0][1]   # posameznik sestavlja operator in vrednost
        # rating je vrednost prve vrednosti 
        for operacija, vrednost in posameznik[1:]:
            rating = operacija(rating, vrednost)
        val_fitness = 1 / (abs(ciljna_vrednost - rating) + 1)
        return val_fitness
    except ZeroDivisionError:
        return 0    # če pride do deljenja z 0, je fitness posameznika = 0
    
def izbor_starsev(populacija, fitnessi):
    celotni_fitness = sum(fitnessi) # skupni fitnes celotne populacije, da normiramo vrednosti
    seznam = [f / celotni_fitness for f in fitnessi]
    # Za vsakega posameznika zračunamo verjetnost, da ga zberemo: njegov fitness / skupni fitness
    starsa = np.random.choice(len(populacija), size=velikost_populacije, p=seznam)
    return [populacija[i] for i in starsa]

def mesanje(stars1, stars2):
    tocka_mesanja = random.randint(1, stevilo_clenov - 1)
    otrok1 = stars1[:tocka_mesanja] + stars2[tocka_mesanja:]
    otrok2 = stars2[:tocka_mesanja] + stars1[tocka_mesanja:]
    return otrok1, otrok2

def mutiranje(posameznik):
    for i in range(len(posameznik)):
        if random.random() < faktor_mutacije:
            posameznik[i] = (random.choice(operacije), random.randint(min_vrednost, max_vrednost))
    return posameznik

def GA():
    populacija = init_populacije(velikost_populacije, stevilo_clenov)
    for generacijo in range(stevilo_generacij):
        fitnesi = [fitness(posameznik) for posameznik in populacija]
        if max(fitnesi) == 1:
            break
        starsi = izbor_starsev(populacija, fitnesi)
        naslednja_populacija = []
        for i in range(0, velikost_populacije, 2):
            stars1 = starsi[i]
            stars2 = starsi[i+1]
            otrok1, otrok2 = mesanje(stars1, stars2)
            naslednja_populacija.append(mutiranje(otrok1))
            naslednja_populacija.append(mutiranje(otrok2))
        populacija = naslednja_populacija
    najboljši_posameznik = populacija[np.argmax(fitnesi)]
    return najboljši_posameznik, generacijo

najboljši_posameznik, generacija = GA()
enačba = f"{najboljši_posameznik[0][1]}"
for operacija, vrednost in najboljši_posameznik[1:]:
    enačba += f" {operator_string[operacije.index(operacija)]} {vrednost}"
rezultat = fitness(najboljši_posameznik)
print(f"Končna enačba: {enačba}")
print(f"Število iteracij: {generacija}")
print(f"Rezultat: {ciljna_vrednost / rezultat}")
