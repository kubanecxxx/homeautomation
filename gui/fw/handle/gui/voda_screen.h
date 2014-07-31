#ifndef VODA_SCREEN_H
#define VODA_SCREEN_H

//screen
piris::PScreen voda_screen(main_screen_p,&mast);

#define VODA_X_H    (MARGIN)
#define VODA_X_M    (MARGIN + 80)
#define VODA_Y(row) (MARGIN * 2 +  SIZEY * ((row)))

//hours start1
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(voda_startH1,VODA_X_H,VODA_Y(0),"Zacit   ",font8_p);
piris::PSpecialSpinBox voda_startH1(hours_sp,voda_startH1_p,&voda_screen);
//minutes start1
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(voda_startM1,VODA_X_M,VODA_Y(0),":",font8_p);
piris::PSpecialSpinBox voda_startM1(minutes_sp,voda_startM1_p,&voda_screen);
//hours konec1
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(voda_stopH1,VODA_X_H,VODA_Y(1),"Konec   ",font8_p);
piris::PSpecialSpinBox voda_stopH1(hours_sp,voda_stopH1_p,&voda_screen);
//minutes konec1
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(voda_stopM1,VODA_X_M,VODA_Y(1),":",font8_p);
piris::PSpecialSpinBox voda_stopM1(minutes_sp,voda_stopM1_p,&voda_screen);

//hours start2
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(voda_startH2,VODA_X_H,VODA_Y(3),"Zacit   ",font8_p);
piris::PSpecialSpinBox voda_startH2(hours_sp,voda_startH2_p,&voda_screen);
//minutes start2
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(voda_startM2,VODA_X_M,VODA_Y(3),":",font8_p);
piris::PSpecialSpinBox voda_startM2(minutes_sp,voda_startM2_p,&voda_screen);
//hours konec2
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(voda_stopH2,VODA_X_H,VODA_Y(4),"Konec   ",font8_p);
piris::PSpecialSpinBox voda_stopH2(hours_sp,voda_stopH2_p,&voda_screen);
//minutes konec2
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(voda_stopM2,VODA_X_M,VODA_Y(4),":",font8_p);
piris::PSpecialSpinBox voda_stopM2(minutes_sp,voda_stopM2_p,&voda_screen);

//back
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(voda_back,50,140,"Zpet",font8_p);
const DECL_SPECIALSPINBOX_PROPERTIES(voda_back, 0,6,1, cb, NULL,0, NULL,0,"",NULL);
DECL_SPECIAL_SPINBOX(voda_back,&voda_screen);

#endif // VODA_SCREEN_H
