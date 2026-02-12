from lxml import etree
from xmldiff import main, patch
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_xml(path):
    full = os.path.join(BASE_DIR, path)
    return etree.parse(full)

def save_xml(tree, path):
    full = os.path.join(BASE_DIR, path)
    tree.write(full, pretty_print=True, encoding="utf-8", xml_declaration=True)

def merge_three_way(base_path, left_path, right_path, result_path):
    try:
        base_tree = load_xml(base_path)
        left_tree = load_xml(left_path)
        right_tree = load_xml(right_path)
    except Exception as e: 
        return False


    diff_left = main.diff_trees(base_tree, left_tree)
    diff_right = main.diff_trees(base_tree, right_tree)

    patcher = patch.Patcher()
    merged_root = patcher.patch(diff_left, base_tree)
    merged_root = patcher.patch(diff_right, merged_root)

    save_xml(etree.ElementTree(merged_root), result_path)
    return True


if __name__ == "__main__":
    index = 0

    inputs_dir = "inputs"
    result_dir= "results"

    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    if not os.path.exists(inputs_dir): 
        print(f"Nexistoval priečinok '{inputs_dir}' v projekte. Zaplnite ho súbormi a spustite program znovu.") 
        os.mkdir(inputs_dir)
        exit(1)

    base_path=inputs_dir + "/" + str(index) + "/base"+ str(index) +".xml"
    left_path=inputs_dir + "/" + str(index) + "/left"+ str(index) +".xml"
    right_path=inputs_dir + "/" + str(index) + "/right"+ str(index) +".xml"
    
    result_path=result_dir + "/result"+ str(index) +".xml"
    
    while merge_three_way(
        base_path=base_path,
        left_path=left_path,
        right_path=right_path,
        result_path=result_path
    ):
        index += 1
        base_path=inputs_dir + "/"+ str(index) +"/base"+ str(index) +".xml"
        left_path=inputs_dir + "/"+ str(index) +"/left"+ str(index) +".xml"
        right_path=inputs_dir + "/"+ str(index) +"/right"+ str(index) +".xml"
        result_path=result_dir + "/result"+ str(index) +".xml"
    
    if index == 0:print("Nenajdeny ziadny súbor na spracovanie.")
    else: print(f"Zpracované {index} súborov/súbory.")