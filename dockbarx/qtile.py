'''
Created on 15/apr/2015

@author: spax
'''

from common import *
from dockbarx.dockbar import SPECIAL_RES_CLASSES, DockBar
from groupbutton import Group, GroupIdentifierError
from log import logger
from libqtile.command import Client
from dockbarx import groupbutton
from dockbarx.groupbutton import WidgetFactory


class DockQ(DockBar):
    
    def __init__(self, parent):
        DockBar.__init__(self, parent)
        self.qtile = Client()
        
    def make_group_list(self):
        self.groups = DockBar.make_group_list(self)
        for identifier in self.qtile.groups().keys():
                self._DockBar__make_groupbutton(identifier)
        return self.groups
        
    def _DockBar__add_window(self, window):
        group = None
        window_identifier = window.get_name().lower()
        
        q_tile_window_list = self.qtile.windows()
        match=filter(lambda d : d['name'].lower() == window_identifier, q_tile_window_list)
        if len(match) > 0:
            qtile_window = match[0]
            group_identifier = qtile_window['group']
            self.windows[window] = group_identifier
            group = self.groups[group_identifier]
            group.add_window(window)
            
    def must_remove_group(self, group):
        return False
    
    def make_group(self, identifier, desktop_entry, pinned):
        return QtileGroup(self, self.qtile, identifier, desktop_entry, pinned)
       

class QtileGroup(groupbutton.Group):
    
    def __init__(self, dockbar, qtile, identifier=None, desktop_entry=None, 
        pinned=False):
        groupbutton.Group.__init__(self, dockbar, identifier=identifier, desktop_entry=desktop_entry, pinned=pinned, widget_factory=QtileWidgetFactory())
        self.qtile = qtile
        
    def action_select_empty(self):
        self.qtile.group[self.identifier].toscreen()


class QtileWidgetFactory(groupbutton.WidgetFactory):
    
    def get_window_list(self, group):
        return QtileWindowList(group)
    
    def get_group_button(self, group):
        return QtileGroupButton(group)
        
        
class QtileWindowList(groupbutton.WindowList):
    
    def can_be_shown(self):
        return True
    
class QtileGroupButton(groupbutton.GroupButton):
    
    def must_hide(self):
        return False
    
    def must_show_popup(self):
        return True
        