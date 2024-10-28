.. admin_Metadata_index:

.. _Wet open overheid: https://wetten.overheid.nl/BWBR0045754/
.. _Woo-index: https://open.overheid.nl/
.. _DiWoo: https://standaarden.overheid.nl/diwoo/metadata
.. _Woo informatiecategorieën: https://standaarden.overheid.nl/tooi/waardelijsten/work?work_uri=https%3A%2F%2Fidentifier.overheid.nl%2Ftooi%2Fset%2Fscw_woo_informatiecategorieen
.. _Thema-indeling voor Officiële Publicaties (TOP-lijst): https://standaarden.overheid.nl/tooi/waardelijsten/work?work_uri=https%3A%2F%2Fidentifier.overheid.nl%2Ftooi%2Fset%2Fscw_toplijst

Metadata
========

Onder het menu-item "Metadata" en op het dashboard onder het kopje "Metadata" wordt toegang geboden tot het beheer van:

* Informatiecategorieën
* Thema's

Door hierop te klikken wordt het desbetreffende beheerscherm geopend.

Informatiecategorieën
---------------------

Toelichting
~~~~~~~~~~~

De `Wet open overheid`_ beschrijft 17 *informatiecategorieën*. Documenten die onder minstens één van deze categorieën vallen, moeten *actief* openbaar gemaakt worden. Dat wil zeggen dat een bestuursorgaan deze online moet publiceren, ook wanneer daar niet door een burger expliciet om gevraagd is in een *Woo-verzoek*. 

Daarnaast vraagt de wet om ook documenten openbaar te maken die buiten deze *informatiecategorieën* vallen. Hiervoor geldt geen "harde" plicht, maar wel een *inspanningsverplichting*.

Overigens gelden op de plicht tot openbaarmaking ook een aantal uitzonderingen (hoofdstuk 5 van de wet). Raadpleeg voor meer informatie over de wet de jurist en/of informatiebeheerder van je eigen organisatie.

Voor de aansluiting op de landelijke `Woo-index`_ wordt ten zeerste geadviseerd om documenten te voorzien van metadata conform de `DiWoo`_-standaard. Deze standaard vereist onder meer dat in de metadata wordt vastgelegd op grond van welke *informatiecategorie(ën)* het document actief openbaar is gemaakt.

De 17 *informatiecategorieën* zijn opgenomen in de landelijke waardelijst `Woo informatiecatgeorieën`_. Deze lijst is al standaard opgenomen in het "Woo Publicaties"-component. Daarnaast bestaat de mogelijkheid, zoals we hieronder zullen beschrijven, om in het kader van de *inspanningsverplichting* hier voor de eigen organisatie *extra informatiecategorieën* aan toe te voegen.

In het "WOO Publicaties"-component leggen we de *informatiecategorieën* vast op de *publicatie* (in ontwikkeling). Dezelfde *informatiecategorieën* gelden voor de daaraan gekoppelde *documenten*.

Beheerscherm
~~~~~~~~~~~~

In het beheerscherm van de *informatiecatgeorieën* wordt een lijst getoond van alle *informatiecategorieën* die zijn opgeslagen in het "WOO Publicaties"-component. 

Standaard staan de landelijke 17 verplichte *informatiecategorieën* hier al in. Zij zijn te herkennen aan de waarde "Waardelijst" in de kolom `Oorsprong` van de lijst. Zij kunnen niet gewijzigd worden.
Daarnaast bestaat er de mogelijkheid om voor de eigen organisatie *extra informatiecategorieën* toe te voegen. Deze zijn te herkennen aan de waarde "Zelf-toegevoegd item" in de kolom `Oorsprong` van de lijst. Deze kunnen indien nodig gewijzigd worden.

Op het beheerscherm zijn de volgende acties mogelijk:

* Rechtboven zit een knop **informatiecategorie toevoegen** waarmee een *informatiecategorie* toegevoegd kan worden.
* Bovenaan zit een zoekveld met en knop **"Zoeken"** waarmee naar *informatiecategorieën* gezocht kan worden.
* Daaronder zit de mogelijkheid om **eenzelfde actie uit te voeren over meerdere informatiecategorieën**. Op dit moment wordt alleen de actie **"Geselecteerde informatiecategorieën verwijderen"** ondersteund. Merk op dat het mogelijk is om in de lijst één of meerdere *informatiecategorieën* aan te vinken.
* Onder de (bulk-)actie staat de lijst met *informatiecategorieën*. Door op de kolomtitels te klikken kan de lijst **alfabetisch of chronologisch geordend** worden. 
* Rechts naast de lijst bestaat de mogelijkheid om deze te **filteren op oorsprong**.
* Bij een *informatiecategorie* kan op de `naam` geklikt worden om **de details in te zien** en deze eventueel **te wijzigen**.
* Bij een *informatiecategorie* kan op **"Show logs"** (op één na rechter kolom) geklikt worden om direct de :ref:`audit trail <admin_logging_index>` in te zien.

