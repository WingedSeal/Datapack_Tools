import datapacktools as dpt
import os, sys

EXE_DIRECTORY = os.path.join(os.path.dirname(sys.argv[0]), 'TEST', 'datapacks', 'my_datapack')
#EXE_DIRECTORY = os.path.dirname(sys.argv[0])

def run(window: dpt.Window) -> None:
    if not dpt.path.is_valid(EXE_DIRECTORY):
        window.label("Current directory is not valid, please put this file under [ saves/<world>/datapacks/<datapack> ].",20,(20,20))
        return
    
    datapack_name = dpt.path.datapack_name(EXE_DIRECTORY)
    datapack = dpt.Datapack(EXE_DIRECTORY, datapack_name, window)

    if dpt.path.is_empty(EXE_DIRECTORY):
        datapack.init()
    else:
        datapack.main()


def main() -> None:
    window = dpt.Window("Datapack Tools by WingedSeal", dpt.utils.resource_path('icon.ico'))
    run(window)
    window.root.mainloop()

if __name__ == "__main__":
    main()