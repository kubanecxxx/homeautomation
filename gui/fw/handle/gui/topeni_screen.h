#ifndef TOPENI_SCREEN_H
#define TOPENI_SCREEN_H

//screen
piris::PScreen topeni_screen_week(main_screen_p,&mast);


//week/weekend
void cb_enterTopeniWeekend (piris::PKeyEvent *, piris::PSpecialSpinBox *);
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(topeni_week_day,MARGIN,10,"Po-Pa",font8_p);
const DECL_SPECIALSPINBOX_PROPERTIES(topeni_week_day, 0,6,1, cb_enterTopeniWeekend, NULL,0, NULL,0,"",NULL);
DECL_SPECIAL_SPINBOX(topeni_week_day,&topeni_screen_week);

const DECL_SPECIALSPINBOX_PROPERTIES(topeni, 0,500,5, NULL, NULL,0, NULL,3,"%3d~C",NULL);

#define DECL_TOPENI_MINUTES(name,sec_x,sec_y) \
DECL_SPECIAL_SPINBOX_SECOND_COORDINATES(name,sec_x,sec_y); \
const DECL_SPECIALSPINBOX_PROPERTIES(name, 0,59,1, NULL, NULL,0, NULL,0,"%.2u",&name##_sec)

#define DECL_TOPENI_HOURS(name,sec_x,sec_y) \
DECL_SPECIAL_SPINBOX_SECOND_COORDINATES(name,sec_x,sec_y); \
const DECL_SPECIALSPINBOX_PROPERTIES(name, 0,23,1, NULL, NULL,0, NULL,0,"%2u",&name##_sec)

#define SIZE            8
#define SIZEY           12
#define Y_MARGIN        25

#define X_HOURS1        (MARGIN)
#define X_MINUTES1      (MARGIN + SIZE * 2)
#define X_HOURS2        (MARGIN + SIZE * 8)
#define X_MINUTES2      (MARGIN + SIZE * 10)
#define X_TEMPERATURE   (MARGIN+30)

#define Y1(row)             (Y_MARGIN + SIZEY * ((2*row)))
#define Y_TEMPERATURE(row)  (Y_MARGIN + SIZEY * ((2*row)+1))
#define Y2(row,max_count)   (Y1((row - 1 + (!row * (max_count)))))

#define CREATE_ROW(prefix,row,max,screen) \
const DECL_TOPENI_HOURS(prefix##_hours##row,X_HOURS2,Y2(row,max)); \
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(prefix##_hours##row,X_HOURS1,Y1(row),"",font8_p); \
DECL_SPECIAL_SPINBOX(prefix##_hours##row,screen); \
const DECL_TOPENI_MINUTES(prefix##_minutes##row,X_MINUTES2,Y2(row,max)); \
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(prefix##_minutes##row,X_MINUTES1,Y1(row),":",font8_p);\
DECL_SPECIAL_SPINBOX(prefix##_minutes##row,screen); \
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(prefix##_t##row,X_TEMPERATURE,Y_TEMPERATURE(row),"",font8_p); \
piris::PSpecialSpinBox prefix##_t##row(topeni_sp,prefix##_t##row##_p,screen)

CREATE_ROW(topeni_week,0,4,&topeni_screen_week);
CREATE_ROW(topeni_week,1,4,&topeni_screen_week);
CREATE_ROW(topeni_week,2,4,&topeni_screen_week);
CREATE_ROW(topeni_week,3,4,&topeni_screen_week);

const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(topeni_week_back,50,140,"Zpet",font8_p);
const DECL_SPECIALSPINBOX_PROPERTIES(topeni_week_back, 0,6,1, cb, NULL,0, NULL,0,"",NULL);
DECL_SPECIAL_SPINBOX(topeni_week_back,&topeni_screen_week);

//weekend screen
piris::PScreen topeni_screen_weekend(main_screen_p,&mast);

//week/weekend
const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(topeni_weekend_day,MARGIN,10,"So-Ne",font8_p);
const DECL_SPECIALSPINBOX_PROPERTIES(topeni_weekend_day, 0,6,1, cb_enterTopeni, NULL,0, NULL,0,"",NULL);
DECL_SPECIAL_SPINBOX(topeni_weekend_day,&topeni_screen_weekend);
CREATE_ROW(topeni_weekend,0,2,&topeni_screen_weekend);
CREATE_ROW(topeni_weekend,1,2,&topeni_screen_weekend);

const DECL_COMMON_SPECIALSPINBOXWIDGET_PROPERTIES(topeni_weekend_back,50,140,"Zpet",font8_p);
const DECL_SPECIALSPINBOX_PROPERTIES(topeni_weekend_back, 0,6,1, cb, NULL,0, NULL,0,"",NULL);
DECL_SPECIAL_SPINBOX(topeni_weekend_back,&topeni_screen_weekend);


#endif // TOPENI_SCREEN_H
