.. _admin_logging_index:

Logging
=======

Onder het menu-item "Logging" en op het dashboard onder het kopje "Logging" wordt toegang geboden tot het beheer van:

* (audit)logitems
* Access attempts
* Access failures
* Access logs
* Uitgaande request-logs

Door hierop te klikken wordt het desbetreffende beheerscherm geopend.

(audit)logitems
---------------
Hier wordt de logging getoond van:

* Publicaties
* Documenten
* Informatiecategorieën
* Organisaties
* Thema's
* Gebruikers (alleen degene die direct toegang hebben tot dit component)

Daarop worden de volgende handelingen gelogd. 

* Nieuwe records (create)
* Raadplegingen van records (read)
* Downloaden van bestanden (bij _documenten_)
* Wijzigingen van records (update / patch)
* Verwijdering / vernietiging van records (delete)

Zowel handelingen uitgevoerd via de admin-interface als via de API worden gelogd.

Op het beheerscherm zijn de volgende acties mogelijk:

* Bovenaan zit een zoekveld met en knop **Zoeken** waarmee naar *(audit)logitems* gezocht kan worden.
* Onder de (bulk-)actie staat de lijst met *(audit)logitems*. Door op de kolomtitels (m.u.v. de kolom `bericht`) te klikken kan de lijst **alfabetisch of chronologisch geordend** worden. 
* Rechts naast de lijst bestaat de mogelijkheid om deze te **filteren op datum en/of gebeurtenis**.
* Bij een *(audit)logitem* kan op het `bericht` geklikt worden om **de details in te zien**. Daarbij worden o.a. de gegevens getoond van het betrokken object zoals bekend direct ná de handeling.
* Bij een *(audit)logitem* kan op het **betrokken object** (rechter kolom) geklikt worden om direct naar het record te gaan waar het *(audit)logitem* betrekking op heeft.

Access attempts
---------------

...

Access failures
---------------

...

Access logs
-----------

...

Uitgaande request-logs
----------------------

...
