TEST_CASE = [
    {
        "conversation_history": [
            {"role": "user", "content": "Sto sviluppando un'app RAG e ho un dubbio sulla pipeline di retrieval. Meglio BM25 o embeddings?"},
            {"role": "assistant", "content": "Dipende dal dominio. BM25 va meglio su contenuti lunghi e keyword-based, embeddings su semantica stretta."},
            {"role": "user", "content": "Il dominio è molto tecnico. Documenti brevi ma densi."},
            {"role": "assistant", "content": "Allora embeddings + reranking leggero è la scelta tipica."},
            {"role": "user", "content": "Ok. Altra cosa: devo salvare la cronologia chat ogni 10 messaggi per creare un sommario incrementale, giusto?"},
            {"role": "assistant", "content": "Corretto. Ogni 10 messaggi generi un sommario e lo usi come contesto compresso."},
            {"role": "user", "content": "Uso toon-format per ottimizzare i token. Va bene?"},
            {"role": "assistant", "content": "Perfetto. Toon-format riduce la verbosità della chat mantenendo la struttura logica."}
            ],
        "expected_summary": "L'utente sta sviluppando una webapp RAG. Sta scegliendo tra BM25 e embeddings e riceve il consiglio di usare embeddings con reranking. Ha bisogno di salvare la cronologia ogni 10 messaggi per generare un sommario ed è confermato che il toon-format è adeguato.",
    },
    {
        "conversation_history": [
            {"role": "user", "content": "Sto costruendo un braccialetto IoT con sensori biomedici. Devo decidere l'architettura edge-fog-cloud."},
            {"role": "assistant", "content": "Nel tuo caso l'edge sta sul bracciale, il fog è il telefono, e il cloud gestisce analisi pesanti."},
            {"role": "user", "content": "Il telefono farà da bridge BLE → MQTT per il digital twin. Ti torna?"},
            {"role": "assistant", "content": "Sì, ed è coerente con la pipeline di sincronizzazione. HTTP/REST lo tieni per i servizi lato utente."},
            {"role": "user", "content": "Mi serve anche valutare anomalie di movimento. Posso farlo sul cloud?"},
            {"role": "assistant", "content": "Sì, modelli di anomaly detection sono pesanti e meglio eseguirli lato cloud."}
            ],
        "expected_summary": "L'utente sta progettando un braccialetto IoT biomedicale. Clarifica l'architettura edge-fog-cloud, con il telefono come bridge BLE→MQTT. Il cloud gestisce sia servizi REST sia i modelli di anomaly detection."
    },
    {
        "conversation_history": [
            {"role": "user", "content": "Sto creando una pipeline ML per rilevare se un malato di Alzheimer si allontana da aree abituali."},
            {"role": "assistant", "content": "Usa clustering delle traiettorie e un modello di deviazione spaziale."},
            {"role": "user", "content": "E per andare in produzione?"},
            {"role": "assistant", "content": "Serve monitoring, retraining periodico e valutazione continua delle metriche."},
            {"role": "user", "content": "Mi servono riferimenti per la letteratura."},
            {"role": "assistant", "content": "Cerca articoli su human mobility modeling e anomaly detection per elderly care."}
            ],
        "expected_summary": "L'utente sta progettando una pipeline ML per rilevare deviazioni dalle traiettorie abituali di pazienti Alzheimer. Vengono suggeriti modelli basati su clustering e monitoraggio continuo, più riferimenti a letteratura su human mobility e elderly care."
    },
    {
        "conversation_history": [
            {"role": "user", "content": "Sto preparando un laboratorio di pentesting. Voglio simulare un attacco realisticamente controllato."},
            {"role": "assistant", "content": "Assicurati che l’ambiente sia isolato: rete virtuale separata e snapshot pronti."},
            {"role": "user", "content": "Voglio introdurre un attacco MITM. Meglio ARP spoofing o DNS spoofing?"},
            {"role": "assistant", "content": "ARP spoofing è più facile da dimostrare, DNS spoofing più didattico."},
            {"role": "user", "content": "Userò ARP allora. Mi serve loggare tutto per analisi RAG successiva."},
            {"role": "assistant", "content": "Ottimo: cattura pacchetti, log di autenticazione, e transcript delle sessioni."},
            {"role": "user", "content": "Sto anche creando prompt per classificare i log in base al tipo di minaccia."},
            {"role": "assistant", "content": "Puoi usare un LLM come classifier zero-shot, poi un reranker per maggiore precisione."},
            {"role": "user", "content": "Devo generare un sommario dell’attacco dopo ogni fase: scan, exploit, escalation."},
            {"role": "assistant", "content": "Strategia valida per mantenere un audit trail leggibile."},
            {"role": "user", "content": "Quanto è utile ridurre tutto in toon-format?"},
            {"role": "assistant", "content": "Molto per questo tipo di verbosità. Ti permette di comprimere sequenze lunghe senza perdere struttura."}
            ],
        "expected_summary": "L’utente sta preparando un laboratorio di pentesting isolato. Vuole simulare un MITM con ARP spoofing, loggare dati per analisi RAG, classificare log con LLM e generare sommari per ogni fase dell’attacco. Il toon-format viene consigliato per gestire la verbosità dei dati."
    },
    {
        "conversation_history": [
            {"role": "user", "content": "Sto studiando analisi di sequenziamento RNA-Seq. Non so se usare DESeq2 o edgeR."},
            {"role": "assistant", "content": "Entrambi validi. DESeq2 tende a essere più robusto su dataset piccoli."},
            {"role": "user", "content": "Il dataset che ho è da 18 campioni. Abbastanza piccolo."},
            {"role": "assistant", "content": "Allora DESeq2 è una scelta naturale."},
            {"role": "user", "content": "Mi serve poi classificare i geni upregulated usando un modello ML."},
            {"role": "assistant", "content": "Puoi usare random forest o un modello lineare regolarizzato per iniziare."},
            {"role": "user", "content": "Sto considerando anche una pipeline RAG per spiegare le funzioni geniche."},
            {"role": "assistant", "content": "Ottima idea: un RAG può collegare ogni gene alle annotazioni di database biologici."},
            {"role": "user", "content": "In quel caso devo chunkare le descrizioni dei geni o le passo intere?"},
            {"role": "assistant", "content": "Meglio chunk brevi: le descrizioni possono essere verbose."},
            {"role": "user", "content": "E un sommario della sessione ogni 20 messaggi basta?"},
            {"role": "assistant", "content": "È sufficiente, considerando che l’argomento è denso ma non estremamente dialogico."},
            {"role": "user", "content": "Per ridurre i token pensavo al toon-format."},
            {"role": "assistant", "content": "Funziona bene anche con contenuti biologici strutturati."}
            ],
        "expected_summary": "L’utente analizza dati RNA-Seq e sceglie DESeq2 per dataset piccoli. Vuole classificare geni upregulated, integrare un RAG per spiegare le funzioni geniche, usare chunk brevi, generare sommari periodici e adottare toon-format per comprimere il contesto."
    },
    {
        "conversation_history": [
            {"role": "user", "content": "Sto lavorando a un robot mobile e voglio migliorare la localizzazione."},
            {"role": "assistant", "content": "Stai usando un approccio SLAM o solo odometria?"},
            {"role": "user", "content": "SLAM, ma l'odometria è rumorosa."},
            {"role": "assistant", "content": "Allora usa un filtro di Kalman esteso per la fusione sensoriale."},
            {"role": "user", "content": "Ho anche un LiDAR 2D. Lo integro nel filtro?"},
            {"role": "assistant", "content": "Sì, usando le misure come osservazioni per correggere la stima."},
            {"role": "user", "content": "Sto generando log dettagliati del robot. Li voglio analizzare con RAG per capire errori di navigazione."},
            {"role": "assistant", "content": "Molto utile: puoi costruire una base di conoscenza delle anomalie più comuni."},
            {"role": "user", "content": "Meglio embeddings o keyword search?"},
            {"role": "assistant", "content": "Embeddings, perché gli errori sono spesso descritti in modo poco uniforme."},
            {"role": "user", "content": "Ogni volta che il robot completa un ciclo, vorrei un sommario automatico."},
            {"role": "assistant", "content": "Soluzione tipica: generi un report compatto degli eventi principali del ciclo."},
            {"role": "user", "content": "L’uso del toon-format ha senso anche qui?"},
            {"role": "assistant", "content": "Sì, se i log sono lunghi e ripetitivi."}
            ],
        "expected_summary": "L’utente sta lavorando alla localizzazione di un robot mobile usando SLAM e sensor fusion via filtro di Kalman esteso. Integra dati LiDAR, genera log da analizzare con RAG, preferisce embeddings per la variabilità degli errori e usa sommari a fine ciclo con toon-format per ridurre la lunghezza dei log."
    },
    {
        "conversation_history": [
            {"role": "user", "content": "Sto lavorando al mio sistema RAG ma Docker mi rompe tutto. I container non vedono la cartella dei documenti."},
            {"role": "assistant", "content": "Probabile problema di mount. Controlla i volumi nel docker-compose."},
            {"role": "user", "content": "Sì ma nel frattempo l’embedder crasha perché non trova le risorse. Forse è colpa dei permessi?"},
            {"role": "assistant", "content": "È possibile: Docker a volte monta con permessi root-only."},
            {"role": "user", "content": "Tra l’altro il tokenizer sta esplodendo: `[ValueError: text too long]`."},
            {"role": "assistant", "content": "Se stai processando PDF enormi, devi chunkare prima."},
            {"role": "user", "content": "Aspetta… ora tutto si blocca e mi esce `OSError: cannot allocate memory`."},
            {"role": "assistant", "content": "Sembra un loop di elaborazione. Hai controllato che l’ingestion non reinserisca gli stessi file?"},
            {"role": "user", "content": "Non ancora. E mentre tutto ciò succede, voglio aggiungere anche un modulo per analizzare log Kubernetes."},
            {"role": "assistant", "content": "In questo caso conviene separare l’ingestion in pipeline distinte."},
            {"role": "user", "content": "Sto provando a fare una tool-call: `TOOL{type=retrieve, query='docker error mount'}` ma non so dove metterla."},
            {"role": "assistant", "content": "Dipende dal tuo framework. Sembra comunque una debug call interna."},
            {"role": "user", "content": "Ok cambio argomento: quanto testo posso mettere in un sommario incrementale senza far saltare tutto?"},
            {"role": "assistant", "content": "Mantieni il sommario sotto i 500 token se vuoi evitare esplosioni ricorsive."},
            {"role": "user", "content": "E se uso toon-format invece?"},
            {"role": "assistant", "content": "Riduce il rischio, ma non fa miracoli: se l’ingestion è rotta, rimane rotta."},
            {"role": "user", "content": "Sto anche migrando tutto da Windows a Ubuntu… forse peggioro la situazione."},
            {"role": "assistant", "content": "Di solito la migliori. L’ambiente Linux è più prevedibile per ML e container."}
        ],
        "expected_summary": "L’utente ha problemi con il sistema RAG: volumi Docker non montati, permessi errati, crash del tokenizer e potenziali loop di ingestion. Valuta l’analisi di log Kubernetes e usa pseudo-tool-call. Chiede indicazioni sui sommari incrementali e sul toon-format. L’assistente suggerisce chunking, limiti di token e pipeline separate, con nota sul vantaggio di migrare a Linux."
    },
    {
        "conversation_history": [
            {"role": "user", "content": "Sto cercando di ottimizzare un modello di regressione ma l’MSE è negativo. Non dovrebbe essere impossibile?"},
            {"role": "assistant", "content": "Corretto, un MSE negativo indica un errore di calcolo o di implementazione."},
            {"role": "user", "content": "Forse ho normalizzato due volte. O forse tre."},
            {"role": "assistant", "content": "Normalizzazioni duplicate possono distruggere le scale dei dati."},
            {"role": "user", "content": "Sto usando anche un RAG per spiegare i residui ma la risposta è: ‘la regressione è un mito platonico’."},
            {"role": "assistant", "content": "Sembra ironica o fuori dominio. Potresti avere documenti non puliti."},
            {"role": "user", "content": "Poi ho provato una tool-call: TOOL{fit_model, params={lr: 0.05}} ma è apparsa nella chat finale."},
            {"role": "assistant", "content": "Probabilmente il sistema non filtra correttamente le tool-calls."},
            {"role": "user", "content": "Ho cambiato modello passando a una rete neurale ma il loss è NaN dopo due iterazioni."},
            {"role": "assistant", "content": "Di solito succede con learning rate troppo alto o dati mal normalizzati."},
            {"role": "user", "content": "E nel mezzo ho rotto l’ambiente virtuale aggiornando pip a metà."},
            {"role": "assistant", "content": "Ricompatta l’ambiente da zero, è la scelta più sicura."},
            {"role": "user", "content": "Vorrei comunque includere una pipeline di summarization automatica, ogni 30 messaggi."},
            {"role": "assistant", "content": "Va bene, purché il sommario sia stabile e non ricorsivo."},
            {"role": "user", "content": "Uso toon-format o markdown minimalista?"},
            {"role": "assistant", "content": "Toon-format se vuoi più compressione."},
            {"role": "user", "content": "Il bello è che i log del training sono pieni di caratteri random tipo `▒▒▒▒`. Devo chunkarli?"},
            {"role": "assistant", "content": "Sì, e devi ripulirli per evitare caratteri binari nel corpus."},
            {"role": "user", "content": "Ah e non so perché, ma il mio script logga ogni batch due volte."},
            {"role": "assistant", "content": "Probabile callback registrata doppia o loop annidato."},
            {"role": "user", "content": "Comunque, in tutto questo, il problema dell’MSE negativo resta un mistero."},
            {"role": "assistant", "content": "Devi verificare la funzione di perdita: forse stai calcolando la differenza al contrario o stai restituendo un valore normalizzato male."}
        ],
        "expected_summary": "L’utente cerca di ottimizzare un modello di regressione ma ottiene un MSE negativo, probabilmente per normalizzazioni multiple o implementazione errata. Ha problemi con il RAG che restituisce risposte fuori dominio, tool-calls che appaiono nella chat, NaN nel training di una rete neurale, un ambiente virtuale corrotto e log danneggiati. L’assistente suggerisce pulizia, filtraggio dei documenti, limiti ai sommari, uso del toon-format e controlli sulla funzione di perdita."
    }
]