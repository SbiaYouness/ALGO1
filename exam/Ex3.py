import time


def decorateur_analyseur(f):
    def wrapper(*args, **kwargs):
        debut=time.time()
        res=f(*args, **kwargs)
        fin=time.time()
        print("Temps d'execution:", fin-debut, "secondes")
        print("Nombre de parametres transmis:", len(args))
        return res
    return wrapper


@decorateur_analyseur
def analyser(*nums, arrondi=False, func=None, **options):

    if len(nums)==0:
        raise ValueError("Aucun nombre n'est passe")
    nums=list(nums)

    if options.get("unique",False):
        nums=list(dict.fromkeys(nums))

    if options.get("strict_positive",False):
        for n in nums:
            if n<=0:
                raise ValueError("Nombre <= 0 detecte")

    if func is not None:
        nums=[func(x) for x in nums]
    resultat={}

    if options.get("somme",False):
        resultat["somme"]=sum(nums)
    if options.get("moyenne",False):
        resultat["moyenne"]=sum(nums)/len(nums)
    if options.get("tri",False):
        resultat["tri"]=sorted(nums)
    return resultat
