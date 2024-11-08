from dataclasses import dataclass
from typing import Optional


def _get_value(cls, attr: str) -> str:
    if not hasattr(cls, attr):
        raise KeyError(f'"{key}" is not a property of this class.')
    value = getattr(cls, attr)
    expected_type = cls.__annotations__[attr]

    if hasattr(expected_type, '_name') and expected_type._name == Optional._name:
        if not value:
            return ''
        expected_type = expected_type.__args__[0]

    if hasattr(expected_type, '__origin__'):
        if not isinstance(value, expected_type.__origin__):
            raise ValueError(
                f'A value of type "{expected_type.__origin__.__name__}" '
                f'was expected for "{attr}".')
    elif not isinstance(value, expected_type):
        raise ValueError(
            f'A value of type "{expected_type.__name__}" '
            f'was expected for "{attr}".')

    if isinstance(value, dict):
        locale_type = expected_type.__args__[0]
        if hasattr(expected_type.__args__[1], '__origin__'):
            value_type = expected_type.__args__[1].__origin__
            lv_type = expected_type.__args__[1].__args__[0]
        else:
            value_type = expected_type.__args__[1]
        value_formatted = ''
        key = ''.join(part.capitalize() for part in attr.split('_')[:-1])
        for locale, value in value.items():
            if not isinstance(locale, locale_type):
                raise KeyError(
                    f'A value of type "{locale_type.__name__}" '
                    f'was expected for the key "{locale}" of "{attr}".')
            elif not isinstance(value, value_type):
                raise ValueError(
                    f'A value of type "{value_type.__name__}" '
                    f'was expected for "{locale}" of "{attr}".')
            elif value_type is list:
                kw_formatted = ''
                for kw in value:
                    if not isinstance(kw, lv_type):
                        raise ValueError(
                            f'A value of type "{lv_type.__name__}" '
                            f'was expected for "{attr}[{local}]" '
                            f'index "{value.index(kw)}".')
                    kw_formatted += kw + ';'
                value = kw_formatted
            value_formatted += f'{key}[{locale}]={value}\n'
        return value_formatted.rstrip('\n')
    elif isinstance(value, list):
        value_formatted = ''
        lv_type = expected_type.__args__[0]
        for lv in value:
            if not isinstance(lv, lv_type):
                raise ValueError(
                    f'A value of type "{lv_type.__name__}" '
                    f'was expected for "{attr}" index "{value.index(lv)}".')
            elif isinstance(lv, Action):
                lv = lv.id
            value_formatted += lv + ';'
        value = value_formatted
    elif isinstance(value, bool):
        value = str(value).lower()
    elif not value:
        raise ValueError(
            f'"{attr}" has a null value or categorized as "empty".')

    return ''.join(part.capitalize() for part in attr.split('_')) + f'={value}'


@dataclass
class Action:
    name: str = None
    name_ls: dict[str, str] = None
    icon: Optional[str] = None
    exec: str = None

    def __init__(self, id: str, **kargs):
        self.id = id
        for key, value in kargs.items():
            if not hasattr(self, key) or \
                    hasattr(getattr(self, key), '__call__') or key.startswith('_'):
                raise KeyError(f'"{key}" is not a property of this class.')
            setattr(self, key, value)

    def generate(self) -> str:
        desktop_entry = f'[Desktop Action {self.id}]\n'
        for attr in self.__annotations__.keys():
            field = _get_value(self, attr)
            desktop_entry += field + '\n' if field else ''
        return desktop_entry.rstrip('\n')


@dataclass
class DesktopEntry:
    _type: str = 'Application'
    _version: str = '1.5'
    name: str = None
    name_ls: dict[str, str] = None
    generic_name: Optional[str] = None
    generic_name_ls: dict[str, str] = None
    comment: Optional[str] = None
    comment_ls: dict[str, str] = None
    icon: Optional[str] = None
    exec: str = None
    terminal: bool = False
    actions: Optional[list[Action]] = None
    mime_type: Optional[list[str]] = None
    categories: Optional[list[str]] = None
    keywords: Optional[list[str]] = None
    keywords_ls: dict[str, list[str]] = None
    startup_notify: bool = False
    single_main_window: bool = False

    def __init__(self, **kargs):
        for key, value in kargs.items():
            if not hasattr(self, key) or \
                    hasattr(getattr(self, key), '__call__') or key.startswith('_'):
                raise KeyError(f'"{key}" is not a property of this class.')
            setattr(self, key, value)

        for attr in self.__annotations__.keys():
            if attr.startswith('_'):
                continue
            property_type = self.__annotations__[attr]
            if hasattr(property_type, '_name'):
                property_type = property_type.__args__[0]
            if hasattr(property_type, '__origin__'):
                property_type = property_type.__origin__
            if property_type is dict and getattr(self, attr) is None:
                setattr(self, attr, {})
            elif property_type is list and getattr(self, attr) is None:
                setattr(self, attr, [])

    def generate(self) -> str:
        desktop_entry = '[Desktop Entry]\n'
        for attr in self.__annotations__.keys():
            field = _get_value(self, attr)
            desktop_entry += field + '\n' if field else ''
        for action in self.actions:
            desktop_entry += f'\n{action.generate()}\n' 
        return desktop_entry.rstrip('\n')


if __name__ == '__main__':
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
