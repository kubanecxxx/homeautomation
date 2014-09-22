/**
 * @file guiinit.h
 * @author kubanec
 * @date 28. 7. 2014
 *
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef GUIINIT_H_
#define GUIINIT_H_

#ifdef __cplusplus
extern "C"
{
#endif

/* Includes ------------------------------------------------------------------*/
#include "pmaster.h"
#include "pspecialspinbox.h"

namespace gui
{

/* Exported types ------------------------------------------------------------*/
/* Exported constants --------------------------------------------------------*/

extern piris::PSpecialSpinBox spin_hours;
extern piris::PSpecialSpinBox spin_minutes;
extern piris::PSpecialSpinBox spin_day;
extern piris::PSpecialSpinBox main_teplotaChtena;
extern piris::PSpecialSpinBox main_teplotaVoda;
extern piris::PSpecialSpinBox main_teplotaDoma;
extern piris::PSpecialSpinBox main_program;
extern piris::PWidget main_square;
extern piris::PSpecialSpinBox main_topi;
extern int16_t ManualTemp;
extern int16_t HeatingTemp;
extern piris::PSpecialSpinBox voda_temperature;
extern piris::PSpecialSpinBox main_countdown;

typedef struct
{
	piris::PSpecialSpinBox * hours;
	piris::PSpecialSpinBox * minutes;
	piris::PSpecialSpinBox * temperature;
} heating_row_t;

typedef struct
{
	piris::PSpecialSpinBox * hours;
	piris::PSpecialSpinBox * minutes;
} water_row_t;

/*
 extern piris::PSpecialSpinBox topeni_week_minutes0;
 extern piris::PSpecialSpinBox topeni_week_minutes1;
 extern piris::PSpecialSpinBox topeni_week_minutes2;
 extern piris::PSpecialSpinBox topeni_week_minutes3;
 extern piris::PSpecialSpinBox topeni_week_hours0;
 extern piris::PSpecialSpinBox topeni_week_hours1;
 extern piris::PSpecialSpinBox topeni_week_hours2;
 extern piris::PSpecialSpinBox topeni_week_hours3;
 extern piris::PSpecialSpinBox topeni_week_t0;
 extern piris::PSpecialSpinBox topeni_week_t1;
 extern piris::PSpecialSpinBox topeni_week_t2;
 extern piris::PSpecialSpinBox topeni_week_t3;

 extern piris::PSpecialSpinBox topeni_weekend_hours0;
 extern piris::PSpecialSpinBox topeni_weekend_hours1;
 extern piris::PSpecialSpinBox topeni_weekend_minutes0;
 extern piris::PSpecialSpinBox topeni_weekend_minutes1;
 extern piris::PSpecialSpinBox topeni_weekend_t0;
 extern piris::PSpecialSpinBox topeni_weekend_t1;
 */

extern const heating_row_t heating_week[];
extern const heating_row_t heating_weekend[];

/*
 extern piris::PSpecialSpinBox voda_startH1;
 extern piris::PSpecialSpinBox voda_startH2;
 extern piris::PSpecialSpinBox voda_startM1;
 extern piris::PSpecialSpinBox voda_startM2;

 extern piris::PSpecialSpinBox voda_stopH1;
 extern piris::PSpecialSpinBox voda_stopH2;
 extern piris::PSpecialSpinBox voda_stopM1;
 extern piris::PSpecialSpinBox voda_stopM2;
 */
extern const water_row_t water[];


/* Exported macro ------------------------------------------------------------*/
/* Exported functions --------------------------------------------------------*/
piris::PMaster * guiInit(piris::PPortingAbstract * port, size_t & size);
extern void cb_programSwitcher(piris::PKeyEvent * evt, piris::PSpecialSpinBox * spin);
}

#ifdef __cplusplus
}
#endif

#endif /* GUIINIT_H_ */
