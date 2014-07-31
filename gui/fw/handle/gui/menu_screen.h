#ifndef MENU_SCREEN_H
#define MENU_SCREEN_H

piris::PScreen menu_screen(main_screen_p,&mast);

void cb_enterMain(piris::PKeyEvent *, piris::PSpecialSpinBox *);
void cb_enterVoda(piris::PKeyEvent *, piris::PSpecialSpinBox *);
void cb_enterTopeni(piris::PKeyEvent *, piris::PSpecialSpinBox *);

//topeni
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(menu_topeni,MARGIN,10,"Topeni",font8_p);
const DECL_SPECIALSPINBOX_PROPERTIES(menu_topeni, 0,6,1, cb_enterTopeni, NULL,0, NULL,0,"",NULL);
DECL_SPECIAL_SPINBOX(menu_topeni,&menu_screen);

//voda
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(menu_voda,MARGIN,25,"Voda",font8_p);
const DECL_SPECIALSPINBOX_PROPERTIES(menu_voda, 0,6,1, cb_enterVoda, NULL,0, NULL,0,"",NULL);
DECL_SPECIAL_SPINBOX(menu_voda,&menu_screen);

//zpet
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(menu_zpet,MARGIN +40,140,"Zpet",font8_p);
const DECL_SPECIALSPINBOX_PROPERTIES(menu_zpet, 0,6,1, cb_enterMain, NULL,0, NULL,0,"",NULL);
DECL_SPECIAL_SPINBOX(menu_zpet,&menu_screen);

#endif // MENU_SCREEN_H
