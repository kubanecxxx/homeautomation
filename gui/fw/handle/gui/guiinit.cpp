#include "PirisPort.h"
#include "pkeyevent.h"
#include "pwidget.h"
#include "pmaster.h"
#include "pscreen.h"
#include "qdebugprint.h"
#include "pbutton.h"
#include "pfont.h"
#include "ptouchevent.h"
#include "plabel.h"
#include "pcheckbox.h"
#include "pspecialspinbox.h"
#include "guiinit.h"

#include "hal.h"
#include "PwmBacklight.h"

#define MARGIN  5
//fonts
static const DECL_FONT(font8_p,NULL,8,8);
static const DECL_FONT(font16_p,NULL,16,16);
piris::PFont font8(font8_p);
piris::PFont font16(font16_p);

//main
piris::PKeyEvent e;
piris::PTouchEvent t;
piris::PMaster mast(&e, &t);

namespace gui
{

/*********************************************************
 * main screen object declaration
 *********************************************************/
#include "main_screen.h"

/*********************************************************
 * menu screen
 *********************************************************/
#include "menu_screen.h"

/*********************************************************
 * topeni screen
 *********************************************************/
#include "topeni_screen.h"

/*********************************************************
 * voda screen
 *********************************************************/
#include "voda_screen.h"

const heating_row_t heating_week[4] =
{
{ &topeni_week_hours0, &topeni_week_minutes0, &topeni_week_t0 },
{ &topeni_week_hours1, &topeni_week_minutes1, &topeni_week_t1 },
{ &topeni_week_hours2, &topeni_week_minutes2, &topeni_week_t2 },
{ &topeni_week_hours3, &topeni_week_minutes3, &topeni_week_t3 } };

const heating_row_t heating_weekend[2] =
{
{ &topeni_weekend_hours0, &topeni_weekend_minutes0, &topeni_weekend_t0 },
{ &topeni_weekend_hours1, &topeni_weekend_minutes1, &topeni_weekend_t1 } };

const water_row_t water[4] =
{
{ &voda_startH1, &voda_startM1 },
{ &voda_stopH1, &voda_stopM1 },
{ &voda_startH2, &voda_startM2 },
{ &voda_stopH2, &voda_stopM2 } };


WORKING_AREA(gui_thd, 1024);

msg_t thd_gui(void* a)
{
	piris::PMaster * g = (piris::PMaster*) a;
	while (TRUE)
	{
		g->main();
	}
}

piris::PMaster * guiInit(piris::PPortingAbstract * port, size_t & size)
{
	/*
	 spin_hours.name = "hodiny";
	 spin_minutes.name = "minuty";
	 spin_day.name = "day";
	 main_menu.name = "menu";
	 main_screen.name = "main";
	 main_topi.name = "topi";
	 menu_screen.name = "menu";
	 */

	PwmBacklight::Init();
    main_screen.addChild(&main_teplotaVoda_label);
    main_screen.addChild(&main_teplotaDoma_label);

    main_screen.addChild(&main_square);
    main_square.setSelectable(false);
    main_square.setEnabled(false);

	main_menu.setToggleable(false);
	menu_topeni.setToggleable(false);
	menu_voda.setToggleable(false);
	menu_zpet.setToggleable(false);
	topeni_weekend_day.setToggleable(false);
	topeni_week_day.setToggleable(false);
	topeni_weekend_back.setToggleable(false);
	topeni_week_back.setToggleable(false);
	voda_back.setToggleable(false);

	main_screen.makeActive();

	main_screen.setFocusWidget(&main_program);
	menu_screen.setFocusWidget(&menu_topeni);
	topeni_screen_week.setFocusWidget(&topeni_week_day);
	topeni_screen_weekend.setFocusWidget(&topeni_weekend_day);
	voda_screen.setFocusWidget(&voda_startH1);

	mast.setHW(port);

	size = main_screen.dataSize();
	size += menu_screen.dataSize();
	size += topeni_screen_week.dataSize();
	size += topeni_screen_weekend.dataSize();
	size += voda_screen.dataSize();

	chThdCreateStatic(&gui_thd, 1024, LOWPRIO, thd_gui, &mast);

	return &mast;
}

void cb(piris::PKeyEvent *, piris::PSpecialSpinBox *)
{
	menu_screen.makeActive();
}

void cb_enterMain(piris::PKeyEvent *, piris::PSpecialSpinBox *)
{
	main_screen.makeActive();
}

void cb_enterTopeni(piris::PKeyEvent *, piris::PSpecialSpinBox *)
{
	topeni_screen_week.makeActive();
}

void cb_enterTopeniWeekend(piris::PKeyEvent *, piris::PSpecialSpinBox *)
{
	topeni_screen_weekend.makeActive();
}

void cb_enterVoda(piris::PKeyEvent *, piris::PSpecialSpinBox *)
{
	voda_screen.makeActive();
}

int16_t temp = 200;
int16_t temp2 = 400;

void cb_programSwitcher(piris::PKeyEvent * evt, piris::PSpecialSpinBox * spin)
{
	uint8_t s = spin->val();

	//zatop
	if (s == 4 && !spin->toggled() && evt->key == kENTER)
	{
		//spin->setHidden(true);
		//zablikat a aktivovat
		return;
	}

	if (!spin->toggled() || evt->key == kENTER)
		return;

	//deaktivovat pokud aktivováno

	//manual
	if (s == 1)
	{
		main_teplotaChtena.setHidden(false);
		main_teplotaChtena.setEnabled(true);
		main_teplotaChtena.setValue(temp);
	}
	//topeni
	else if (s == 3)
	{
		main_teplotaChtena.setHidden(false);
		main_teplotaChtena.setEnabled(false);
		main_teplotaChtena.setValue(temp2);
	}
	else
	{
		main_teplotaChtena.setHidden(true);
		main_teplotaChtena.setEnabled(false);
	}

	main_teplotaChtena.dirty = true;
}

void cb_temperature(piris::PKeyEvent * evt, piris::PSpecialSpinBox * spin)
{
	if (evt->key != kENTER)
		return;

	temp = spin->val();
}

}

