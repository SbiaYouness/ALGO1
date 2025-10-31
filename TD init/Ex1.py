from datetime import date

tuple_inventaire=("nom","prix","quantite","category")
inventaire=[{"id":1, "nom":"try", "prix":3000, "quantite":32, "category":"skincare"},
            {"id":2, "nom":"try2", "prix":30123, "quantite":13, "category":"computer"},
            {"id":3, "nom":"try3", "prix":1230, "quantite":3, "category":"skincare"},
            {"id":4, "nom":"try4", "prix":1200, "quantite":23, "category":"phone"},
            {"id":5, "nom":"try5", "prix":1300, "quantite":2, "category":"skincare"},
            {"id":6, "nom":"try6", "prix":2300, "quantite":5, "category":"computer"},
            {"id":7, "nom":"try7", "prix":3300, "quantite":12, "category":"phone"},
            {"id":8, "nom":"try8", "prix":4300, "quantite":7, "category":"skincare"},
            {"id":9, "nom":"try9", "prix":5300, "quantite":9, "category":"computer"},
            {"id":10, "nom":"try10", "prix":6300, "quantite":11, "category":"phone"}]

historique=[{"id":1, "old_quantite":5, "new_quantite":4, "Date_Op":date(2025, 10, 25)},
            {"id":2, "old_quantite":15, "new_quantite":13, "Date_Op":date(2025, 10, 24)},
            {"id":3, "old_quantite":8, "new_quantite":3, "Date_Op":date(2025, 10, 23)},
            {"id":1, "old_quantite":35, "new_quantite":32, "Date_Op":date(2025, 10, 22)},
            {"id":4, "old_quantite":25, "new_quantite":23, "Date_Op":date(2025, 10, 21)},
            {"id":5, "old_quantite":5, "new_quantite":2, "Date_Op":date(2025, 10, 20)},
            {"id":6, "old_quantite":8, "new_quantite":5, "Date_Op":date(2025, 10, 19)},
            {"id":7, "old_quantite":15, "new_quantite":12, "Date_Op":date(2025, 10, 18)},
            {"id":8, "old_quantite":10, "new_quantite":7, "Date_Op":date(2025, 10, 17)},
            {"id":9, "old_quantite":12, "new_quantite":9, "Date_Op":date(2025, 10, 16)}]
minS=5
dictmp={}
count=0

# print(inventaire[4].get("nom"))

