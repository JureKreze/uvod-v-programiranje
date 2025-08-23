import csv
def shrani_disertacije(disertacije):
    with open("disertacije.csv", "w", newline='', encoding="utf-8") as f:
        pisatelj = csv.writer(f, delimiter="|")
        pisatelj.writerow(
            [
                "ID",
                "Naslov",
                "Avtor",
                "Mentor",
                "Ključne besede",
                "Leto",
                "Jezik",
                "Organizacija",
                "Kraj",
                "Dolžina uvoda",
                "Dolžina glavnega dela",
                "Ogledi",
                "Prenosi",
            ]
        )
        for disertacija in disertacije:
            pisatelj.writerow(
                [
                    disertacija["ID"],
                    disertacija["Naslov"],
                    disertacija["Avtor"],
                    disertacija["Mentor"],
                    disertacija["Ključne besede"],
                    disertacija["Leto izida"],
                    disertacija["Jezik"],
                    disertacija["Organizacija"],
                    disertacija["Kraj izida"],
                    disertacija["dolzina_uvoda"],
                    disertacija["dolzina_glavnega_dela"],
                    disertacija["Število ogledov"],
                    disertacija["Število prenosov"],
                ]
            )

def shrani_komentorje(disertacije):
    with open("disertacije_komentorji.csv", "w", newline='', encoding="utf-8") as f:
        pisatelj = csv.writer(f, delimiter="|")
        pisatelj.writerow(
            [
                "Ime in priimek", #tu bi bilo bolje imeti ID, ker imata 2 osebi lahko enako ime in priimek
            ]
        )
        ze_videni = set()
        for disertacija in disertacije:
            for oseba in disertacija["Komentorji"]:
                if oseba in ze_videni or oseba == "Več o mentorju..." or oseba == "ID":
                    continue
                ze_videni.add(oseba)
                pisatelj.writerow(
                    [
                        oseba,
                    ]
                )
