MENU = [
    {
    'label': 'Navegação',
    'permission': None,
    'submenu': [
        {
            'label': 'Início',
            'url': 'index',
            'permission': None
        }
    ]
},
    {
    'label': 'Correspondências',
    'permission': None,
    'submenu': [
        {
            'label': 'Nova',
            'url': 'mail.new',
            'permission': None
        },
        {
            'label': 'Enviados',
            'url': 'mail.my_mails',
            'permission': None
        },
        {
            'label': 'Recebidos',
            'url': 'mail.my_mails',
            'permission': 'não implementado'
        }
    ]
},
    {
    'label': 'Administração',
    'permission': 'acesso restrito',
    'submenu': [
        {
            'label': 'Gestão de usuários',
            'url': 'user.manager_user',
            'permission': 'acesso restrito'
        },
        {
            'label': 'Gestão Organizacional',
            'url': 'organization.manager_new_org',
            'permission': 'acesso restrito'
        },
        {
            'label': 'Gestão Perfis e Permissões',
            'url': 'admin.roles',
            'permission': 'acesso restrito'
        },
        {
            'label': 'Relatórios',
            'url': 'index',
            'permission': 'não implementado'
        },
        {
            'label': 'Log de Atividades',
            'url': 'index',
            'permission': 'não implementado'
        }
    ]
},
]