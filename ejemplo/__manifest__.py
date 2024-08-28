{
    'name':'ejemplo',
    'depends':[
        'base_setup'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',

    'data':[
        'security/ir.model.access.csv',
        'views/ejemplo_real_estate_views.xml',
        'views/ejemplo_menu.xml',
        'views/ejemplo_list_view.xml',
        'views/ejemplo_real_estate_form.xml',
        'views/ejemplo_real_estate_search.xml',
        'views/property_type_action.xml',
        'views/property_type_list_view.xml',
        'views/property_type_menu.xml',
        'views/property_tag_action.xml',
        'views/property_tag_menu.xml',
        'views/property_offer_tree_view.xml',
        'views/property_offer_form.xml',

    ]
}