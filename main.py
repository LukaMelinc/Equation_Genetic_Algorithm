import random
import operator
import numpy as np
import matplotlib.pyplot as plt

"""
Genetski algoritem je vrsta optimizacijskega algoritma, ki imitira delovanje naravne selekcije in koncepte genetike. Ustvarjajo 
se generacije mižnih rešitev, da se skozi generacije izberejo najboljši posamezniki generacije in sse repreducirajo, potomci
pa mutirajo. S ponavljanjem tega se generirajo nove generacije in proces konvergira v optimum. 

"""

# 1) definiramo možne operacije
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
stevilo_starsev = 10 

# postavimo populacijo
def init_populacije(velikost, stevilo_clenov):  # kot argument prejme velikost populacije (št. članov) in stevilo zahtevanih členov v enacbi

    """
    Inicializra se populacija določene velikosti, vsak član populacije ima določen število členov in operatorjev,
    vsak član je naključno izbran z vrednostmi znotraj omejitev.
    Se pokliče samo enkrat, ko se inicializira prvotna populacija, iz katere nato naprej evolvirajo člani.
    """

    populacija = []
    for i in range(velikost): # inicializiramo posameznikov, kolikor je velika populacija
        posamezniki = []   
        for j in range(stevilo_clenov): 
            clen = (random.choice(operacije), random.randint(min_vrednost, max_vrednost))   # Clen v enacbi je nakljucen znotraj meje
            #clen je tuple, ki vsebuje naključen operator in naključno vrednost za operatorjem
            posamezniki.append(clen)
        populacija.append(posamezniki)
    return populacija   # nakoncu imamo list tuplov, ki držijo operator in vrednost, ki jih je, kolikor je velika generacija

def fitness(posameznik):
    
    """
    fitness posazmenega predstavnika nam pove, kako blizu je končni rešitvi, koncu poti. Tisti z boljšim fitnesom so boljši
    predstavniki v posamezni generaciji, so bližje končnemu cilju in so zato boljši kandidati za osnovo za naslednje generacije.
    Funckija se izračuna za vsakega predstavnika posamezne generacije. 
    """
    try:
        equation = str(posameznik[0][1])
        for operacija, vrednost in posameznik[1:]:
            equation += f" {operator_string[operacije.index(operacija)]} {vrednost}"    # sestavimo string, ki predstavlja enačbo
        rating = eval(equation) # eval izračuna dejansko vrednost enačbe
        val_fitness = 1 / (abs(ciljna_vrednost - rating) + 1)  
        # najpomembnejša vrstica funckije, zračunamo fitness člana generacije kot inverz razlike med vrednostjo
        # enačbe in ciljno vrednostjo. Če je razlika=0, je fitness=1, kar pomeni, da smo našli naš ciljni
        # člen/enačbo/predstavnika in nehamo izvajati genetski algoritem
        return val_fitness
    except ZeroDivisionError:
        return 0
    



def izbor_starsev(populacija, fitnessi, stevilo_starsev):

    """
    ta funkcija se izvaja po izračunu fitnessev članov generacije, da se izbere podlago za sledečo generacijo. 
    Pomembno je, koliko staršev se vzame za naslednjo generacijo, z večjim številom staršev se sicer vključi starše s slabšim 
    fitnessom, kar upočasni konvergenco, vendar pa je naslednja generacija bolj raznolika. Z manjšim številom staršev
    se izbere boljšo osnovo za naslednjo generacijo
    """
    celotni_fitness = sum(fitnessi) 
    seznam = [f / celotni_fitness for f in fitnessi]    # znormiramo posamezne fitnesse
    starsi = np.random.choice(len(populacija), size=stevilo_starsev, p=seznam, replace=False)
    # izberemo poljubno število staršev, z večjo verjetnostjo tiste z višjim fitnessem
    return [populacija[i] for i in starsi]


def mesanje(starsi):

    """
    izvaja ti. crossover, kombinira "gene" staršev za generiranje nove generacije 

    """
    #tocka_mesanja = random.randint(1, stevilo_clenov - 1)
    otroci = []
    for i in range(len(starsi)):
        otrok = []
        for j in range(stevilo_clenov):
            vir = random.choice(starsi) # izberemo poljubnega staša
            otrok.append(vir[j])    # dodamo izbrani "gen" iz izbranega starša v otroka
        otroci.append(otrok)
    return otroci

def mutiranje(posameznik):

    """
    določamo, kako bodo mutirali pripadniki generacije - posnemamo obnašanje narave
    Z večjim faktorjem mutacije bomo dobili bolj raznoliko generacijo
    
    """
    for i in range(len(posameznik)):
        if random.random() < faktor_mutacije:
            # preveri, če se bo mutacija zgodila s pomočjo naključnega števila med 0 in 1
            # če je random vrednost večja od praga, ki je faktor_mutacije, se mutacija izvede
            posameznik[i] = (random.choice(operacije), random.randint(min_vrednost, max_vrednost))
    return posameznik

def plot_fitness_history(fitness_history):

    """
    funckija za izpis cenilke skozi generacije
    """
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_history, marker='o', linestyle='-', color='b')
    plt.title('Najvišji fitness skozi generacije')
    plt.xlabel('Generacija')
    plt.ylabel('Najvišji fitness')
    plt.grid(True)
    plt.show()

def GA():
    """
    izvaja celoten algoritem, kliče posamezne funkcije
    """
    populacija = init_populacije(velikost_populacije, stevilo_clenov)   # postavimo prvo generacijo
    fitness_history = []
    for generacijo in range(stevilo_generacij):
        fitnesi = [fitness(posameznik) for posameznik in populacija] # izračunamo fitnesse za posamezno generacijo 
        fitness_history.append(max(fitnesi))
        if max(fitnesi) == 1:
            break
        starsi = izbor_starsev(populacija, fitnesi, stevilo_starsev)    # izberemo število staršev za naslednjo generacijo
        naslednja_populacija = []
        for i in range(0, velikost_populacije, stevilo_starsev):
            otroci = mesanje(starsi)    # mesanje med starsi in generiranje novih torok
            for otrok in otroci:
                naslednja_populacija.append(mutiranje(otrok))   # zmutiramo nove otroke
        populacija = naslednja_populacija[:velikost_populacije]  
    najboljši_posameznik = populacija[np.argmax(fitnesi)]
    return najboljši_posameznik, generacijo, fitness_history

najboljši_posameznik, generacija, fitness_history = GA()
enačba = f"{najboljši_posameznik[0][1]}"
for operacija, vrednost in najboljši_posameznik[1:]:
    enačba += f" {operator_string[operacije.index(operacija)]} {vrednost}"
rezultat = fitness(najboljši_posameznik)

print(f"Končna enačba: {enačba}")
print(f"Število iteracij: {generacija}")
print(f"Rezultat: {ciljna_vrednost / rezultat}")

# Prikaži graf najvišjega fitnessa skozi generacije
plot_fitness_history(fitness_history)

"""
Če je kakšen kontekst čudno napisan ali je kaj nejasnega, moje razumevanje genteskih algoritmov prihaja iz uporabe 
genetskih algoritmov za optimizacijo agentov v igrah kot je recimo Trackmania, kjer se genetski algoritmi uporabljajo
za optimizacijo poti vozil: https://www.youtube.com/watch?v=a8Bo2DHrrow
"""