<h1 align="center"> Progetto IPCV </h1>

### Obiettivi

Il progetto consiste nel creare un'applicazione in grado di rilevare i gesti della mano e dell'occhio per controllare un
media player (nel caso in esame utilizzeremo VLC). Riguardo il face detection, si andra’ a “catturare” il momento in cui
una gesture viene eseguita per un certo intervallo di tempo e verra’ di conseguenza collegato ad un comando da eseguire.
Per evitare di impartire erroneamente dei comandi, valuteremo se abilitare una particolare ROI dove le gesture verranno
interpretate. In alternativa si potrebbero utilizzare entrambe le mani per confermare la volonta’ di abilitare
l’handtracking oppure gesti specifici da anticipare il comando.

I principali comandi che abbiamo pensato di introdurre sono i seguenti:

- il video si mette in pausa se si esce dall'inquadratura della camera per un tot di secondi oppure se si chiudono
  entrambi gli occhi
- regolazione del volume in base alla distanza tra pollice e indice
- disattivare l'audio con mano "come segnale di stop" e riattivazione con mano aperta
- pausa gestita dall'utente mediante apertura/chiusura della mano
- regolazione velocità di riproduzione tramite swipe a sinistra/destra con più di un dito
- avanzamento veloce (+- 10s) tramite swipe a sinistra/destra con un dito

### Tools utilizzati

OpenCV

### Possibili estensioni

- Collegare l'applicazione ad un dispositivo in grado di emettere vibrazioni: utile nel caso in cui l'utente fosse sia
  cieco che sordo.
 
  
  
