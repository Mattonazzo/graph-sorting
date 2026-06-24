from core.constants import WINDOW_SIZE, myWin
from pages.dag_page import DAG_page
from controllers.ui_controllers import check_action
from patches.turtle_patches import *

def main() -> None:
    myWin.setup(width=WINDOW_SIZE[0],height=WINDOW_SIZE[1])
    turtle.tracer (False)

    DAG_page ()

    turtle.update()
    myWin.onclick(check_action)
    myWin.mainloop()

if __name__ == "__main__":
    main()
