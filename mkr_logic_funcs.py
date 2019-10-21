import sys
import os
import random

sys.path.append("/aslan/projects/Custom_scripts/Girijashankar/Codes/marakkar")
import Mkr_common_funcs.mkr_common_funcs as com_func
reload(com_func)

Portuguese_ship_look_file= "/aslan/projects/Marakkar/assets/Vehicles/Portuguese_ship_001/published/3d/lookdev/abc/skin_Mesh.abc"
Zamourain_ship_look_file= "/aslan/projects/Marakkar/assets/Vehicles/Zamourain_ship_001/published/3d/lookdev/abc/SkinMesh_v01.abc"
shaders_path = "/aslan/projects/Custom_scripts/Girijashankar/Codes/marakkar/Shaders/"
all_matnets_path = "/aslan/projects/Custom_scripts/Girijashankar/Codes/marakkar/Shaders/matnets/"

def connect_xform_func(vehicle, vehicle_transform_object, lookfile):
    '''
    This function create alembic xform nodes for ships
    :return: None
    '''
    all_childs = com_func.MkrCommonClass(x="/obj").get_childs()
    ''' all_childs :returns all nodes under /obj eg: <hou.ObjNode of type geo at /obj/Ship>'''
    for d in all_childs:
        abc_node = com_func.MkrAlembicClass(x=d).gather_abc_nodes()
        ''' abc_node :returns  
        {'abc_path': '/obj/Ship/alembic1', 'abc_value': '/aslan/projects/Marakkar/assets/Veh
    icles/Portuguese_ship_001/3d/deepakk/lookdev/maya/cache/alembic/Portuguese_ship_001.
abc', 'obj_path': '/obj/Ship', 'geo_path': 'Ship'}
        '''
        try:
            if vehicle in abc_node["abc_value"] and "skinMesh" in abc_node["abc_value"]:
                xform_node = abc_node["geo_path"]+"_transform"
                com_func.MkrAlembicClass(x=xform_node).alembicxform_func()
                ''' create alembic xform node for ship '''
                com_func.MkrModifyClass(x=xform_node).modify_parm(y="fileName", z=abc_node["abc_value"], e=False, o=False)
                ''' set the xform cache path'''
                com_func.MkrModifyClass(x=xform_node).modify_parm(y="objectPath", z=vehicle_transform_object, e=False, o=False)
                ''' set the xform object path '''
                com_func.MkrModifyClass(x=xform_node).modify_parm(y="frame", z="$F", e=True, o=False)
                ''' set  the frame parameter '''
                com_func.MkrModifyClass(x=xform_node).modify_parm(y="fetchworldxform", z=1, o=False)
                ''' set the fetch '''
                com_func.MkrConnectClass(x=abc_node["geo_path"]).connect_nodes(y=xform_node)
                ''' connect the xform node to main geo nodes '''
                com_func.MkrModifyClass(x=abc_node["abc_path"]).modify_parm(y="fileName", z=lookfile, e=False, o=True)
                ''' connect the main ship look file alembic nodes '''
        except:
            pass
    com_func.MkrCommonClass(x="/obj").fix_layout()
    


def connect_xform():
    '''
    This function create alembic xform nodes for objects
    
    '''
    connect_xform_func(vehicle = "Portuguese_ship_001", vehicle_transform_object = "/Portuguese_ship_cube", lookfile = Portuguese_ship_look_file)
    connect_xform_func(vehicle = "Zamourain_ship_001", vehicle_transform_object = "/Zamourain_ship_Cube", lookfile = Zamourain_ship_look_file)


def material_import():
    '''
    this func import all materials to scene in the shaders path
    :return: None
    '''
    ''' :returns  all shader hip files in path eg: all_materials.hipnc, Portuguese_ship_001_matnet.hip '''
    ''' import lights, ropnet and materials '''
    all_shaders = os.listdir(all_matnets_path)
    all_childs = com_func.MkrCommonClass(x="/obj").get_childs()
    if os.path.exists(all_matnets_path + "backup"):
        all_shaders.remove("backup")
    for e_shader in all_shaders:
        attrA = e_shader.replace("_matnet.hip", "")
        for e_child in all_childs:
            try:
                if attrA in e_child.name():
                    var_a = os.path.join(all_matnets_path, attrA+"_matnet.hip")
                    com_func.MkrCommonClass(x=var_a).merge_func()
                    break
            except:
                pass

    lit_file= os.path.join(shaders_path,"Light_setup.hip")
    com_func.MkrCommonClass(x=lit_file).merge_func()
    all_mats_file = os.path.join(shaders_path, "all_materials.hip")
    com_func.MkrCommonClass(x=all_mats_file).merge_func()
    ropnet_file = os.path.join(shaders_path, "ropnet.hip")
    com_func.MkrCommonClass(x=ropnet_file).merge_func()

    com_func.MkrCommonClass(x="/obj").fix_layout()

