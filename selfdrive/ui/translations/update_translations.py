#!/usr/bin/env python3
import os
from openpilot.common.basedir import BASEDIR
from openpilot.system.ui.lib.multilang import SYSTEM_UI_DIR, UI_DIR, TRANSLATIONS_DIR, multilang
from openpilot.selfdrive.ui.translations.potools import extract_strings, generate_pot, merge_po, init_po

LANGUAGES_FILE = os.path.join(str(TRANSLATIONS_DIR), "languages.json")
POT_FILE = os.path.join(str(TRANSLATIONS_DIR), "app.pot")


def update_translations():
  files = []
  # 扫描整个 UI 代码树（system/ui 与 selfdrive/ui），覆盖 sunnypilot、mici 等所有子目录，
  # 避免遗漏未被翻译提取的界面字符串。排除 tests 与 translations 目录。
  for base_dir in (SYSTEM_UI_DIR, str(UI_DIR)):
    for root, _, filenames in os.walk(base_dir):
      if os.sep + "tests" in root or os.sep + "translations" in root:
        continue
      for filename in filenames:
        if filename.endswith(".py"):
          files.append(os.path.relpath(os.path.join(root, filename), BASEDIR))

  # Extract translatable strings and generate .pot template
  entries = extract_strings(files, BASEDIR)
  generate_pot(entries, POT_FILE)

  # Generate/update translation files for each language
  for name in multilang.languages.values():
    po_file = os.path.join(TRANSLATIONS_DIR, f"app_{name}.po")
    if os.path.exists(po_file):
      merge_po(po_file, POT_FILE)
    else:
      init_po(POT_FILE, po_file, name)


if __name__ == "__main__":
  update_translations()
