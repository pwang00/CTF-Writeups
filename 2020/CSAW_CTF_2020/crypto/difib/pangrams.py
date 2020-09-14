from sympy.crypto.crypto import decipher_bifid5
alphabet = set(__import__("string").ascii_letters[:26])
pangrams = ['mrjocktvquizphdbagsfewlynx', 'jocknymphswaqfdrugvexblitz', 'crwthvoxzapsqigymfjeldbunk', 'hmfjordwaltzcinqbuskpyxveg', 'phavfyxbugstonqmilkjzdcrew', 'hesaidbcfgjklmnopqrtuvwxyz', 'jenqvahlbidgumkrwcfpostxyz', 'emilyqjungschwarzkopfxtvbd', 'johnfezcamrwsputyxigkqblvd', 'qtipforsuvnzxylemdcbaghwjk', 'jumblingvextfrowzyhackspdq', 'jqvandzstruckmybigfoxwhelp', 'lumpydrabcgqvzjinksfoxthew', 'heyiamnopqrstuvwxzbcdfgjkl', 'quizjvbmwlynxstockderpaghf', 'pledbigczarjunksmyvwfoxthq', 'waltzgbquickfjordsvexnymph', 'qwertyuioplkjhgfdsazxcvbnm', 'zyxwvutsrqponmlkjihgfedcba', 'aquickbrownfxjmpsvethlzydg']

res = "snbwmuotwodwvcywfgmruotoozaiwghlabvuzmfobhtywftopmtawyhifqgtsiowetrksrzgrztkfctxnrswnhxshylyehtatssukfvsnztyzlopsv"

if __name__ == "__main__":

    for i in alphabet:
        
        for key in pangrams[::-1]:
            res = decipher_bifid5(res, key.replace(i, ""))

        print(res)