while count == 0:
    print("\n\n444- TO EXIT ", end="     ***************      ")
    print("0- VENTE PRODUIT ")
    print("1- ACHAT PRODUIT ", end=" ***** ")
    print("2- AJOUTER PRODUIT ", end=" ***** ")
    print("3- SUPPRIMER PRODUIT ")
    print("4- VALEUR DU STOCK ",  end=" ***** ")
    print("5- RECHERCHE PAR CATEGORIE ", end=" ***** ")
    print("6- RAPPORT VENTE ")

    choice= int(input("CHOISIR LE NOMBRE CONVENABLE: "))


    match choice:
        case 444 :
            count = int(input("Are you sure? \n 1 TO LEAVE \n 0 TO STAY\n"))
            if count==0:
                continue
            elif count ==1:
                break
        case 0 :
            # FIX: Reset dictionary to avoid data contamination between operations
            dictmp = {}
            print("Available products:")
            for item in inventaire:
                print(f"ID: {item['id']}, Name: {item['nom']}")

            dictmp["id"]=int(input("ecrit ID de votre produit\n"))
            dictmp["new_quantite"]=int(input("Quantite vendue: "))

            for id in inventaire:
                if id["id"] == dictmp["id"]:
                    dictmp["old_quantite"]= id["quantite"]
                    id["quantite"]= id["quantite"]- dictmp["new_quantite"]
                    # FIX: Don't overwrite new_quantite - keep it as sold amount
                    # dictmp["new_quantite"]= id["quantite"]  # OLD CODE - CAUSES WRONG HISTORIQUE
                    if id["quantite"] < minS:
                        print("!!!WARNING STOCK OF PRODUCT IS RUNNING LOW!!!!")
                    # FIX: Add break to exit loop after finding product
                    break
                    print("Updated quantite:")
                    print(f"Name: {id['nom']}, Nouvelle Quantite: {id['quantite']}")

            dictmp["Date_Op"]=date.today()
            historique.append(dictmp) 

        case 1 :
            # FIX: Reset dictionary to avoid data contamination between operations
            dictmp = {}
            print("Available products:")
            for item in inventaire:
                print(f"ID: {item['id']}, Name: {item['nom']}")

            dictmp["id"]=int(input("ecrit ID de votre produit\n"))
            dictmp["new_quantite"]=int(input("Quantite achetee: "))

            for id in inventaire:
                if id["id"] == dictmp["id"]:
                    dictmp["old_quantite"]= id["quantite"]
                    id["quantite"]= id["quantite"] + dictmp["new_quantite"]
                    # FIX: Don't overwrite new_quantite - keep it as purchased amount
                    # dictmp["new_quantite"]= id["quantite"]  # OLD CODE - CAUSES WRONG HISTORIQUE
                    # FIX: Add break to exit loop after finding product
                    break  
            dictmp["Date_Op"]=date.today()
            historique.append(dictmp)
            print("Updated quantite:")
            for item in inventaire:
                print(f"Name: {item['nom']}, Quantite: {item['quantite']}")

        case 2 :
            # FIX: Reset dictionary to avoid data contamination between operations
            dictmp = {}
            for x in tuple_inventaire:
                if x == "prix" or x == "quantite":
                    dictmp[x] = int(input(f"Enter the {x}:"))
                else :
                    dictmp[x] = input(f"Enter the {x}:")
            dictmp["id"]=len(inventaire)+1
            inventaire.append(dictmp)    
            print("New Inventory:")
            for item in inventaire:
                print(f"ID: {item['id']}, Name: {item['nom']}, Prix: {item['prix']}, Quantite: {item['quantite']}, Categorie: {item['category']}")
    
        case 3 :
            # FIX: Reset dictionary to avoid data contamination between operations
            dictmp = {}
            print("Available products:")
            for item in inventaire:
                print(f"ID: {item['id']}, Name: {item['nom']}")
            print()
            dictmp["id"]=int(input("ID de votre produit a SUPPRIMER\n"))
            for id in inventaire:
                if id["id"] == dictmp["id"]:
                    inventaire.remove(id)
                    # FIX: Add break to exit loop after finding and removing product
                    break 
            print("Apres suppression:")
            for item in inventaire:
                print(f"ID: {item['id']}, Name: {item['nom']}")
            print()

        case 4 :
            total=0
            for item in inventaire:
                total+=item["quantite"]*item["prix"]
            print()
            print("La valeur du stock totale est:", total,"dh")

        case 5 :
            # FIX: Reset dictionary and show unique categories only
            dictmp = {}
            print("Les categories disponibles:")
            # FIX: Use set() to show unique categories instead of duplicates
            categories = set(x['category'] for x in inventaire)
            for cat in categories:
                print(f"CAT: {cat}")
            print()
            dictmp["category"]=input("Entrez la categorie a rechercher\n")
            for cat in inventaire:
                if cat["category"] == dictmp["category"]:
                   print(f"ID: {cat['id']}, Name: {cat['nom']}, Prix: {cat['prix']}, Quantite: {cat['quantite']}, Categorie: {cat['category']}")

        case 6 :
            sales_dict = {}  # Use separate dictionary
            for inv in inventaire:
                sales_dict[str(inv["id"])] = 0
                for his in historique:
                    if inv["id"]==his["id"] and his["old_quantite"] > his["new_quantite"]:
                        sales_dict[str(inv["id"])] += his["old_quantite"] - his["new_quantite"]
           
            print("Les produits les plus vendus:\n")
            
            # Create a copy to avoid KeyError
            remaining_items = sales_dict.copy()
            
            while len(remaining_items) > 0:
                # Find max value and its key
                max_val = max(remaining_items.values())
                max_id = None
                
                for i, j in remaining_items.items():
                    if j == max_val:
                        max_id = i
                        break
                
                # Print the result
                for cat in inventaire:
                    if cat["id"] == int(max_id):
                        print(f"ID: {cat['id']}, Nom: {cat['nom']}, Quantite vendue: {remaining_items[max_id]}")
                        break
                
                # Remove from copy (not original)
                del remaining_items[max_id]