def material_connect_logic():
    '''
    connect materials to alembic nodes in the scene
    :return: None
    '''
    all_childs = com_func.MkrCommonClass(x="/obj").get_childs()
    ''' all_childs :returns all nodes under /obj eg: <hou.ObjNode of type geo at /obj/Ship>'''
    all_materials = com_func.MkrCommonClass(x="/obj/all_materials_geo").get_childs()
    ''' :returns all materials existed in the all material node eg: <hou.SopNode of type material at /obj/all_materials_geo/Portuguese_ship_001>'''
    for i in all_childs:
        for d in all_materials:
            abc_node = com_func.MkrAlembicClass(x=i).gather_abc_nodes()
            ''' abc_node :returns  
        {'abc_path': '/obj/Ship/alembic1', 'abc_value': '/aslan/projects/Marakkar/assets/Veh
    icles/Portuguese_ship_001/3d/deepakk/lookdev/maya/cache/alembic/Portuguese_ship_001.
abc', 'obj_path': '/obj/Ship', 'geo_path': 'Ship'}
        '''
            try:
                if d.name() in abc_node["abc_value"]:
                    var_a = d.path()
                    ''' :returns eg:/obj/all_materials_geo/Portuguese_ship_001'''
                    com_func.MkrCopyClass(x=var_a).copy_node(y=abc_node["geo_path"])
                    ''' copy the material node into alembic geo node '''
                    var_c = com_func.MkrCommonClass(x=None).get_sel()
                    ''' get the name of selected material inside geo node eg: /obj/Ship/alembic1/Portuguese_ship_001 '''
                    com_func.MkrConnectClass(x=var_c).connect_nodes(y=abc_node["abc_path"])
                    ''' connect the material to alembic node '''
                    com_func.MkrModifyClass(x=var_c).set_display(z=1, o=True)
                    ''' set the dispaly and render flag to material node '''
                    var_b = "/obj/" + abc_node["geo_path"]
                    com_func.MkrCommonClass(x=var_b).fix_layout()
                    ''' fix the layout inside the alembic node '''
            except:
                pass
	    com_func.MkrCommonClass(x=abc_node["obj_path"]).fix_layout()


def box_setup_logic(matnet_name, netbox_name, geo_name):
    '''
    :param matnet_name: matnet to search in the houdini eg: "Portuguese_ship_001_matnet"
    :param netbox_name: netbox name to create in houdini eg: "Ship"
    :param geo_name: alembic geo name to search in houdini eg: "ship"
    :return: None
    '''
    all_childs = com_func.MkrCommonClass(x="/obj").get_childs()
    red = random.uniform(0.1,0.6)
    green = random.uniform(0.1, 0.6)
    blue = random.uniform(0.1, 0.6)
    for i in all_childs:
        if matnet_name in i.name():
            ship_net_box = com_func.MkrNetBoxClass(x=netbox_name).create_box(y=(float(red), float(green), float(blue)))
            for i in all_childs:
                abc_node = com_func.MkrAlembicClass(x=i).gather_abc_nodes()
                if geo_name in abc_node["geo_path"]:
                    ship_net_box.addItem(i)
                    ship_net_box.fitAroundContents()

