from lxml import etree
from xmldiff import main as xmldiff_main, patch
import os


def user_input_dir_to_files():
    print("Vložte absolútnu cestu k priečinku so súbormi")

    while True:
        input_path = input()

        if not input_path or input_path.strip() == "":
            print("Zadajte platnú cestu (nie prázdnu). Skúste znova:")
            continue

        input_path = input_path.strip().strip('"')
        full_path = os.path.abspath(input_path)

        if not os.path.isdir(full_path):
            print(f"Adresár neexistuje: {full_path}. Skontrolujte cestu a skúste znova:")
            continue

        return full_path


def load_xml(full_path):
    return etree.parse(full_path)


def save_xml(tree, full_path):
    tree.write(full_path, pretty_print=True, encoding="utf-8", xml_declaration=True)


def merge_three_way(base_path, left_path, right_path, result_path):
    base_tree = load_xml(base_path)
    left_tree = load_xml(left_path)
    right_tree = load_xml(right_path)

    diff_left = xmldiff_main.diff_trees(base_tree, left_tree)
    diff_right = xmldiff_main.diff_trees(base_tree, right_tree)

    patcher = patch.Patcher()
    merged_root = patcher.patch(diff_left, base_tree)
    merged_root = patcher.patch(diff_right, merged_root)

    save_xml(etree.ElementTree(merged_root), result_path)


def main():
    DirWithFiles = user_input_dir_to_files()
    result_dir = os.path.join(DirWithFiles, "results")

    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    iteration = 0
    errored_files = []

    while True:

        base_path = os.path.join(DirWithFiles, str(iteration), f"base{iteration}.xml")
        left_path = os.path.join(DirWithFiles, str(iteration), f"left{iteration}.xml")
        right_path = os.path.join(DirWithFiles, str(iteration), f"right{iteration}.xml")
        result_path = os.path.join(result_dir, f"mergedResult{iteration}.xml")

        if not (os.path.isfile(base_path) and
                os.path.isfile(left_path) and
                os.path.isfile(right_path)):

            print(f"Ended at iteration: {iteration}")

            if iteration == 0:
                print("Nenájdený žiadny súbor na spracovanie.")
            else:
                print(f"Počet chybne spracovaných súborov: {len(errored_files)}")

                if errored_files:
                    print("Chybné iterácie:", ", ".join(map(str, errored_files)))
                else:
                    print("None")

                conflict_percent = (len(errored_files) * 100.0) / iteration
                print(f"{conflict_percent:.2f}% konfliktov")

            break

        try:
            merge_three_way(base_path, left_path, right_path, result_path)
        except Exception as ex:
            print(f"Chyba pri mergovaní v iterácii {iteration}: {ex}")
            errored_files.append(iteration)

        iteration += 1


if __name__ == "__main__":
    main()