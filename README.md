# Model-Selection-for-Speech-Recognition
Il proggetto consiste in un programma ROS che sfrutta le Google API Speech-to-Text per creare un riconoscitore vocale per il controllo vocale di un turtle bot (simulato con turtlesim). In oltre vengono utilizzate tre metodologie diverse per il controllo dell'errore:
 1. Senza gestione dell' errore: se la parola non viene riconosciuta essattamente non viene attivato il commando ;
 2. Gestione dell'errore attraverso un algoritmo di programmazione dinamica che calcola la distanza tra due stringhe;
 3. Gestion dell'errore attraverso un modello Naive Bayes creato attraverso un mini dataset (tale modello di gestione è stato creato con sensidbilità 54% ma non è stato ancora connesso a ROS e non è ancora accessibile per essere usato)
