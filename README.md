# Telekommunikációs hálozatok tárgy

- TCP, UDP kommunikáció
- Különböző fájlok, adatok küldése szerver és kliens között
- Szerver, kliens írása
    - Közvetítő szerveres példák
## Beadando 3:
Barkóba
Készítsünk egy barkóba alkalmazást. A szerver legyen képes kiszolgálni több klienst. A szerver válasszon egy egész számot 1..100 között véletlenszerűen. A kliensek próbálják kitalálni a számot.

    A kliens logaritmikus keresés segítségével találja ki a gondolt számot. AZAZ a kliens NE a standard inputról dolgozzon.
    Ha egy kliens kitalálta a számot, akkor a szerver minden újabb kliens üzenetre a "Vége" (V) üzenetet küldi, amire a kliensek kilépnek.
    Nyertél (Y), Kiestél (K) és Vége (V) üzenet fogadása esetén a kliens bontja a kapcsolatot és terminál. Igen (I) / Nem (N) esetén folytatja a kérdezgetést.
    A kommunikációhoz TCP-t használjunk!
    A server a SELECT fv-t használja több kliens kiszolgálásához!!!!!
    Ha a játék végetért, akkor minden kérésre a szerver válaszoljon, hogy "Vége" (V).

Üzenet formátum:

    Klienstől: bináris formában egy db karakter, 32 bites egész szám. (struct) Ne használjuk a byte sorrend módosító operátort a struct-ban! ('!')
        A karakter lehet: <: kisebb-e, >: nagyobb-e, =: egyenlő-e
        pl: ('>',10) //a szám nagyobb mint 10
    Szervertől: ugyanaz a bináris formátum , de a számnak nincs szerepe, bármi lehet (struct)
        A karakter lehet: I: Igen, N: Nem, K: Kiestél, Y: Nyertél, V: Vége
        pl: ('V',0)


Script paraméterezése:

    python3 client.py < hostname > < port szám >
        pl: python3 client.py localhost 10000
    python3 server.py < hostname > < port szám >
        pl: python3 server.py localhost 10000

## Beadando 4:
NetCopy
Készíts egy netcopy kliens/szerver alkalmazást, mely egy fájl átvitelét és az átvitt adat ellenőrzését teszi lehetővé CRC vagy MD5 ellenőrzőösszeg segítségével! A feladat során három komponenst/programot kell elkészíteni:

1. Checksum szerver: (fájl azonosító, checksum hossz, checksum, lejárat (mp-ben)) négyesek tárolását és lekérdezését teszi lehetővé. A protokoll részletei lásd lejjebb.
2. Netcopy kliens: egy parancssori argumentumban megadott fájlt átküld a szervernek. Az átvitel során/végén kiszámol egy md5 checksumot a fájlra, majd ezt feltölti fájl azonosítóval együtt a Checksum szerverre. A lejárati idő 60 mp. A fájl azonosító egy egész szám, amit szintén parancssori argumentumban kell megadni.
3. Netcopy szerver: Vár, hogy egy kliens csatlakozzon. Csatlakozás után fogadja az átvitt bájtokat és azokat elhelyezi a parancssori argumentumban megadott fájlba. A végén lekéri a Checksum szervertől a fájl azonosítóhoz tartozó md5 checksumot és ellenőrzi az átvitt fájl helyességét, melynek eredményét stdoutputra is kiírja. A fájl azonosító itt is parancssori argumentum kell legyen.
Checksum server

    Beszúr üzenet
        Formátum: szöveges
        Felépítése: BE|< fájl azon. >|< érvényesség másodpercben >|< checksum hossza bájtszámban >|< checksum bájtjai >
        A „|” delimiter karakter
        Példa: BE|1237671|60|12|abcdefabcdef
            Ez esetben: a fájlazon: 1237671, 60mp az érvényességi idő, 12 bájt a checksum, abcdefabcdef maga a checksum
            Válasz üzenet: OK
    Kivesz üzenet
        Formátum: szöveges
        Felépítése: KI|< fájl azon. >
        A „|” delimiter karakter
        Példa: KI|1237671
            Azaz kérjük az 1237671 fájl azonosítóhoz tartozó checksum-ot
            Válasz üzenet: < checksum hossza bájtszámban >|< checksum bájtjai >
            Példa: 12|abcdefabcdef
        Ha nincs checksum, akkor ezt küldi: 0|
    Futtatás
        python3 checksum_srv.py < ip > < port >
            < ip > - pl. localhost a szerver címe bindolásnál
            < port > - ezen a porton lesz elérhető
        A szerver végtelen ciklusban fut és egyszerre több klienst is ki tud szolgálni. A kommunikáció TCP, csak a fenti üzeneteket kezeli.
        Lejárat utáni checksumok törlődnek, de elég ha csak a következő kérésnél ellenőrzöd.

NetCopy kliens

    Működés:
        Csatlakozik a szerverhez, aminek a címét és portját parancssori argumentumban kapja meg.
        Fájl bájtjainak sorfolytonos átvitele a szervernek.
        A Checksum szerverrel az ott leírt módon kommunikál.
        A fájl átvitele és a checksum elhelyezése után bontja a kapcsolatot és terminál.
    Futtatás:
        python3 netcopy_cli.py < srv_ip > < srv_port > < chsum_srv_ip > < chsum_srv_port > < fájl azon > < fájlnév elérési úttal >
        < fájl azon >: egész szám
        < srv_ip > < srv_port >: a netcopy szerver elérhetősége
        < chsum_srv_ip > < chsum_srv_port >: a Checksum szerver elérhetősége

NetCopy Server

    Működés:
        Bindolja a socketet a parancssori argumentumban megadott címre.
        Vár egy kliensre.
        Ha acceptálta, akkor fogadja a fájl bájtjait sorfolytonosan és kiírja a paracssori argumentumban megadott fájlba.
        Fájlvége jel olvasása esetén lezárja a kapcsolatot és utána ellenőrzi a fájlt a Checksum szerverrel.
        A Checksum szerverrel az ott leírt módon kommunikál.
        Hiba esetén a stdout-ra ki kell írni: CSUM CORRUPTED
        Helyes átvitel esetén az stdout-ra ki kell írni: CSUM OK
        Fájl fogadása és ellenőrzése után terminál a program.
    Futtatás:
        python3 netcopy_srv.py < srv_ip > < srv_port > < chsum_srv_ip > < chsum_srv_port > < fájl azon > < fájlnév elérési úttal >
            < fájl azon >: egész szám ua. mint a kliensnél – ez alapján kéri le a szervertől a checksumot
            < srv_ip > < srv_port >: a netcopy szerver elérhetősége – bindolásnál kell
            < chsum_srv_ip > < chsum_srv_port >: a Checksum szerver elérhetősége
            < fájlnév > : ide írja a kapott bájtokat
