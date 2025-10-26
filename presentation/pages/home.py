def render():

    from presentation.layout import render_navbar, render_footer
    from presentation.components.hero import render_hero
    from presentation.components.card import render_feature_cards

    """Vetrina/Homepage"""
    render_navbar()

    render_hero(
        'Sblocca il tuo potenziale di apprendimento',
        'Organizza i tuoi appunti, carica documenti e interagisci con l’AI per studiare in modo intelligente.',
        '🚀 Inizia ora',
        '/notebooks'
    )

    render_feature_cards([
        ('📚', 'Notebook Intelligenti', 'Organizza i tuoi materiali in spazi dedicati.'),
        ('📄', 'Analisi Documenti', 'Estrai automaticamente concetti e riassunti.'),
        ('💬', 'Chat Contestuale', 'Poni domande sui tuoi appunti.'),
    ])

    render_footer()
