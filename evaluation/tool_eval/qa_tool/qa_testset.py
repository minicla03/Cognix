TEST_CASES = [
    {
        "query": "Cosa sono i servizi in Android?",
        "expected_answer": (
            "I servizi in Android sono componenti che eseguono operazioni in background senza mostrare un'interfaccia. "
            "Possono continuare a funzionare anche se l'rag_qa non è visibile. "
            "Ci sono tipi diversi come Started Service (avviato da un componente), Bound Service (permette a componenti di connettersi) e Foreground Service (che l'utente nota). "
            "Hanno un ciclo di vita gestito da metodi come onCreate(), onStartCommand(), onBind() e onDestroy()."
        ),
        "language_hint": "italian",
        "relevant_docs": ["Android.pdf"],
        "summary": None
    },
    {
        "query": "Cos'è un'activity?",
        "expected_answer": (
            "Un'activity in Android è una schermata con cui l'utente interagisce. "
            "È una classe che gestisce il ciclo di vita con metodi come onCreate(), onStart(), onResume(), onPause(), onStop() e onDestroy(). "
            "Le activity comunicano tramite Intent e si dichiarano nel file AndroidManifest.xml. "
            "Un'rag_qa può avere più activity con scopi diversi."
        ),
        "language_hint": "italian",
        "relevant_docs": ["Android.pdf"],
        "summary": None
    },
    {
        "query": "A cosa serve il manifest.xml?",
        "expected_answer": (
            "Il file AndroidManifest.xml è essenziale per configurare un'rag_qa Android. "
            "Contiene informazioni su tutti i componenti come activity, servizi, e permessi richiesti. "
            "Definisce quale activity è quella principale e può specificare filtri per gli intent. "
            "Si trova nella cartella principale del progetto."
        ),
        "language_hint": "italian",
        "relevant_docs": ["Android.pdf"],
        "summary": None
    },
    {
        "query": "Cos'è il modello a cascata in ingegneria del software?",
        "expected_answer": (
            "Il modello a cascata è un metodo di sviluppo software in cui le fasi seguono un ordine preciso e lineare: "
            "analisi dei requisiti, progettazione, implementazione, test, rilascio e manutenzione. "
            "Ogni fase si completa prima di iniziare la successiva, senza tornare indietro. "
            "È semplice da gestire ma poco flessibile ai cambiamenti."
        ),
        "language_hint": "italian",
        "relevant_docs": ["IngSw teo pt2.pdf"],
        "summary": None
    },
    {
        "query": "Cos'è il pattern Observer in ingegneria del software?",
        "expected_answer": (
            "Il pattern Observer è un modello che definisce una relazione uno-a-molti tra oggetti. "
            "Quando un oggetto cambia stato, tutti gli oggetti osservatori vengono aggiornati automaticamente. "
            "Prevede un'interfaccia Observer con un metodo update() e un Subject che gestisce la lista degli osservatori. "
            "È utile per sistemi reattivi e notifiche."
        ),
        "language_hint": "italian",
        "relevant_docs": ["Software Design.pdf"],
        "summary": None
    },
    {
        "query": "Come è strutturata una classe di testing?",
        "expected_answer": (
            "Una classe di testing serve a verificare il funzionamento del codice ed è organizzata in tre parti: "
            "1. Setup, con metodi come setUp() o annotazioni @Before per preparare l'ambiente; "
            "2. Test, dove si usano metodi con assertion per controllare i risultati; "
            "3. Teardown, con metodi come tearDown() o @After per pulire le risorse. "
            "Si possono usare mock per isolare dipendenze e si applica il principio AAA (Arrange-Act-Assert). "
            "Framework comuni sono JUnit, pytest e Espresso."
        ),
        "language_hint": "italian",
        "relevant_docs": ["IngSw teo pt2.pdf", "Android.pdf"],
        "summary": None
    },
    {
        "query": "What is the purpose of an oscilloscope?",
        "expected_answer": (
            "An oscilloscope is an electronic instrument that shows how voltage signals change over time. "
            "It helps engineers see signal features like frequency, amplitude, and shape. "
            "Modern oscilloscopes capture analog and digital signals and offer tools like triggering and measurements. "
            "They are essential for debugging and testing electronic circuits."
        ),
        "language_hint": "english",
        "relevant_docs": ["Misure Elettroniche.pdf"],
        "summary": None
    },
    {
        "query": "Explain the concept of RMS voltage.",
        "expected_answer": (
            "RMS voltage (Root Mean Square) is a way to express the effective value of an AC voltage. "
            "It is calculated by taking the square root of the average of the squared instantaneous voltages over one cycle. "
            "For a sine wave, RMS equals the peak voltage divided by √2 (about 0.707 times the peak). "
            "RMS values relate AC voltage to the equivalent DC power and are the standard for measurements."
        ),
        "language_hint": "english",
        "relevant_docs": ["Misure Elettroniche.pdf", "Data Analytics.pdf"],
        "summary": None
    },
    {
        "query": "¿Qué es el análisis exploratorio de datos?",
        "expected_answer": (
            "El análisis exploratorio de datos (EDA) es un método para resumir y entender las características principales de un conjunto de datos. "
            "Incluye estadísticas descriptivas como media y desviación estándar, visualizaciones como histogramas y gráficos de dispersión, y la detección de patrones o anomalías. "
            "EDA es importante antes de aplicar modelos complejos para conocer la estructura y calidad de los datos."
        ),
        "language_hint": "spanish",
        "relevant_docs": ["Data Analytics.pdf"],
        "summary": None
    },
    {
        "query": "¿Para qué sirve la regresión lineal?",
        "expected_answer": (
            "La regresión lineal es una técnica para modelar la relación entre una variable dependiente y una o más variables independientes. "
            "Permite predecir valores y medir la fuerza de esa relación. "
            "Hay regresión simple (una variable) y múltiple (varias variables). "
            "Se usa en economía, ciencias sociales y machine learning, bajo supuestos como linealidad y normalidad de errores."
        ),
        "language_hint": "spanish",
        "relevant_docs": ["Data Analytics.pdf", "Misure Elettroniche.pdf"],
        "summary": None
    },
    {
        "query": "Qu'est-ce que le big data?",
        "expected_answer": (
            "Le big data désigne de très grands ensembles de données caractérisés par cinq aspects : volume, vélocité, variété, véracité et valeur. "
            "Ces données dépassent les capacités des outils traditionnels et nécessitent des technologies spécifiques comme Hadoop ou Spark. "
            "Le big data est utilisé pour l’analyse prédictive, la personnalisation et d’autres domaines, avec des défis liés au stockage et à la sécurité."
        ),
        "language_hint": "french",
        "relevant_docs": ["Data Analytics.pdf"],
        "summary": None
    },
    {
        "query": "À quoi sert une analyse prédictive?",
        "expected_answer": (
            "L’analyse prédictive utilise des données historiques et des algorithmes pour prévoir des événements futurs. "
            "Elle emploie des méthodes comme la régression et les arbres de décision. "
            "Ses applications incluent la prévision de la demande, la détection de fraudes et le marketing ciblé. "
            "Le processus comprend la collecte, la préparation des données, l’entraînement des modèles et la validation."
        ),
        "language_hint": "french",
        "relevant_docs": ["DataAnalytics.pdf"],
        "summary": None
    },
    {
        "query": "Was ist eine Klasse in der objektorientierten Programmierung?",
        "expected_answer": (
            "Eine Klasse ist ein Bauplan für Objekte in der objektorientierten Programmierung. "
            "Sie definiert Attribute und Methoden, die die Objekte besitzen. "
            "Objekte sind Instanzen der Klasse und verhalten sich entsprechend den definierten Methoden."
        ),
        "language_hint": "german",
        "relevant_docs": ["OOP_Grundlagen.pdf"],
        "summary": None
    },
    {
        "query": "Welche Arten von Services gibt es in Android?",
        "expected_answer": (
            "In Android gibt es verschiedene Arten von Services: Started Service, Bound Service und Foreground Service. "
            "Started Services werden einmal gestartet und laufen unabhängig, Bound Services erlauben anderen Komponenten die Verbindung, und Foreground Services sind für den Nutzer sichtbar. "
            "Services laufen im Hintergrund und ihr Lebenszyklus wird über Methoden wie onCreate(), onStartCommand(), onBind() und onDestroy() gesteuert."
        ),
        "language_hint": "german",
        "relevant_docs": ["Android.pdf"],
        "summary": None
    },
    {
        "query": "Wie kommunizieren Activities untereinander?",
        "expected_answer": (
            "Activities kommunizieren über Intents miteinander. "
            "Ein Intent kann Daten enthalten und eine andere Activity starten. "
            "Dies ermöglicht die Navigation zwischen verschiedenen Bildschirmen innerhalb einer App, die im AndroidManifest.xml registriert sein müssen."
        ),
        "language_hint": "german",
        "relevant_docs": ["Android.pdf"],
        "summary": None
    },
    {
        "query": "Welche Aufgaben hat die AndroidManifest.xml?",
        "expected_answer": (
            "Die AndroidManifest.xml definiert alle Komponenten einer App, wie Activities, Services und Berechtigungen. "
            "Sie legt die Haupt-Activity fest, beschreibt Intent-Filter und ist notwendig, damit das Betriebssystem die App korrekt ausführt. "
            "Ohne Manifest können die Komponenten nicht erkannt werden."
        ),
        "language_hint": "german",
        "relevant_docs": ["Android.pdf"],
        "summary": None
    },
    {
        "query": "Was versteht man unter Software-Design-Patterns?",
        "expected_answer": (
            "Software-Design-Patterns sind bewährte Lösungen für häufig auftretende Probleme in der Softwareentwicklung. "
            "Sie bieten wiederverwendbare Konzepte, die die Wartbarkeit und Flexibilität erhöhen. "
            "Ein Beispiel ist das Observer-Muster, bei dem Objekte automatisch benachrichtigt werden, wenn sich der Zustand eines anderen Objekts ändert."
        ),
        "language_hint": "german",
        "relevant_docs": ["Software Design.pdf"],
        "summary": None
    },
    {
        "query": "Welche Schritte umfasst eine typische Testklasse?",
        "expected_answer": (
            "Eine Testklasse umfasst typischerweise drei Schritte: "
            "Setup zur Vorbereitung der Umgebung, Testmethoden mit Assertions zur Überprüfung des Codes, und Teardown zur Freigabe von Ressourcen. "
            "Mocks können zur Isolation von Abhängigkeiten genutzt werden, und das AAA-Prinzip (Arrange-Act-Assert) wird angewendet."
        ),
        "language_hint": "german",
        "relevant_docs": ["IngSw teo pt2.pdf", "Android.pdf"],
        "summary": None
    },
    {
        "query": "Was kann ein Oszilloskop messen?",
        "expected_answer": (
            "Ein Oszilloskop kann Spannungen über die Zeit darstellen, Signalformen analysieren und Frequenz sowie Amplitude messen. "
            "Es ermöglicht das Triggern auf bestimmte Signalereignisse und ist ein unverzichtbares Werkzeug beim Testen und Debuggen elektronischer Schaltungen."
        ),
        "language_hint": "german",
        "relevant_docs": ["Misure Elettroniche.pdf"],
        "summary": None
    },
    {
        "query": "Warum wird RMS-Spannung verwendet?",
        "expected_answer": (
            "RMS-Spannung (Effektivspannung) gibt den Energiegehalt einer Wechselspannung in Bezug auf Gleichstrom wieder. "
            "Sie wird als Quadratwurzel des Mittelwerts der quadrierten Momentanwerte über einen Zyklus berechnet. "
            "RMS erleichtert die Vergleichbarkeit und Berechnung von Leistung bei Wechselspannung."
        ),
        "language_hint": "german",
        "relevant_docs": ["Misure Elettroniche.pdf", "Data Analytics.pdf"],
        "summary": None
    },
    {
        "query": "Welche Schritte gehören zur explorativen Datenanalyse?",
        "expected_answer": (
            "Die explorative Datenanalyse umfasst die Untersuchung von Datensätzen mittels Statistik, Visualisierung und Mustererkennung. "
            "Typische Schritte sind deskriptive Statistik, Grafiken wie Histogramme oder Streudiagramme, sowie die Erkennung von Ausreißern und Anomalien."
        ),
        "language_hint": "german",
        "relevant_docs": ["Data Analytics.pdf"],
        "summary": None
    },
    {
        "query": "Welche Vorteile bietet lineare Regression?",
        "expected_answer": (
            "Die lineare Regression modelliert die Beziehung zwischen abhängigen und unabhängigen Variablen. "
            "Sie erlaubt Vorhersagen, die Messung der Stärke von Zusammenhängen und die Identifikation relevanter Einflussgrößen. "
            "Sie ist einfach zu interpretieren und weit verbreitet in Wirtschaft, Wissenschaft und Machine Learning."
        ),
        "language_hint": "german",
        "relevant_docs": ["Data Analytics.pdf", "Misure Elettroniche.pdf"],
        "summary": None
    },
    {
        "query": "Welche Technologien werden bei Big Data eingesetzt?",
        "expected_answer": (
            "Für Big Data werden Technologien wie Hadoop und Spark eingesetzt, um sehr große und vielfältige Datensätze zu speichern und zu verarbeiten. "
            "Ziele sind Analyse, Prognose und Personalisierung, während Herausforderungen Speicher, Geschwindigkeit und Sicherheit betreffen."
        ),
        "language_hint": "german",
        "relevant_docs": ["Data Analytics.pdf"],
        "summary": None
    },
    {
        "query": "Wie funktioniert prädiktive Analyse?",
        "expected_answer": (
            "Prädiktive Analyse nutzt historische Daten und Algorithmen, um zukünftige Ereignisse vorherzusagen. "
            "Sie umfasst Datensammlung, Datenaufbereitung, Modelltraining und Validierung. "
            "Methoden wie Regression, Entscheidungsbäume oder maschinelles Lernen werden angewendet."
        ),
        "language_hint": "german",
        "relevant_docs": ["DataAnalytics.pdf"],
        "summary": None
    },
]