Wanneer bij een *informatiecategorie* op  de `naam` wordt geklikt, wordt een scherm geopend met nadere details.
Hierop zien we:

* **Alle gegevens**. Deze lichten we hieronder toe.
* Rechtsboven een knop **"Show logs"**. Deze toont de volledige `audittrail`_ van de *informatiecategorie*.
* Rechtsboven een knop **"Geschiedenis"**. Deze toont de beheer-handelingen die vanuit de beheerinterface zijn uitgevoerd op de *informatiecategorie*.
* Als de *informatiecategorie* tot de landelijke lijst behoort, linksonder een knop om het scherm te **sluiten** en terug te keren naar de lijst.
* Als de *informatiecatgeorie* door de organisatie zelf is toegevoegd, linksonder de mogelijkheid om **wijzigingen op te slaan** (indien van toepassing). Er kan voor gekozen worden om na het opslaan direct een nieuwe *informatiecategorie* aan te maken of om direct de huidige *informatiecategorie* nogmaals te wijzigen.
* Rechtsonder de mogelijkheid om de *informatiecategorie* te **verwijderen**.

Op een informatiecategorie zijn de volgende gegevens beschikbaar. Op het scherm wordt verplichte velden **dikgedrukt** weergegeven.

Naam
    De naam van de *informatiecategorie*, bijvoorbeeld "convenant".

Naam meervoud
    De meervoudsvorm van de naam, bijvoorbeeld "convenanten".

Definitie
    De (mogelijk landelijke) definitie van de *informatiecategorie*.

UUID
    Een niet-wijzigbaar, automatisch toegekend identificatiekenmerk.

Oorsprong
    Een niet-wijzigbaar, automatisch toegekende aanduiding van op welke wijze de *informatiecategorie* is toegevoegd; via de landelijke waardelijst of zelf toegevoegd.

Thema's
--------

Toelichting
~~~~~~~~~~~~~
Om de vindbaarheid van openbare documenten te bevorderen ondersteunt de `DiWoo`_-standaard het toekennen van een of meerdere *thema's* aan openbare documenten. Hiervoor is een landelijke waardelijst gedefinieerd: `Thema-indeling voor Officiële Publicaties (TOP-lijst)`_. Op de `Woo-index`_ kan een burger zoeken naar openbare documenten, die aan een bepaald thema gekoppeld zijn.

De landelijke thema-lijst is ook standaard ingelezen in en wordt ontsloten met het "Woo-publications"-component, zodat deze gebruikt kan worden bij het registreren en vindbaar maken van openbare documenten.

In het "WOO Publicaties"-component leggen we de *thema's* vast op de *publicatie* (in ontwikkeling). Dezelfde *thema's* gelden voor de daaraan gekoppelde *documenten*.

De `DiWoo`_-standaard ondersteunt alleen het gebruik van de landelijke waardelijst `Thema-indeling voor Officiële Publicaties (TOP-lijst)`_. Ook op de `Woo-index`_ kan alleen op deze *thema's*  gezocht worden naar openbare documenten.

Beheerscherm
~~~~~~~~~~~~

In het beheerscherm van de *thema's* wordt een lijst getoond van alle thema's die zijn opgeslagen in het "WOO Publications"-component. Standaard staan de landelijke thema's hier al in. 

Op het beheerscherm zijn de volgende acties mogelijk:

* Bovenaan zit een zoekveld met en knop **"Zoeken"** waarmee naar *thema's* gezocht kan worden.
* Daaronder zit de mogelijkheid om **eenzelfde actie uit te voeren over meerdere informatiecategorieën**. Op dit moment wordt alleen de actie **"Geselecteerde thema's verwijderen"** ondersteund. Merk op dat het mogelijk is om in de lijst één of meerdere *thema's* aan te vinken.
* Onder de (bulk-)actie staat de lijst met *thema's*. 
* Bij een *thema* kan op de `naam` geklikt worden om **de details in te zien**.
* Bij een *thema* kan op **"Show logs"** (rechter kolom) geklikt worden om direct de `audittrail`_ in te zien.

Wanneer bij een *thema* op  de `naam` wordt geklikt, wordt een scherm geopend met nadere details.
Hierop zien we:

* **Alle gegevens**. Deze lichten we hieronder toe.
* Rechtsboven een knop **"Show logs"**. Deze toont de volledige `audittrail`_ van het *thema*.
* Rechtsboven een knop **"Geschiedenis"**. Deze toont de beheer-handelingen die vanuit de Admin-interface zijn uitgevoerd op het *thema*.
* Linksonder een knop om het scherm te **sluiten** en teurg te keren naar de lijst.
* Rechtsonder de mogelijkheid om het *thema* te **verwijderen**.

Op een *thema* zijn de volgende gegevens beschikbaar.

* ``UUID``. Een niet-wijzigbaar, automatisch toegekend identificatie kenmerk.
* ``Naam``. De naam van het *thema*, bijvoorbeeld "cultuur en recreatie".
* ``position``. (In ontwikkeling)
* ``ref node id``. (In ontwikkeling)
