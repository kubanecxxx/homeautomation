#ifndef MAIN_SCREEN_H
#define MAIN_SCREEN_H

#include "pspecialspinbox.h"

//screen
const DECL_SCREEN_PROPERTIES(main_screen,piris::BLACK,piris::WHITE,piris::BLUE,&font8,1);
piris::PScreen main_screen(main_screen_p,&mast);

//hours
const DECL_SPECIALSPINBOX_PROPERTIES(hours, 0,23,1, NULL, NULL,0, NULL,0,"%2u",NULL);
const DECL_SPECIALSPINBOXWIDGET_PROPERTIES_DISABLED(hours,MARGIN,10,"",piris::INVALID,piris::INVALID,NULL,font8_p);
piris::PSpecialSpinBox spin_hours(hours_sp,hours_p,&main_screen);

//minutes
const DECL_SPECIALSPINBOX_PROPERTIES(minutes, 0,59,1, NULL, NULL,0, NULL,0,"%.2u",NULL);
const DECL_SPECIALSPINBOXWIDGET_PROPERTIES_DISABLED(minutes,MARGIN+16,10,":",piris::INVALID,piris::INVALID,NULL,font8_p);
//const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(minutes,MARGIN+16,10,":",font8_p);
piris::PSpecialSpinBox spin_minutes(minutes_sp,minutes_p,&main_screen);

//days
const char * den_table[7] =
{
    "po", "ut","st","ct","pa","so","ne"
};
const DECL_SPECIALSPINBOXWIDGET_PROPERTIES_DISABLED(day,MARGIN+90,10,"",piris::INVALID,piris::INVALID,NULL,font8_p);
const DECL_SPECIALSPINBOX_PROPERTIES(day, 0,6,1, NULL, den_table,7, NULL,0,"",NULL);
piris::PSpecialSpinBox spin_day(day_sp,day_p,&main_screen);

//program
void cb_programSwitcher(piris::PKeyEvent * evt, piris::PSpecialSpinBox * spin);
const char * program_table[5] =
{
    "Vypnuto","Manual ","Voda   ","Topeni ","Zatop  "
};
const DECL_SPECIALSPINBOXWIDGET_PROPERTIES(main_program,MARGIN,25,"",piris::INVALID,piris::INVALID,&font16,font16_p);
const DECL_SPECIALSPINBOX_PROPERTIES(main_program, 0,4,1, cb_programSwitcher, program_table,5, NULL,0,"",NULL);
DECL_SPECIAL_SPINBOX(main_program,&main_screen);

//chtena
void cb_temperature(piris::PKeyEvent * evt, piris::PSpecialSpinBox * spin);
DECL_SPECIALSPINBOXWIDGET_PROPERTIES_DISABLED(main_teplotaChtena,MARGIN+35,50,"",piris::INVALID,piris::INVALID,&font16,font16_p);
const DECL_SPECIALSPINBOX_PROPERTIES(main_teplotaChtena, 0,990,5, cb_temperature, NULL,0, NULL,2,"%3d~",NULL);
DECL_SPECIAL_SPINBOX(main_teplotaChtena,&main_screen);

//teplota1
const DECL_LABEL_PROPERTIES(main_teplotaVoda_label,MARGIN,115,"Voda",piris::INVALID,piris::INVALID,&font8,font8_p);
piris::PLabel main_teplotaVoda_label(main_teplotaVoda_label_p);
const DECL_SPECIALSPINBOXWIDGET_PROPERTIES_DISABLED(main_teplotaVoda,MARGIN+35,110,"",piris::INVALID,piris::INVALID,&font16,font16_p);
const DECL_SPECIALSPINBOX_PROPERTIES(main_teplotaVoda, 0,990,5, NULL, NULL,0, NULL,2,"%3d~",NULL);
DECL_SPECIAL_SPINBOX(main_teplotaVoda,&main_screen);
//teplota2
const DECL_LABEL_PROPERTIES(main_teplotaDoma_label,MARGIN,85,"Doma",piris::INVALID,piris::INVALID,&font8,font8_p);
piris::PLabel main_teplotaDoma_label(main_teplotaDoma_label_p);
const DECL_SPECIALSPINBOXWIDGET_PROPERTIES_DISABLED(main_teplotaDoma,MARGIN+35,80,"",piris::INVALID,piris::INVALID,&font16,font16_p);
const DECL_SPECIALSPINBOX_PROPERTIES(main_teplotaDoma, -500,990,5, NULL, NULL,0, NULL,2,"%3d~",NULL);
DECL_SPECIAL_SPINBOX(main_teplotaDoma,&main_screen);

void cb(piris::PKeyEvent *evt, piris::PSpecialSpinBox *spin);

//menu
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(main_menu,MARGIN,140,"MENU",font8_p);
const DECL_SPECIALSPINBOX_PROPERTIES(main_menu, 0,6,1, cb, NULL,0, NULL,0,"",NULL);
piris::PSpecialSpinBox main_menu(main_menu_sp,main_menu_p,&main_screen);



//topim/netopim
const char * topi_table[2] =
{
    "Netopim  ","Topim  "
};
const DECL_SPECIALSPINBOXWIDGET_PROPERTIES_DISABLED(main_topi,60,140,"",piris::GREEN,piris::INVALID,NULL,font8_p);
const DECL_SPECIALSPINBOX_PROPERTIES(main_topi, 0,1,1, NULL, topi_table,2, NULL,0,"",NULL);
piris::PSpecialSpinBox main_topi(main_topi_sp,main_topi_p,&main_screen);

//square
DECL_WIDGET_PROPERTIES(main_square,0,0,128,5,piris::RED);
piris::PWidget main_square(main_square_p);

#endif // MAIN_SCREEN_H
