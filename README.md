# GetMusical
## door: Sadjia Safdari, Joran Verweij en Dennis de Buck

# Features:
### "/"
Geeft de index pagina terug.
- Dennis en Sadjia

### "/upload"
Laat gebruikers een video "uploaden". Gebruikers plaatsen eerst een video op youtube en geven daarna de "video id" aan ons door,
samen met de naam, welk instrument er wordt bespeeld en de moeilijkheidsgraad.
- Dennis

### "/like" en "/dislike"
Laat gebruikers een video liken of disliken. Er is met JavaScript voor gezorgd dat wanneer een video wordt geliket, de
like button verandert in een dislike button, om duplicatie te voorkomen. Voegt likes toe aan user database voor berekening van skill level.
- Joran en Dennis

### "/follow" en "/unfollow"
Laat gebruikers andere gebruikers volgen. Met JavaScipt wordt gezorgd dat de functionaliteit en de looks van de knop verandert,
wanneer er op wordt geklikt.
- Joran

### "/search"
Laat gebruikers zoeken naar andere gebruikers. Als er is ingelogd kun je niet naar jezelf zoeken. Wel kun je dan andere
gebruikers volgen of ontvolgen.
- Joran en Dennis

### "/login" en "/logout"
Zorgt dat gebruiker kan in- en uitloggen. De gebruiker krijgt een waarschuwing als er iets fout gaat en wordt tegengehouden.
- Joran

### "/profile"
Laat gebruiker eigen profielpagina zien. De gebruiker ziet zijn eigen video's, de gebruikers die hij volgt en zijn skill level,
welke berekend worden door middel van het aantal gehaalde likes per instrument.
- Dennis en Joran

### "/profileeditor"
Hier kan de je informatie over jezelf in je profiel updaten. Ook dit wordt weergeven in /profile.
- Joran

### "/register"
Laat gebruiker een account aanmaken voor de website, waarbij wordt aangegeven welke instrumenten hij/zij wilt leren. Deze worden
dan weergeven op profile pagina. Er wordt gecontroleerd of de gebruiker goede informatie invult en of de gebruikersnaam nog niet in gebruik is.
- Joran en Dennis

### "/instruments"
Laat gebruikers zoeken naar video's op instrument en moeilijkheidsgraad. Weergeeft alle geuploade video's per 4.
- Sadjia

### "/registercheck"
Kijkt of gebruikersnaam al bestaat.
- Joran

### "/usercheck"
Usercheck zorgt ervoor dat een gebruiker niet met de verkeerde gegevens kan inloggen. Je krijgt gelijk een melding als er iets verkeerd gaat.
- Joran

### "/video"
Weergeeft de youtube video's in een nieuw scherm, wanneer iemand op de knop "watch video" klikt. Op deze pagina kunnen gebruikers comments plaatsen onder een video.
Daarnaast is te zien hoeveel likes de video heeft. Ook kunnen gebruikers hun eigen comments verwijderen. Het plaatsen van comments gebeurt via JavaScript in video.html.
- Sadjia en Joran

### "/delete-comment"
Laat gebruikers hun eigen comments verwijderen. Wanneer gebruikers hun comments verwijderen, zien zij dat gelijk op de pagina zonder dat de pagina wordt gerefresht.
- Sadjia

## Helpers
We hebben een aantal functies in helpers gezet.

### apology
Geeft een foutmelding als er iets mis gaat.

### login_required
Zorgt ervoor dat de gebruiker ingelogd is.

### skill_counter
Kijkt voor elk instrument dat de gebruiker wilt leren, hoe hoog het skill level van de gebruiker is.
Bij 0 tot 11 likes, is de gebruiker beginner. 10 likes daarbovenop verandert gebruiker naar competent.
10 likes daarna wordt hij/zij proficient en bij 30 likes of meer is de gebruiker een expert.

### like en dislike_instrument
Zet een like bij, of haalt hem weg in users, als een gebruiker op de liketoets klikt.

![schets](doc/screenshot.jpg)
