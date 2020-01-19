import sys
import os
import random

sys.path.append("/drive/common_funcs_path")
import Show_common_funcs.Show_common_funcs as com_func
reload(com_func)

asset_a= "/drive/projects/Show/assets/Vehicles/Asset_a/published/3d/lookdev/abc/skin_Mesh.abc"
asset_b= "/drive/projects/Show/assets/Vehicles/Asset_b/published/3d/lookdev/abc/SkinMesh_v01.abc"
shaders_path = "/drive/Show/Shaders/"
all_matnets_path = "/drive/Show/Shaders/matnets/"

def connect_xform_func(vehicle, vehicle_transform_object, lookfile):
    '''
    This function create alembic xform nodes for asset_names
    :return: None
    '''
    all_childs = com_func.ShowCommonClass(x="/obj").get_childs()
    ''' all_childs :returns all nodes under /obj eg: <hou.ObjNode of type geo at /obj/asset_name>'''
    for d in all_childs:
        abc_node = com_func.ShowAlembicClass(x=d).gather_abc_nodes()
        ''' abc_node :returns  
        {'abc_path': '/obj/asset_name/alembic1', 'abc_value': '/drive/projects/Show/assets/Veh
    icles/Asset_a/3d/artist/lookdev/maya/cache/alembic/Asset_a.
abc', 'obj_path': '/obj/asset_name', 'geo_path': 'asset_name'}
        '''
        try:
            if vehicle in abc_node["abc_value"] and "skinMesh" in abc_node["abc_value"]:
                xform_node = abc_node["geo_path"]+"_transform"
                com_func.ShowAlembicClass(x=xform_node).alembicxform_func()
                ''' create alembic xform node for asset_name '''
                com_func.ShowModifyClass(x=xform_node).modify_parm(y="fileName", z=abc_node["abc_value"], e=False, o=False)
                ''' set the xform cache path'''
                com_func.ShowModifyClass(x=xform_node).modify_parm(y="objectPath", z=vehicle_transform_object, e=False, o=False)
                ''' set the xform object path '''
                com_func.ShowModifyClass(x=xform_node).modify_parm(y="frame", z="$F", e=True, o=False)
                ''' set  the frame parameter '''
                com_func.ShowModifyClass(x=xform_node).modify_parm(y="fetchworldxform", z=1, o=False)
                ''' set the fetch '''
                com_func.ShowConnectClass(x=abc_node["geo_path"]).connect_nodes(y=xform_node)
                ''' connect the xform node to main geo nodes '''
                com_func.ShowModifyClass(x=abc_node["abc_path"]).modify_parm(y="fileName", z=lookfile, e=False, o=True)
                ''' connect the main asset_name look file alembic nodes '''
        except:
            pass
    com_func.ShowCommonClass(x="/obj").fix_layout()
    


def connect_xform():
    '''
    This function create alembic xform nodes for objects
    
    '''
    connect_xform_func(vehicle = "Asset_a", vehicle_transform_object = "/Asset_a_name_cube", lookfile = asset_a)
    connect_xform_func(vehicle = "Asset_b", vehicle_transform_object = "/Asset_b_name_Cube", lookfile = asset_b)


def material_import():
    '''
    this func import all materials to scene in the shaders path
    :return: None
    '''
    ''' :returns  all shader hip files in path eg: all_materials.hipnc, Asset_a_matnet.hip '''
    ''' import lights, ropnet and materials '''
    all_shaders = os.listdir(all_matnets_path)
    all_childs = com_func.ShowCommonClass(x="/obj").get_childs()
    if os.path.exists(all_matnets_path + "backup"):
        all_shaders.remove("backup")
    for e_shader in all_shaders:
        attrA = e_shader.replace("_matnet.hip", "")
        for e_child in all_childs:
            try:
                if attrA in e_child.name():
                    var_a = os.path.join(all_matnets_path, attrA+"_matnet.hip")
                    com_func.ShowCommonClass(x=var_a).merge_func()
                    break
            except:
                pass

    lit_file= os.path.join(shaders_path,"Light_setup.hip")
    com_func.ShowCommonClass(x=lit_file).merge_func()
    all_mats_file = os.path.join(shaders_path, "all_materials.hip")
    com_func.ShowCommonClass(x=all_mats_file).merge_func()
    ropnet_file = os.path.join(shaders_path, "ropnet.hip")
    com_func.ShowCommonClass(x=ropnet_file).merge_func()

    com_func.ShowCommonClass(x="/obj").fix_layout()

