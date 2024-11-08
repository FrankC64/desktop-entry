# Desktop-Entry
This repository contains a small code file to facilitate the creation of desktop entries.

## Use
Within **desktop.py** there are two classes, the main class **DesktopEntry** and **Action** a complementary class of **DesktopEntry** to add actions.

An example of use may be the following:
```Python
action1 = Action(
    'action-1',
    name='Action 1',
    name_ls={'es_DO': 'Acción 1'},
    icon='icon',
    exec='executable --action1',
)

action2 = Action(
    'action-2',
    name='Action 2',
    name_ls={'es_DO': 'Acción 2'},
    icon='icon',
    exec='executable --action2',
)

desktop_entry = DesktopEntry(
    name='Hello Browser',
    name_ls={'es_DO': 'Navegador Hola'},
    generic_name='Browser',
    generic_name_ls={'es_DO': 'Navegador'},
    comment='Comment',
    comment_ls={'es_DO': 'Comentario'},
    icon='icon',
    exec='executable',
    terminal=True,
    actions=[action1, action2],
    mime_type=['text/html', 'application/js'],
    categories=['Network', 'WebBrowser'],
    keywords=['web', 'browser'],
    keywords_ls={'es_DO': ['web', 'buscador']},
    startup_notify=True,
    single_main_window=False,
)

print(desktop_entry.generate())
```

Ouput:
```
[Desktop Entry]
Type=Application
Version=1.5
Name=Hello Browser
Name[es_DO]=Navegador Hola
GenericName=Browser
GenericName[es_DO]=Navegador
Comment=Comment
Comment[es_DO]=Comentario
Icon=icon
Exec=executable
Terminal=true
Actions=action-1;action-2;
MimeType=text/html;application/js;
Categories=Network;WebBrowser;
Keywords=web;browser;
Keywords[es_DO]=web;buscador;
StartupNotify=true
SingleMainWindow=false

[Desktop Action action-1]
Name=Action 1
Name[es_DO]=Acción 1
Icon=icon
Exec=executable --action1

[Desktop Action action-2]
Name=Action 2
Name[es_DO]=Acción 2
Icon=icon
Exec=executable --action2
```

Two actions and a desktop entry are created and to generate the complete desktop entry the **generate** method is called, which in turn is also present in the **Action** class.
