/**
 * @file application.cpp
 * @author kubanec
 * @date 6. 5. 2014
 *
 */

/* Includes ------------------------------------------------------------------*/
#include "packetHandling.h"
#include "application.h"
#include "Temperature.h"
#include "scheduler.hpp"
#include "ch.h"
#include "hal.h"
#include "guiinit.h"
#include "dataModel.h"
/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/
extern packetHandling ph;
/* Private function prototypes -----------------------------------------------*/
static void InitTemperature();
static void InitRelays();

static void refresh_temp(arg_t);
/* Private functions ---------------------------------------------------------*/

dataModel model;

//int16_t connection_status;
void connection_state(bool ok)
{
	piris::PColor col;
	if (ok)
	{
		col = piris::BLUE;
		if (model.slaveConnectionStatus())
		{
			col = piris::WHITE;
			uint8_t sc = model.screensReady();
			if (sc == MODEL_READY_MASK)
				col = piris::GREEN;
		}
	}
	else
		col = piris::RED;

	gui::main_square.setColor(col);
	gui::main_square.dirty = true;
}

void getData_cb(arg_t)
{
	static uint8_t ja = 0;
	if (chTimeNow() < S2ST(180))
	{
		gui::main_countdown =  chTimeNow() / CH_FREQUENCY;
		return;
	}


	if (ja++ > 30)
	{

		ja = 0;
		model.setScreenDirty(MODEL_READY_MASK);
	}

	gui::main_countdown = (30 - ja) * 10;

	uint8_t ready = model.screensReady();

	if (ready == MODEL_READY_MASK)
		return;

	if (!(ready & MODEL_READY_HEATING_WEEKEND))
		ph.WriteData(HANDLE_GET_SCREENS, HANDLE_RELOAD_HEATING_SCREEN_WEEKEND,
				1);
	else if (!(ready & MODEL_READY_HEATING_WEEK)
			|| !(ready & MODEL_READY_HEATING_WEEK_P2))
		ph.WriteData(HANDLE_GET_SCREENS, HANDLE_RELOAD_HEATING_SCREEN_WEEK, 1);
	else if (!(ready & MODEL_READY_WATER) || !(ready & MODEL_READY_WATER_TEMP))
		ph.WriteData(HANDLE_GET_SCREENS, HANDLE_RELOAD_WATER_SCREEN, 1);
	else if (!(ready & MODEL_READY_MAIN))
		ph.WriteData(HANDLE_GET_SCREENS, HANDLE_RELOAD_MAIN_SCREEN, 1);
}

void appInit()
{
	InitTemperature();
	model.Init();
}

static Temperature t;
static Scheduler temp(refresh_temp, NULL, MS2ST(2000));
static Scheduler getData(getData_cb, NULL, S2ST(10));

static void InitTemperature()
{
	t.Init(&I2CD1, I2C_TEMP_ADDRESS);
	temp.Register();
	getData.Register();
}

//temperature measure timeout
void refresh_temp(arg_t)
{
	static int16_t old = 0;
	static uint8_t count = 0;
	int16_t tem;
	t.RefreshTemperature();
	tem = t.GetTemperature();

	gui::main_teplotaDoma = tem * 5;
	if (old != tem || count++ > 10)
	{
		count = 0;
		old = tem;
		//bool ok = ph.WriteData(KOTEL_TEMPERATURE, &tem, 2);
		model.sendHomeTemperature();
	}
}

/* Callbacks table-----------------------------------------------------------*/
const packetHandling::callback_table_t phTable[] =
{
{ HANDLE_MAIN_SCREEN, dataModel::mainScreenCb, &model },
{ HANDLE_HEATING_SCREEN, dataModel::heatingScreenCb, &model },
{ HANDLE_WATER_SCREEN, dataModel::waterScreenCb, &model },
{ IDLE, NULL, NULL }, };