def set_netbox():
    '''
    create and connect the network box in the scene
    :return: None
    '''
    box_setup_logic(matnet_name="Portuguese_ship_001_matnet", netbox_name="Portuguese_ship", geo_name="Portuguese_ship")
    box_setup_logic(matnet_name="Zamourain_ship_001_matnet", netbox_name="Zamourain_ship", geo_name="Zamourain_ship")
    box_setup_logic(matnet_name="Cpboatc_matnet", netbox_name="Cpboatc", geo_name="Cpboatc")
    box_setup_logic(matnet_name="Cpboate_matnet", netbox_name="Cpboate", geo_name="Cpboate")
    box_setup_logic(matnet_name="Small_rowing_boat_matnet", netbox_name="Small_rowing_boat", geo_name="Small_rowing_boat")
    box_setup_logic(matnet_name="Young_kunjali_matnet", netbox_name="Young_kunjali", geo_name="Young_kunjali")
    box_setup_logic(matnet_name="Pathu_matnet", netbox_name="Pathu", geo_name="Pathu")
    box_setup_logic(matnet_name="Arrow_001_matnet", netbox_name="Arrow_001", geo_name="Arrow_001")
    box_setup_logic(matnet_name="Bag_a_matnet", netbox_name="Bag_a", geo_name="Bag_a")
    box_setup_logic(matnet_name="Bag_b_matnet", netbox_name="Bag_b", geo_name="Bag_b")
    box_setup_logic(matnet_name="Bamboo_basket02_matnet", netbox_name="Bamboo_basket02", geo_name="Bamboo_basket02")
    box_setup_logic(matnet_name="Bamboo_basket_matnet", netbox_name="Bamboo_basket", geo_name="Bamboo_basket")
    box_setup_logic(matnet_name="Barrel_gun_matnet", netbox_name="Barrel_gun", geo_name="Barrel_gun")
    box_setup_logic(matnet_name="Big_anchor_a_matnet", netbox_name="Big_anchor_a", geo_name="Pathu")
    box_setup_logic(matnet_name="Big_barrel_a_matnet", netbox_name="Big_barrel_a", geo_name="Big_barrel_a")
    box_setup_logic(matnet_name="Bow_001_matnet", netbox_name="Bow_001", geo_name="Bow_001")
    box_setup_logic(matnet_name="Bucket_a_matnet", netbox_name="Bucket_a", geo_name="Bucket_a")
    box_setup_logic(matnet_name="Cannon_a_matnet", netbox_name="Cannon_a", geo_name="Cannon_a")
    box_setup_logic(matnet_name="Cannon_b_matnet", netbox_name="Cannon_b", geo_name="Cannon_b")
    box_setup_logic(matnet_name="Cannon_balls_with_basket_001_matnet", netbox_name="Cannon_balls_with_basket", geo_name="Cannon_balls_with_basket")
    box_setup_logic(matnet_name="Coconut_bunch_001_matnet", netbox_name="Coconut_bunch_001", geo_name="Coconut_bunch_001")
    box_setup_logic(matnet_name="Copper_pot_a_matnet", netbox_name="Copper_pot_a", geo_name="Copper_pot_a")
    box_setup_logic(matnet_name="extra_mesh_matnet", netbox_name="extra_mesh", geo_name="extra_mesh")
    box_setup_logic(matnet_name="Kunjali_sword_001_matnet", netbox_name="Kunjali_sword_001", geo_name="Kunjali_sword_001")
    box_setup_logic(matnet_name="Lantern_a_matnet", netbox_name="Lantern_a", geo_name="Lantern_a")
    box_setup_logic(matnet_name="Lantern_b_matnet", netbox_name="Lantern_b", geo_name="Lantern_b")
    box_setup_logic(matnet_name="Lantern_c_matnet", netbox_name="Lantern_c", geo_name="Lantern_c")
    box_setup_logic(matnet_name="Lantern_d_matnet", netbox_name="Lantern_d", geo_name="Lantern_d")
    box_setup_logic(matnet_name="Oil_barrel_001_matnet", netbox_name="Oil_barrel_001", geo_name="Oil_barrel_001")
    box_setup_logic(matnet_name="Pot_set_matnet", netbox_name="Pot_set", geo_name="Pot_set")
    box_setup_logic(matnet_name="Pulley_a_matnet", netbox_name="Pulley_a", geo_name="Pulley_a")
    box_setup_logic(matnet_name="Quiver_001_matnet", netbox_name="Quiver_001", geo_name="Quiver_001")
    box_setup_logic(matnet_name="Raft_matnet", netbox_name="Raft", geo_name="Raft")
    box_setup_logic(matnet_name="Small_anchor_b_matnet", netbox_name="Small_anchor_b", geo_name="Small_anchor_b")
    box_setup_logic(matnet_name="Soldier_spear_001_matnet", netbox_name="Soldier_spear_001", geo_name="Soldier_spear_001")
    box_setup_logic(matnet_name="Soldier_sword_001_matnet", netbox_name="Ship", geo_name="ship")
    box_setup_logic(matnet_name="Spear_and_flag_001_matnet", netbox_name="Soldier_sword_001", geo_name="Soldier_sword_001")
    box_setup_logic(matnet_name="Spike_ball_001_matnet", netbox_name="Spike_ball_001", geo_name="Spike_ball_001")
    box_setup_logic(matnet_name="Spike_ball_002_matnet", netbox_name="Spike_ball_002", geo_name="Spike_ball_002")
    box_setup_logic(matnet_name="Treasure_box_a_matnet", netbox_name="Treasure_box_a", geo_name="Treasure_box_a")
    box_setup_logic(matnet_name="Treasure_box_b_matnet", netbox_name="Treasure_box_b", geo_name="Treasure_box_b")
    box_setup_logic(matnet_name="Treasure_box_c_matnet", netbox_name="Treasure_box_c", geo_name="Treasure_box_c")
    box_setup_logic(matnet_name="Treasure_box_d_matnet", netbox_name="Treasure_box_d", geo_name="Treasure_box_d")
    box_setup_logic(matnet_name="Treasure_box_e_matnet", netbox_name="Treasure_box_e", geo_name="Treasure_box_e")
    box_setup_logic(matnet_name="Wooden_cannon_001_matnet", netbox_name="Wooden_cannon_001", geo_name="Wooden_cannon_001")
    box_setup_logic(matnet_name="Wooden_pot_b_matnet", netbox_name="Wooden_pot_b_", geo_name="Wooden_pot_b_")
    box_setup_logic(matnet_name="Zamourain_fire_arrow_001_matnet", netbox_name="Zamourain_fire_arrow_001", geo_name="Zamourain_fire_arrow_001")
    box_setup_logic(matnet_name="Small_barrel_a_matnet", netbox_name="Small_barrel_a", geo_name="Small_barrel_a")
    box_setup_logic(matnet_name="Small_barrel_b_matnet", netbox_name="Small_barrel_b", geo_name="Small_barrel_b")
    box_setup_logic(matnet_name="Small_barrel_c_matnet", netbox_name="Small_barrel_c", geo_name="Small_barrel_c")


    all_childs = com_func.MkrCommonClass(x="/obj").get_childs()
    matnet_netbox = com_func.MkrNetBoxClass(x="all_matnets").create_box(y=(0.4,.5,.2))
    for i in all_childs:
        abc_node = com_func.MkrAlembicClass(x=i).gather_abc_nodes()
        if "matnet" in abc_node["geo_path"] or "all_materials_geo" in abc_node["geo_path"]:
            matnet_netbox.addItem(i)
            matnet_netbox.fitAroundContents()










