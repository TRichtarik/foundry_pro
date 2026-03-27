{
    'name': 'Foundry Composition – Quality Bridge',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'sequence': 51,
    'summary': 'Chemistry Sample quality check type for foundry heats',
    'description': """
Foundry Composition – Quality Bridge
=====================================
Adds a **Chemistry Sample** quality check type that creates structured
``foundry.analysis`` records with per-element readings and automatic
in-spec / out-of-spec evaluation against the heat's alloy grade.

This module installs automatically when both *Foundry Composition* and
*Quality Control* (Enterprise) are present.  It does not need to be
purchased separately.
""",
    'author': 'Tomáš Richtárik',
    'website': 'https://tomasrichtarik.sk',
    'license': 'OPL-1',
    'price': 119.00,
    'currency': 'EUR',
    'depends': [
        'foundry_composition',
        'quality_control',
        'quality_mrp',
    ],
    'data': [
        'data/quality_data.xml',
        'views/quality_views.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'auto_install': True,
    'installable': True,
}
