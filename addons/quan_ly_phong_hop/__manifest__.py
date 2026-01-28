# -*- coding: utf-8 -*-
{
    'name': 'Quản lý phòng họp',
    'summary': 'Quản lý phòng họp nội bộ',
    'description': 'Module quản lý phòng họp',
    'author': 'TTDN-16-05-N4',
    'website': 'https://github.com/Nemmer772004/TTDN-16-05-N4',
    'category': 'Administration',
    'version': '1.0',
    'license': 'LGPL-3',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/quan_ly_phong_hop.xml',
        'views/dat_phong.xml',
        'views/lich_su_thay_doi.xml',
        'views/lich_su_muon_tra.xml',
        'views/thiet_bi.xml',
        'views/dat_phong_dashboard.xml',
        'views/menu.xml',
    ],

    'installable': True,
    'application': True,
}