'''
{'abc_path': '/obj/Ship/alembic1', 'abc_value': '/aslan/projects/Marakkar/assets/Vehicles/Portuguese_shi
p_001/3d/deepakk/lookdev/maya/cache/alembic/Portuguese_ship_002.abc', 'obj_path': '/obj/Ship', 'geo_path
': 'Ship'}
None
{'abc_path': '/obj/char_01/alembic1', 'abc_value': '//aslan/projects/Marakkar/sequences/swr/swr_0010/pub
lished/3d/animation/extra_mesh/MKR_swr_0010_001_animation_v009_v001_extra_mesh.abc', 'obj_path': '/obj/c
har_01', 'geo_path': 'char_01'}
{'abc_path': '/obj/Ship1/alembic4', 'abc_value': '/aslan/projects/Marakkar/assets/Vehicles/Portuguese_sh
ip_001/3d/deepakk/lookdev/maya/cache/alembic/Portuguese_ship_002.abc', 'obj_path': '/obj/Ship1', 'geo_pa
th': 'Ship1'}
None
{'abc_path': '/obj/char_02/alembic1', 'abc_value': '//aslan/projects/Marakkar/sequences/swr/swr_0010/pub
lished/3d/animation/extra_mesh/MKR_swr_0010_001_animation_v009_v001_extra_mesh.abc', 'obj_path': '/obj/c
har_02', 'geo_path': 'char_02'}
'''


