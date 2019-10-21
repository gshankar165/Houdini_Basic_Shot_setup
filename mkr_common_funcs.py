import os
import hou

class MkrCommonClass(object):
    def __init__(self,x):
        self.x = x
    def create_net_box_cmd(self,x=None):
        '''
        :param x: string:: name to create network box eg: "Ship"
        :return: string:: node name of network box eg: <hou.NetworkBox at /obj/Ship>
        '''
        var_a = hou.node("/obj")
        var_a.createNetworkBox(self.x)
        var_b = var_a.findNetworkBox(self.x)
        var_b.setComment(self.x)
        return var_b
    def merge_func(self,x=None):
        '''
        :param x: string:: file to import into the scene eg: /aslan/lookfile.hip
        :return: None
        '''
        return hou.hipFile.merge(self.x)
    def list_dir(self,x=None):
        '''
        :param x: string:: folder name eg: /aslan/asset
        :return: list:: list of all items in the directory eg: ["a", "b", "c"]
        '''
        return os.listdir(self.x)
    def path_exists(self,x=None):
        '''
        :param x: string:: folder name eg: /aslan/asset
        :return: bool:: True/False
        '''

        return os.path.exists(self.x)
    def get_childs(self,x=None):
        '''
        :param x: string:: any node to get its child nodes eg: "/obj" or "/obj/ship_alembic"
        :return: list:: list of all child nodes eg: (<hou.SopNode of type alembic at /obj/Ship/alembic1>, <hou.SopNode of type null at /obj/Ship/Geo_Out>,)
        '''
        var_a = hou.node(self.x)
        try:
            return var_a.children()
        except:
            pass
    def get_cache_value(self,x=None):
        '''
        :param x: string:: node name to get the cache path eg:  <hou.SopNode of type alembic at /obj/Ship/alembic1>
        :return: string:: alembic cache path eg: '/aslan//Marakkar/Portuguese_ship_001/cache/alembic/Portuguese_ship_002.abc'
        '''
        var_a =self.x
        if var_a.parm("fileName"):
            return var_a.parm("fileName").eval()
    def list_all_params(self,x=None):
        '''
        :param x: string:: houdini node to get the attribute list eg: <hou.RopNode of type ifd at /out/mantra1>
        :return: list:: list of all attributes eg: ['trange', 'f1', 'f2', 'f3', 'take',]
        '''
        var_a= self.x
        return [p.name() for p in var_a.parms()]
    def fix_layout(self,x=None):
        '''
        :param x: string:: parent node group name to fix the layout of childrens eg: <hou.ObjNode of type geo at /obj/Ship>
        :return: None
        '''
        var_a=hou.node(self.x)
        return var_a.layoutChildren()
    def cr_abc_xform_node(self,x=None):
        '''
        :param x: string:: input name to crate a node eg:"Ship01_transform"
        :return: None
        '''
        var_a = hou.node("/obj")
        return var_a.createNode("alembicxform", self.x)
    def confirm_box(self, x=None, y=None):
        '''
        :param x: string:: message to show ask user eg: Do you want a Second Wife?
        :param y: string:: command to execute on pressing confirm button
        :return: None
        '''
        if hou.ui.displayConfirmation(self.x, suppress=hou.confirmType.OverwriteFile):
            print y
    def get_name(self,x=None):
        '''
        :param x: string:: houdini node eg: <hou.ObjNode of type geo at /obj/Ship>
        :return: string:: node name eg: "Ship"
        '''
        var_a = self.x
        return var_a.name()
    def get_path(self,x=None):
        '''
        :param x: string:: houdini node eg: <hou.ObjNode of type geo at /obj/Ship>
        :return: string:: node name eg: "/obj/Ship"
        '''
        var_a = self.x
        return var_a.path()
    def get_sel(self):
        '''
        :return: string:: the path of selected node in houdini eg: '/obj/Ship1/Portuguese_ship_001'
        '''
        return hou.selectedItems()[0].path()



