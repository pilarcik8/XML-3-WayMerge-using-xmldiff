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
    base_tree = load_xml(base_path)
    left_tree = load_xml(left_path)
    right_tree = load_xml(right_path)

    diff_left = main.diff_trees(base_tree, left_tree)
    diff_right = main.diff_trees(base_tree, right_tree)

    patcher = patch.Patcher()
    merged_root = patcher.patch(diff_left, base_tree)
    merged_root = patcher.patch(diff_right, merged_root)

    save_xml(etree.ElementTree(merged_root), result_path)
"""
if __name__ == "__main__":
    merge_three_way(
        base_path="base_class.xml",
        left_path="left_class.xml",
        right_path="right_class.xml",
        result_path="result_class.xml"
    )
"""

"""
if __name__ == "__main__":
    merge_three_way(
        base_path="base_set.xml",
        left_path="left_set.xml",
        right_path="right_set.xml",
        result_path="result_set.xml"
    )
"""


if __name__ == "__main__":
    merge_three_way(
        base_path="base_list.xml",
        left_path="left_list.xml",
        right_path="right_list.xml",
        result_path="result_list.xml"
    )
