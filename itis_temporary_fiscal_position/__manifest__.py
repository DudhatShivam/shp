# -*- coding: utf-8 -*-
# Part of IT IS AG. See LICENSE file for full copyright and licensing details.


{
    'name': 'IT IS temporary fiscal position',
    'version': '13.0.1',
    'category': 'Tools',
    'sequence': 1,
    'summary': 'Temporary fiscal position',
    'description': """

Um die Wirtschaft nach der Corona-Krise wieder anzukurbeln, hat sich die Bundesregierung auf ein umfangreiches steuerliches Konjunkturpaket geeinigt. Ein zentraler Bestandteil dieser Maßnahmen, ist die temporäre Senkung der gesetzlichen Umsatzsteuer.

    - Der normale Regelsteuersatz wird von derzeit 19% auf 16% gesenkt
    - Der ermäßigte Steuersatz wird von 7% auf 5% gesenkt.
    - Die Mehrwertsteuersenkung gilt für alle Unternehmer.

Die gesenkten Umsatzsteuersätze treten am 1.7.2020 in Kraft und gelten 6 Monate – also bis zum 31.12.2020.
Nach dem 31.12.2020 sind voraussichtlich wieder die alten Sätze in Höhe von 19 % beim Regelsteuersatz und 7 % bei dem ermäßigten Steuersatz gültig.
Die Absenkung der Umsatzsteuersätze ist sowohl für die Erstellung von Ausgangsrechnungen an Kunden, sowie auch für die Prüfung von Eingangsrechnungen relevant.

Gültigkeit der Steuersätze:
Der Zeitpunkt der Ausführung der Leistung ist maßgeblich für die Anwendung des jeweiligen Steuersatzes. Das Datum der Leistungserbringung ist danach entscheidend, mit welchem Steuersatz der Umsatz zu berechnen bzw. der Vorsteuerabzug vorzunehmen ist.


Diese einschneidenden Änderungen, müssen auch entsprechend in Ihrem ERP-System abgebildet sein. Hierfür stellen wir Ihnen dieses Modul zur Verüfung, um die Abbildung im System zu vereinfachen.


HAFTUNGSAUSSCHLUSS:
Dieses Modul, sowie unsere Dokumentation haben ausschließlich eine Unterstützungsfunktion zur befristeten Steuersenkung, ersetzt aber in keinem Falle die Kontrolle durch den Unternehmer selbst, bzw. dessen Steuerberater.
Die Anpassungen und Ratschläge in diesem Module und Dokument erfolgen ohne Gewähr und ohne den Anspruch auf Vollständigkeit oder Richtigkeit.
    """,
    'author': "IT IS AG",
    'website': "http://www.itis-odoo.de",
    'depends': ['sale_management', 'purchase'],
    'data': [
        'views/assets.xml',
        'data/data.xml',
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'views/sale_views.xml',
        'views/purchase_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'demo': [
        
    ],
    'qweb': [
        "static/src/xml/base.xml",
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'post_init_hook': '_add_server_action_menu',
}