class MkrConnectClass(MkrCommonClass):
    def connect_nodes(self, x=None,y=None):
        '''
        :param x: string:: the node b to connect from the node y. eg: <hou.ObjNode of type geo at /obj/Ship>/ship_material>
        :param y: string:: the node a to connect to node x. eg: <hou.ObjNode of type geo at /obj/Ship>/alembic1>
        :return: None
        '''
        if "/obj" in self.x:
            var_a = hou.node(self.x)
        else:
            var_a = hou.node("/obj" + "/" + self.x)
        if "/obj" in y:
            var_c = hou.node(y)
        else:
            var_c = hou.node("/obj"+"/"+y)
        return var_a.setInput(0,var_c,0)

class MkrModifyClass(MkrCommonClass):
    def modify_parm(self, x=None, y=None, z=None, e=None, o=None):
        '''
        :param x: string::  houdini node name set attribute eg: Ship_transform, Char_transform
        :param y: string:: houdini node's attribute eg: "soho_diskfile"
        :param z: string:: value to replace or add in the node's attribute
        :param o: bool:: if True do not add "/obj" in var_a, else add "obj"
        :return: None
        '''
        if o==True:
            var_b = hou.node(self.x)
        else:
            var_b = hou.node("obj" + "/" + self.x)
        var_c = var_b.parm(y)
        if e==True:
            var_c.setExpression(expression=z, language=None)
        else:
            return var_c.set(z)
    def set_display(self,x=None,z=None,o=None):
        '''
        :param x: string:: opject path to turn on selectoon eg: "/obj/Ship/alembic"
        :param z: string:: value to set eg: 1
        :param o: bool:: if True do not add "/obj" in var_a, else add "obj"
        :return: None
        '''
        if o==True:
            var_a = hou.node(self.x)
        else:
            var_a = hou.node("obj" + "/" + self.x)
        var_a.setDisplayFlag(z)
        var_a.setRenderFlag(z)
        var_a.setSelectableTemplateFlag(z)
        var_a.setTempleteFlag(z)
        return None

class MkrCopyClass(MkrCommonClass):
    def copy_node(self, x=None, y=None):
        '''
        :param x: string:: the node to copy eg: <hou.SopNode of type material at /obj/alembic1/material2>
        :param y: string:: the node to copy inside, means the other parent group eg: <hou.ObjNode of type geo at /obj/Ship>
        :return: None
        '''
        var_a=hou.node(self.x)
        var_b = hou.node("/obj/"+y)
        return var_a.copyTo(var_b)

class MkrAlembicClass(MkrCommonClass):
    def gather_abc_nodes(self, x=None):
        '''
        :param x: string:: any node to get its child nodes eg: "/obj" or "/obj/ship_alembic"
        :return: dict:: all detatis of alembic nodes { 'geo_path': var_b, 'abc_path':self.get_path(self.x),}
        '''
        ''' :returns all items inside /obj eg: <hou.ObjNode of type geo at /obj/Ship> '''
        var_a = self.get_path(self.x)
        var_b = self.get_name(self.x)
        print "var_b: ", var_b
        ''' :returns i.path() /obj/Ship '''
        self.x = var_a
        grand_sons = self.get_childs(self.x)
        ''' :returns children nodes inside the /obj/Ship <hou.ObjNode of type geo at /obj/Ship>, <hou.ObjNode of type alembicxform at /obj/alembicxform2>, '''
        if grand_sons:
            for f in grand_sons:
                self.x=f
                var_c = self.get_cache_value(self.x)
                ''' :returns alembic cache eg: file.abc '''
                my_dict = {'geo_path': var_b, 'abc_path': self.get_path(self.x), 'abc_value': var_c, 'obj_path': var_a}
                ''' :returns dictionary '''
                return my_dict
        else:
            var_c = None
            var_d = None
            my_dict = {'geo_path': var_b, 'abc_path': var_d, 'abc_value': var_c, 'obj_path': var_a}
            return my_dict

    def alembicxform_func(self, x=None,):
        '''
        :param x: string:: name to rename the xform node
        :return: None
        '''
        ''' :returns crete the alembix xform node '''
        self.cr_abc_xform_node(self.x)
        return None


class MkrNetBoxClass(MkrCommonClass):
    def create_box(self,x=None, y=None):
        '''
        :param x: string:: name to create network box eg: "Ship"
        :return: string:: Network box name eg:<hou.NetworkBox at /obj/__netbox1>
        '''
        box = self.create_net_box_cmd(self.x)
        var_a =  hou.Color(y)
        box.setColor(var_a)
        return box


