def material_connect_logic():
    '''
    connect materials to alembic nodes in the scene
    :return: None
    '''
    all_childs = com_func.ShowCommonClass(x="/obj").get_childs()
    ''' all_childs :returns all nodes under /obj eg: <hou.ObjNode of type geo at /obj/asset_name>'''
    all_materials = com_func.ShowCommonClass(x="/obj/all_materials_geo").get_childs()
    ''' :returns all materials existed in the all material node eg: <hou.SopNode of type material at /obj/all_materials_geo/Asset_a>'''
    for i in all_childs:
        for d in all_materials:
            abc_node = com_func.ShowAlembicClass(x=i).gather_abc_nodes()
            ''' abc_node :returns  
        {'abc_path': '/obj/asset_name/alembic1', 'abc_value': '/drive/projects/Show/assets/Veh
    icles/Asset_a/3d/artist/lookdev/maya/cache/alembic/Asset_a.
abc', 'obj_path': '/obj/asset_name', 'geo_path': 'asset_name'}
        '''
            try:
                if d.name() in abc_node["abc_value"]:
                    var_a = d.path()
                    ''' :returns eg:/obj/all_materials_geo/Asset_a'''
                    com_func.ShowCopyClass(x=var_a).copy_node(y=abc_node["geo_path"])
                    ''' copy the material node into alembic geo node '''
                    var_c = com_func.ShowCommonClass(x=None).get_sel()
                    ''' get the name of selected material inside geo node eg: /obj/asset_name/alembic1/Asset_a '''
                    com_func.ShowConnectClass(x=var_c).connect_nodes(y=abc_node["abc_path"])
                    ''' connect the material to alembic node '''
                    com_func.ShowModifyClass(x=var_c).set_display(z=1, o=True)
                    ''' set the dispaly and render flag to material node '''
                    var_b = "/obj/" + abc_node["geo_path"]
                    com_func.ShowCommonClass(x=var_b).fix_layout()
                    ''' fix the layout inside the alembic node '''
            except:
                pass
	    com_func.ShowCommonClass(x=abc_node["obj_path"]).fix_layout()


def box_setup_logic(matnet_name, netbox_name, geo_name):
    '''
    :param matnet_name: matnet to search in the houdini eg: "Asset_a_matnet"
    :param netbox_name: netbox name to create in houdini eg: "asset_name"
    :param geo_name: alembic geo name to search in houdini eg: "asset_name"
    :return: None
    '''
    all_childs = com_func.ShowCommonClass(x="/obj").get_childs()
    red = random.uniform(0.1,0.6)
    green = random.uniform(0.1, 0.6)
    blue = random.uniform(0.1, 0.6)
    for i in all_childs:
        if matnet_name in i.name():
            asset_name_net_box = com_func.ShowNetBoxClass(x=netbox_name).create_box(y=(float(red), float(green), float(blue)))
            for i in all_childs:
                abc_node = com_func.ShowAlembicClass(x=i).gather_abc_nodes()
                if geo_name in abc_node["geo_path"]:
                    asset_name_net_box.addItem(i)
                    asset_name_net_box.fitAroundContents()

def set_netbox():
    '''
    create and connect the network box in the scene
    :return: None
    '''
    box_setup_logic(matnet_name="Asset_a_matnet", netbox_name="Asset_a_name", geo_name="Asset_a_name")
    box_setup_logic(matnet_name="Asset_b_matnet", netbox_name="Asset_b_name", geo_name="Asset_b_name")
    box_setup_logic(matnet_name="Bag_a_matnet", netbox_name="Bag_a", geo_name="Bag_a")
    box_setup_logic(matnet_name="Bag_b_matnet", netbox_name="Bag_b", geo_name="Bag_b")


    all_childs = com_func.ShowCommonClass(x="/obj").get_childs()
    matnet_netbox = com_func.ShowNetBoxClass(x="all_matnets").create_box(y=(0.4,.5,.2))
    for i in all_childs:
        abc_node = com_func.ShowAlembicClass(x=i).gather_abc_nodes()
        if "matnet" in abc_node["geo_path"] or "all_materials_geo" in abc_node["geo_path"]:
            matnet_netbox.addItem(i)
            matnet_netbox.fitAroundContents()






