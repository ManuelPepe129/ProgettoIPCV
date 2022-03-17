#Relazione Computer Vision

##1) Introduzione
Negli ultimi anni la necessità di applicazioni accessibili ad un numero
sempre maggiore di persone ha portato allo sviluppo di nuove forme 
di interazioni che si inseriscono in un quadro di sviluppo molto ampio
denominato "interazione multimodale". L’intento di questo progetto è 
quello di sfruttare l’image processing e la computer vision al fine di 
realizzare un’applicazione che riconosca i gesti di un utente per 
controllare un’applicazione multimediale senza l'utilizzo di dispositivi come 
mouse o tastiera. In concreto, attraverso 
l’utilizzo di una semplice webcam sul proprio computer si può controllare
la riproduzione multimediale di un video. L’applicazione multimediale di riferimento 
è VLC e le funzionalità, che verranno illustrate in seguito, spaziano 
dall’interruzione della riproduzione quando il volto dell’utente non è più
rilevato all’interno dello spazio di visualizzazione della webcam 
fino alla modifica del volume attraverso l’utilizzo della mano.
Nei prossimi capitoli verranno illustrati a fondo gli obiettivi prefissati,
le funzionalità principali che si è deciso di implementare,
i requisiti e infine l’implementazione vera e propria con tutte
le scelte effettuate.

##2) Obiettivi
Partendo da quello che volevamo fosse il risultato finale del nostro progetto,
ovvero un’applicazione che permettesse ad un utente di controllare un video 
riprodotto su VLC attraverso delle “gestures” effettuate all’interno del campo
 di visualizzazione della webcam (frame) abbiamo definito i seguenti macro 
 obiettivi per raggiungere il nostro scopo, ai quali successivamente si sono 
 aggiunti ulteriori micro obiettivi che vedremo meglio nella fase di implementazione:
* **Riconoscimento del volto:** in primo luogo abbiamo ritenuto necessario il 
riconoscimento della forma del volto (frontale) all’interno di ogni frame video,
in ogni momento, in quanto una delle funzionalità che si è deciso di implementare
riguarda l’interruzione automatica del video qualora il volto dell’utente non
venga rilevato. Questo perché si è immaginato che un’applicazione del genere debba
tenere conto del comportamento dell’utente e debba reagire di conseguenza, 
anche se l’utente non ha impartito esplicitamente alcun comando: se l’utente 
è distratto o improvvisamente qualcuno entra nella sua stanza e si gira per 
comunicare, il video si interrompe e riprenderà una volta che l’utente sarà di 
nuovo disponibile. 
* **Riconoscimento degli occhi:** successivamente abbiamo ritenuto necessario 
il riconoscimento della posizione degli occhi e la loro apertura o chiusura 
in quanto qualora l’utente fosse stanco e chiudesse gli occhi il video non avrebbe
motivo di proseguire nella sua riproduzione.
* **Riconoscimento della mano:** infine abbiamo ritenuto necessario il riconoscimento
della mano, in quanto strumento attivo dell’interazione tra utente e sistema.
Ed in particolare, oltre al riconoscimento della forma completa della mano al fine
di permettere all’utente di mettere in pausa la riproduzione e riavviarla (tramite
una gesture che verrà illustrata in seguito), abbiamo ritenuto necessario 
individuare le dita per sviluppare un meccanismo di controllo del volume di 
riproduzione. 

#3) Requisiti
Oltre a disporre di una webcam, che costituisce un requisito fondamentale per 
il funzionamento dell’applicazione, è necessario che l’utente sia all’interno 
di una stanza adeguatamente illuminata evitando una fonte di illuminazione alle
spalle, ma piuttosto favorendone una frontale che permetta di avere un giusto 
livello di contrasto tra l’utente e lo sfondo. E’ inoltre necessario che l’utente
sia ben inserito all’interno del frame, ad una distanza di circa mezzo metro 
dallo schermo. Infine è necessario che l’utente abbia una mano libera per poter 
effettuare le gestures di controllo della riproduzione video e del volume. 

#4) Implementazione

Nella prima parte dello sviluppo dell’applicazione ci siamo occupati del riconoscimento
del volto e degli occhi e per fare ciò abbiamo utilizzato due classificatori di tipo 
Haar Cascade. A fronte di un’equalizzazione di ogni singolo frame per fornire al 
classificatore delle immagini classificabili con maggiore semplicità, il meccanismo di
controllo del player video è molto semplice. Se il volto viene rilevato e gli occhi sono
aperti allora la riproduzione prosegue normalmente, altrimenti, se gli occhi (aperti) 
o l’intero viso non vengono rilevati per un tot di secondi, viene chiamata la funzione
`player.pause()` e il player viene appunto messo in pausa. Il video viene automaticamente
fatto ripartire quando vengono rilevati il volto e gli occhi aperti con la funzione 
`player.play()`.
Il numero di secondi di attesa prima che il video venga messo in pausa, qualora non 
vengano rilevati gli elementi descritti, è stato stabilito facendo alcune considerazioni
ed effettuando delle prove. Da una parte abbiamo considerato alcuni comportamenti comuni
degli utenti e alcuni fattori di distrazione, come ad esempio guardare le notifiche del
telefono, guardare l’orologio o semplicemente dare un’occhiata all’ambiente circostante.
Per questo motivo abbiamo ritenuto che un applicazione che rispondesse immediatamente 
alla non rilevazione degli elementi discussi precedentemente fosse sgradevole per 
l’utente e piuttosto abbiamo preferito un’applicazione flessibile. Dall’altra parte
abbiamo considerato i limiti dei classificatori utilizzati e dell’ambiente in cui 
l’utente è inserito e, di conseguenza, la possibilità che per una breve sequenza di
frame gli elementi necessari alla riproduzione del video non vengano individuati 
correttamente nonostante siano presenti. 


