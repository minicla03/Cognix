TEST_ROUTER_DATASET = [
    {
        "query": "Spiegami in modo semplice il funzionamento del protocollo MQTT.",
        "expected_tool": "QA_TOOL"
    },
    {
        "query": "Generami 5 flashcard sul capitolo del Fog Computing.",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Fammi un quiz a risposta multipla sul machine learning supervisionato.",
        "expected_tool": "QUIZ_TOOL"
    },
    {
        "query": "Make flashcards about the OSI model.",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Qual è la differenza tra edge e cloud computing?",
        "expected_tool": "QA_TOOL"
    },
    {
        "query": "Explain how SSL/TLS works in simple terms.",
        "expected_tool": "QA_TOOL"
    },
    {
        "query": "Create 10 flashcards to study Kubernetes architecture.",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Generate a multiple-choice quiz about operating systems.",
        "expected_tool": "QUIZ_TOOL"
    },
    {
        "query": "Explícame la diferencia entre inteligencia artificial y aprendizaje automático.",
        "expected_tool": "QA_TOOL"
    },
    {
        "query": "Crea tarjetas de estudio sobre el modelo TCP/IP.",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Genérame un cuestionario de 5 preguntas sobre seguridad informática.",
        "expected_tool": "QUIZ_TOOL"
    },
    {
        "query": "Explique-moi le fonctionnement du protocole HTTPS.",
        "expected_tool": "QA_TOOL"
    },
    {
        "query": "Crée des flashcards pour réviser le modèle client-serveur.",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Génère un quiz sur les bases de données relationnelles.",
        "expected_tool": "QUIZ_TOOL"
    },
    {
        "query": "Erkläre mir den Unterschied zwischen RAM und ROM.",
        "expected_tool": "QA_TOOL"
    },
    {
        "query": "Erstelle Lernkarten über Netzwerkschichten.",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Erzeuge ein Quiz über neuronale Netze.",
        "expected_tool": "QUIZ_TOOL"
    },

    # ——— LINGUA MISTA ———
    {
        "query": "Explícame in English sobre TCP/IP, please.",
        "expected_tool": "QA_TOOL"
    },
    {
        "query": "Crea flashcards sobre Kubernetes in italiano.",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Make un pequeño quiz sobre cloud computing.",
        "expected_tool": "QUIZ_TOOL"
    },
    {
        "query": "Mi fai un riassunto about SSL/TLS?",
        "expected_tool": "QA_TOOL"
    },

    # ——— INPUT MINIMALISTI ———
    {
        "query": "Flashcards?",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Quiz!",
        "expected_tool": "QUIZ_TOOL"
    },
    {
        "query": "Explain?",
        "expected_tool": "QA_TOOL"
    },

    # ——— TYPO / ERRORI ———
    {
        "query": "Fashcards sobre AI plz",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Qwiz about networking",
        "expected_tool": "QUIZ_TOOL"
    },
    {
        "query": "Expalin how HTTP works",
        "expected_tool": "QA_TOOL"
    }
]

COMPLEX_CASES = [

    # ——— AMBIGUITÀ (intenzionalmente borderline) ———
    {
        "query": "Mi fai un riassunto del capitolo sulla sicurezza di rete? Magari anche due domande per ripassare.",
        "expected_tool": "QA_TOOL"
        # La parte dominante è il riassunto → QA_TOOL
    },
    {
        "query": "Vorrei capire meglio Docker. Puoi anche generare qualche domanda se serve.",
        "expected_tool": "QA_TOOL"
        # Focus primario → capire meglio (QA), non creare domande
    },
    {
        "query": "Spiegami cos'è il machine learning e crea poi delle flashcard.",
        "expected_tool": "FLASHCARD_TOOL"
        # Ambigua: la richiesta finale domina
    },
    {
        "query": "Come funziona Kafka? E dopo fammi un piccolo quiz.",
        "expected_tool": "QUIZ_TOOL"
    },

    # ——— RUMORE (linguaggio colloquiale, errori, slang) ———
    {
        "query": "Bro plz make me some flashcards about cloud stuff thx.",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Ehi senti, mi fai un quiz easy sul deep learning?",
        "expected_tool": "QUIZ_TOOL"
    },
    {
        "query": "Hey could u, like, explain 5G architecture but keep it simple?",
        "expected_tool": "QA_TOOL"
    },
    {
        "query": "Oye, ¿me haces ‘unas tarjetitas’ para estudiar redes?",
        "expected_tool": "FLASHCARD_TOOL"
    },

    # ——— MISTI (richieste doppie → conta l’intento prevalente) ———
    {
        "query": "Prima spiegami cosa fa un load balancer e poi crea qualche flashcard per ricordarlo.",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Dame un resumen de blockchain y tal vez unas preguntas.",
        "expected_tool": "QA_TOOL"
    },
    {
        "query": "Parlami del modello OSI e fammi anche un quiz se puoi.",
        "expected_tool": "QUIZ_TOOL"
    },
    {
        "query": "Kannst du mir die wichtigsten Punkte von TCP erklären und danach ein paar Lernkarten machen?",
        "expected_tool": "FLASHCARD_TOOL"
    },

    # ——— ERRORI UMANI/TYPO/MIX DI LINGUE ———
    {
        "query": "Puoi expalin me la diff tra RAM e cache?",
        "expected_tool": "QA_TOOL"
    },
    {
        "query": "Flashcards bitte über cybersec pls.",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Quiz sobre sistema operativos, porfavo? (sí, mal escrito).",
        "expected_tool": "QUIZ_TOOL"
    },
    {
        "query": "Fai un explayn su AI, grazie.",
        "expected_tool": "QA_TOOL"
    },

    # ——— INDIRETTI (richieste che implicano il tool senza nominarlo) ———
    {
        "query": "Vorrei delle domande per capire se ho capito gli algoritmi di sorting.",
        "expected_tool": "QUIZ_TOOL"
    },
    {
        "query": "Mi servono appunti facili da ripassare sul serverless.",
        "expected_tool": "QA_TOOL"
        # “appunti” → riassunto → QA
    },
    {
        "query": "Ho bisogno di un modo rapido per memorizzare il modello TCP/IP.",
        "expected_tool": "FLASHCARD_TOOL"
        # implicito → flashcard
    },
    {
        "query": "Give me something to test if I truly understand microservices.",
        "expected_tool": "QUIZ_TOOL"
    },

    # ——— TRICK (richiesta fuorviante: sembra A ma è B) ———
    {
        "query": "Scrivimi un elenco di 5 domande e risposte sulla sicurezza web.",
        "expected_tool": "FLASHCARD_TOOL"
        # Domande+risposte → flashcard, non quiz
    },
    {
        "query": "Fammi 10 domande senza risposta sul cloud computing.",
        "expected_tool": "QUIZ_TOOL"
        # Domande senza risposta → quiz, non flashcard
    },
    {
        "query": "Posso avere un set di coppie domanda-risposta sul TCP?",
        "expected_tool": "FLASHCARD_TOOL"
    },
    {
        "query": "Mi fai domande sì/no per verificare che ho capito il machine learning?",
        "expected_tool": "QUIZ_TOOL"
    }
]

