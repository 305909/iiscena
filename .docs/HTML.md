# Guida HTML

##### by Francesco Giuseppe Gillio
###### I.I.S. G. Cena di Ivrea

HTML è il principale linguaggio di pubblicazione di pagine Web, oltre che uno strumento sempre più utilizzato per la realizzazione di contenuti e applicazioni mobile. Seguendo questa guida imparerai a realizzare pagine e siti in HTML, con immagini, link, tabelle, form di inserimento dati per gli utenti, e tanto altro ancora.

## Primi passi

- [Introduzione all'HTML](#introduzione-all'html)
- [Hello HTML! Creare la prima pagina](#hello-html!-creare-la-prima-pagina)

## Introduzione all'HTML

Con il markup si impostano la struttura di pagine Web come delle app Mobile. Qui una panoramica per entrare nello sfaccettato mondo dell'HTML.

HTML è l'acronimo di HyperText Markup Language ("Linguaggio di contrassegno per gli Ipertesti") e non è un linguaggio di programmazione. Si tratta invece di un linguaggio di markup (di 'contrassegno' o 'di marcatura'), che permette di indicare come disporre gli elementi all'interno di una pagina.

```python
<!doctype html>
<html>
    <head>
        <title>HMTL.it</title>
```

Queste indicazioni vengono date attraverso degli appositi marcatori, detti tag ('etichette'), che hanno la caratteristica di essere inclusi tra parentesi angolari (ad es, <img> è il segnaposto di un'immagine).

Con HTML quindi indichiamo, attraverso i tag, quali elementi dovranno apparire su uno schermo e come essi debbano essere disposti. Tutte queste indicazioni sono contenute in un documento HTML, spesso detto "Pagina HTML". Una pagina HTML è rappresentata da un file di testo, ovvero un file che possiamo modificare con programmi come notepad e in genere hanno un nome che finisce con l'estensione .html.

Ciò significa che HTML non possiede i costrutti propri della programmazione, come i meccanismi "condizionali", che consentono di reagire in modo diverso a seconda del verificarsi di una condizione ("in questa situazione fai questo, in quest'altra fai quest'altro"), o i costrutti iterativi ("ripeti questa azione, finché non succede questo").

Nota: Si parla in questo caso di linguaggio dichiarativo, che serve appunto ad indicare cosa deve apparire sullo schermo (testi, immagini, suoni, etc.), dove e in che sequenza. Nel caso di linguaggi in cui specifichiamo algoritmi precisi con "strutture di controllo", come C, C++, Java, o anche PHP e JavaScript, parliamo di "linguaggi imperativi".

#### HTML + CSS + JavaScript

Anche se non ce ne occuperemo direttamente, è utile sapere che per lavorare con HTML è utile conoscere tutto il cosiddetto "stack", ovvero tutte le tecnologie necessarie a realizzare un sito o una applicazione.

In passato si utilizzavano alcuni tag HTML per definire font (tipi di carattere), i colori o le dimensioni degli oggetti sullo schermo. Oggi il quadro è definitivamente cambiato e molte di quelle funzionalità sono deprecate favorendo una divisione dei compiti più chiara tra diversi strumenti:

- HTML serve a definire quali sono gli elementi in gioco, stabilire collegamenti (link) tra le pagine e l'importanza (non la forma o il colore) che hanno i testi, creare form per gli utenti, fissare titoli, caricare immagini, video, etc.
- CSS o "fogli di stile". Si tratta di una serie di regole che permettono di definire l'aspetto (lo stile) che devono assumere gli elementi sulla pagina. Dimensioni, colori, animazioni, ogni caratteristica visuale può essere manipolata.
- JavaScript è un linguaggio di programmazione che consente di manipolare veramente qualunque cosa nella pagina HTML: lo stile, i contenuti della pagina, ma soprattutto l'interazione con l'utente. Ci permette di creare la logica dell'interfaccia utente (o anche di una applicazione) e di sfruttare le API messe a disposizione dal browser: dalla gestione del mouse al touch, dalla manipolazione delle immagini, alle richieste di dati dinamiche (in modalità Ajax) alla gestione di dati in locale (grazie ai LocalStorage).

In questa guida approfondiremo tutto ciò che riguarda il potenziale messo a disposizione da HTML ma faremo riferimento spesso anche a queste altre tecnologie, legate a doppio filo con il nostro markup.

####  HTML è uno standard: il W3C

Da quando Tim Berners Lee, nel 1991, ha definito la prima versione del linguaggio, fino ai giorni nostri, HTML ha continuato ad evolversi fino a maturare nello standard HTML 5.

Il secondo rilascio delle specifiche (HTML 2) è stato pubblicato dallo IEFT nel 1995, mentre già stava nascendo il W3C: World Wide Web Consortium l'organizzazione fondata dallo stesso Berners Lee con CERN e MIT, che oggi vede coinvolti numerosi istituti universitari e i più importanti attori tecnologici sulla scena mondiale come Apple, Microsoft, Google, Facebook, IBM, Adobe, e moltissimi altri.

Il W3C si occuperà di traghettare lo standard attraverso la versione 3.2 (1997) fino alla definizione di HTML 4 nel 1998 e HTML 4.01, la versione che ha sostenuto la crescita del Web di tutti gli anni 2000 e che assurgerà a standard ISO proprio a cavallo del terzo millennio.

Proprio negli anni 2000 nasce XHTML, un filone parallelo che cerca di dare maggior rigore all'HTML, definendolo come "applicazione XML" ne sono già state rilasciate due versioni (XHTML1.0 e XHTML1.1), molto simili a HTML 4.1, poi praticamente abbandonate già nel 2011 quando il W3C decide di affermare lo standard HTML 5 (tutt'ora sussiste una definizione di XHTML5.1 nella bozza delle specifiche HTMl5).

#### HTML5, Web e mobile

La versione di HTML che esamineremo in questa guida è quella più attuale: HTML 5, che è anche la versione che nasce appositamente per uscire dal solo ambito Web e diventare piattaforma per la creazione di applicazioni, anche desktop e mobile.

La specifica HTML5 infatti si compone della definizione di:

- una sintassi per il markup più efficace e adatta alle esigenze più moderne, con l'introduzione di specifici controlli per i form o degli attributi "data-" da arricchire i tag di informazioni specifiche;
- una serie di API che consentono di gestire, a livello approfondito aspetti come network, multimedia, e hardware dei dispositivi. In altre parole dalla gestione del video e dell'audio al monitoraggio delle batterie di un device.

Questo sviluppo dello standard ha dato il via alla generazione delle cosiddette App mobile ibride, che sfruttano sia HTML5, per creare app che si possono distribuire, come quelle native, sui marketplace dei dispositivi più comuni (come Google Play per Android ad esempio).

#### Link e ipertesti

La potenza di Internet consiste nell'essere un insieme esteso di contenuti connessi tra loro. Il linguaggio HTML e i link sono alla base di questo meccanismo che consente di muoversi rapidamente tra testi, immagini, video, applicazioni e quant'altro creando percorsi i propri percorsi di navigazione in totale autonomia.

Per accedere rapidamente a una ormai enorme mole di informazioni, sono nati i motori di ricerca, che si basano su una serie di elementi "semantici" per rispondere adeguatamente alle richieste degli utenti. Si parte dall'analisi del testo (o del contenuto) e dei collegamenti, fino a sfruttare i comportamenti degli utenti per catalogare le pagine e stabilire il livello di rilevanza (ranking) che hanno a seconda della singola query di ricerca.

L'ottimizzazione dei contenuti per favorire il posizionamento della pagina per specifiche ricerche si dice SEO (Search Engine Optimization), nel corso della guida ci troveremo a parlarne ancora.

## Hello HTML! Creare la prima pagina
