import math
import random
from functools   import partial
import matplotlib.pyplot    as plt
from collections import defaultdict
import matplotlib.animation as animation

def uzaklikFormul(x, y):
    """
    Euclidean distance formülü tanımı
    """
    return math.sqrt((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2)

def mesafe_matrisi(saltData):
    """
    Her bir nokta arasındaki mesafe matrisini hesaplar.
    """
    uzaklık_matrisi = defaultdict(dict)
    for x in saltData:
        for y in saltData:
            uzaklık_matrisi[x][y] = uzaklık_matrisi[y][x] = uzaklikFormul(x, y)
    return uzaklık_matrisi 

def cozum_mesafesi(cozum, uzaklık_matrisi ):
    """
    Bir çözeltinin toplam uzunluğunu hesaplar.
    """
    toplam_uzaklık = 0

    for i in range(len(cozum) - 1):
        toplam_uzaklık += uzaklık_matrisi[cozum[i]][cozum[i + 1]]

    return toplam_uzaklık

def individualOlusturma(saltData):
    """
    Point set'inin içinde koordinatlarımız var ve bunları listeye cevirip shuffle yapıyoruz.
    Belirli bir şehirden diğer şehire gitme gibi spesifik bir şey olmadığı için random yapıldı.
    """
    cities = list(saltData)
    random.shuffle(cities)

    return cities

def populationOlusturma(n_adet_individuals, saltData, uzaklık_matrisi):
    """
    Populasyon olusturma aşaması
    """
    individuals = [individualOlusturma(saltData) for _ in range(n_adet_individuals)]
    uzaklıklar = list(map(partial(cozum_mesafesi,
                                 uzaklık_matrisi  = uzaklık_matrisi), individuals))

    return sorted(zip(individuals, uzaklıklar), key = lambda x: x[1])

def plot_result(cozum):
    """
    Sonucu görsel hale getirildi
    """
    xs = [point[0] for point in cozum]
    ys = [point[1] for point in cozum]
    plt.plot(xs, ys)
    plt.axis('off')
    plt.show()

def plot_point_set(saltData):
    """
    #Genler ilk önce görsel halinde gösterildi
    """
    point_list = list(saltData)
    xs = [point[0] for point in point_list]
    ys = [point[1] for point in point_list]
    plt.scatter(xs, ys)
    plt.axis('off')
    plt.show()

def mutate(individual, uzaklık_matrisi):
    def mutation_swap_operator():
        swap_index       = random.randint(0, len(individual) - 2)
        yeni_individual = individual[:swap_index] + \
                         [individual[swap_index + 1], individual[swap_index]] + \
                         individual[swap_index + 2:]

        return yeni_individual

    mutasyon = mutation_swap_operator 
    yeni_individual = mutasyon()

    return yeni_individual, cozum_mesafesi(yeni_individual, uzaklık_matrisi)

def reproduce(individual_1, individual_2, uzaklık_matrisi):
    def altkume_olustur(altkume_buyuklugu):
        return sorted(random.sample(range(individual_buyuklugu), altkume_buyuklugu))

    def altkume_sec(individual, altkume_index):
        return [individual[i] for i in altkume_index]

    def altkume_birlestir(individual_2, individual_1):
        s = set(individual_1)

        return [point for point in individual_2 if point not in s]

    individual_buyuklugu = len(individual_1)
    individual_1_altkume_buyuklugu = individual_buyuklugu // 2
    altkume_indindividual_1_index  = altkume_olustur(individual_1_altkume_buyuklugu)
    individual_1_altkume     = altkume_sec(individual_1, altkume_indindividual_1_index)
    individual_2_altkume     = altkume_birlestir(individual_2, individual_1_altkume)

    yeni_individual = individual_1_altkume + individual_2_altkume 

    return yeni_individual, cozum_mesafesi(yeni_individual,
                                                     uzaklık_matrisi )

def evolve(populasyon, reproductions_adeti, mutasyon_adeti, yeni_adet,
           ureme_havuzu, uzaklık_matrisi, saltData):
    """
    Bu işlev popülasyonun evriminin bir adımını hesaplar. 
    Listenin üstteki "ureme_havuzu" kısmındaki "reproductions_adeti" bireyleri seçer ve 
    bunları başka bir rastgele bireyle yeniden üretir. 
    Genom çeşitliliğini korumak için popülasyonlara "mutasyon_adeti” rastgele birey mutasyonları eklenir. 
    Son olarak "yeni_adet" birey rastgele oluşturulur ve popülasyona eklenir.
    """
    populayon_buyuklugu       = len(populasyon)
    n_adet_yeni_individuals     = reproductions_adeti + mutasyon_adeti + yeni_adet
    hayattakiler           = populayon_buyuklugu - n_adet_yeni_individuals
    ureme_havuzu_buyuklugu = round(ureme_havuzu * populayon_buyuklugu)
    yeni_population        = populasyon[:hayattakiler]

    for _ in range(reproductions_adeti):
        individual_1 = populasyon[random.randint(0, ureme_havuzu_buyuklugu - 1)][0]
        individual_2 = random.choice(populasyon)[0]
        yeni_population.append(reproduce(individual_1, individual_2, uzaklık_matrisi))

    for _ in range(mutasyon_adeti):
        individualdan_mutasyona = random.choice(populasyon)[0]
        yeni_population.append(mutate(individualdan_mutasyona, uzaklık_matrisi))

    for _ in range (yeni_adet):
        yeni_individual = individualOlusturma(saltData)
        yeni_population.append((yeni_individual,
                               cozum_mesafesi(yeni_individual, uzaklık_matrisi)))

    return sorted(yeni_population, key = lambda x: x[1])
a=[]
def genetik_algoritma(saltData, populayon_buyuklugu, generations_sayisi,
                      reproductions_adeti, mutasyon_adeti, yeni_adet, ureme_havuzu):
    """
    Bir popülasyon yaratır ve argümanlara göre evrilmesini sağlar.
    """
    uzaklık_matrisi = mesafe_matrisi(saltData)
    populasyon     = populationOlusturma(populayon_buyuklugu, saltData, uzaklık_matrisi)

    for i in range(generations_sayisi):
        populasyon = evolve(populasyon, reproductions_adeti, mutasyon_adeti,
                            yeni_adet, ureme_havuzu, uzaklık_matrisi, saltData)
        print('Generation sayisi', i, 'en iyi uzunluk:', round(populasyon[0][1]/10,2))
        a.append(round(populasyon[0][1]/10,2))
    return populasyon[0]

if __name__ == '__main__':
    import data
    saltData= data.a
    print(saltData)
    print("****")
    plot_point_set(saltData)
    en_iyi_sonuc, uzunluk = genetik_algoritma(saltData, 1000, 100, 1000, 500, 0, 0.30) #parametreler
    lowest=min(a)
    print(lowest)
    plot_result(en_iyi_sonuc)
    