Nella seconda parte dello sviluppo ci siamo occupati dell’individuazione della mano 
al fine di controllare, attraverso delle gestures, ulteriori funzionalità della 
riproduzione video come il volume, oltre alle funzionalità di play/pausa viste 
precedentemente. Per fare questo abbiamo inizialmente testato vari classificatori 
per poi renderci conto che avevamo bisogno di uno strumento più stabile, che ci 
permettesse di fare alcuni calcoli calcoli di distanza in maniera accurata. 
Abbiamo infine ritenuto che la soluzione più adatta al nostro bisogno fosse la 
libreria Mediapipe per il riconoscimento della mano. E’ uno strumento molto potente 
ed affidabile che fornisce 21 coordinate dell’articolazione della mano e sostanzialmente
costituisce una buona base su cui poter lavorare per lo sviluppo delle features. Una 
volta superato lo scoglio della ricerca di uno strumento affidabile abbiamo pensato di
creare una finestra di controllo, si dimensioni ridotte all’interno del frame, 
che fosse una zona in cui l’utente potesse operare con la propria mano. Al di fuori 
di questa zona tutti i comandi impartiti non vengono elaborati dal sistema. (perchè 
lo abbiamo fatto ?). Grazie all’individuazione di coordinate dell’articolazione della
mano abbiamo poi realizzato un meccanismo di controllo del volume basato sulla distanza
tra due dita. In particolare abbiamo considerato la distanza tra i punti 8 (Index_finger_tip) e 4 (thumb_tip) in figura, ovvero tra la punta del pollice e la punta dell’indice. L’utente può quindi aumentare o diminuire il volume della riproduzione facendo variare la distanza tra le punte di queste due dita e successivamente lasciando la finestra di controllo.
Per effettuare questa operazione è però importante che la mano sia interamente 
contenuta all’interno della finestra di controllo, nel pratico, verifichiamo che 
le coordinate di tutti i 21 punti dell’articolazione della mano siano all’interno 
della finestra. Qualora un punto sia fuori dalla finestra l’operazione di modifica 
del volume non viene fatta partire oppure viene interrotta e l’ultimo valore fornito 
al sistema viene salvato. Questo semplice meccanismo permette all’utente di salvare il
valore desiderato semplicemente muovendo la mano in una qualsiasi direzione (uscendo 
dalla finestra). 
Per stabile la percentuale di volume abbiamo definito una distanza massima e minima,
maggiori di zero, tra i due punti di cui abbiamo parlato. Inoltre abbiamo normalizzato
questa distanza attraverso un’altra distanza che rimane sempre costante all’interno 
della mano, ovvero quella tra il punto 0 (Wrist) e il punto 17 (pinky_mcp), metacarpo
del mignolo. In questo modo il calcolo del volume non è suscettibile alla distanza 
dalla video camera, ma mantenendo le dita alla stessa distanza e allantonandoci dalla
webcam il valore percentuale di volume rimane quasi costante. 
Infine abbiamo introdotto una barra all’interno dell’interfaccia che mostra in tempo
reale la percentuale di volume corrispondente alla gesture, favorendone l’usabilità. 

###Manca l’ultima gesture, blocco della riproduzione con la mano

#5) Tecnologie utilizzate 
   * **MediaPipe:** è una libreria multipiattaforma sviluppata da google che fornisce soluzioni
di machine learning pronte all'utilizzo nell'ambito della computer vision. Nel nostro progetto
è stato utilizzato per il riconoscimento della mano e delle dita grazie ad operazioni di machine
learning che permettono di rilevare per ogni singolo frame 21 punti di riferimento 3D all'interno
della mano.

   * **OpenCv:** 

   * **Classificatore Haar**:


#6) Validazione funzionale 

#7) Conclusioni e sviluppi futuri
Pur essendo consapevoli di alcuni limiti dell'applicazione ci riteniamo
complessivamente soddisfatti del lavoro svolto in quando l'utente è in grado,
seguendo dei requisiti minimi di utilizzo, di eseguire le operazioni di controllo
con estrema semplicità. Un possibile sviluppo futuro sarebbe quello di sviluppare
un'interfaccia utente che si attivi ogni volta che il sistema riconosce che l'utente
sta impartendo un comando al sistema e mostri graficamente l'effetto di questi comandi
con elementi grafici, così da restituire un'azione di feedback all'utente. Al dì
fuori di questi momenti di controllo l'interfaccia rimane ridotta ad icona e non
interferisce con la visione del video. Inoltre sarebbe interessante aumentare il numero
di gestures che l'utente può effettuare andando a mappare tutte le azioni possibili
di controllo del riproduttore video, come il controllo della velocità di riproduzione
oppure l'aggiunta di sottotitoli. 




 