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

void appInit()
{
	//InitTemperature();
	model.Init();
}

static Temperature t;
static Scheduler temp(refresh_temp, NULL, MS2ST(2000));
static void InitTemperature()
{
	t.Init(&I2CD2, I2C_TEMP_ADDRESS);
	temp.Register();
}

//temperature measure timeout
void refresh_temp(arg_t)
{
	static int16_t old = 0;
	static uint8_t count = 0;
	int16_t tem;
	t.RefreshTemperature();
	tem = t.GetTemperature();

	if (old != tem || count++ > 10)
	{
		count = 0;
		old = tem;
		//bool ok = ph.WriteData(KOTEL_TEMPERATURE, &tem, 2);

	}
}

/* Callbacks table-----------------------------------------------------------*/
const packetHandling::callback_table_t phTable[] =
{
{ HANDLE_MAIN_SCREEN, dataModel::mainScreenCb, &model },
{ HANDLE_HEATING_SCREEN, dataModel::heatingScreenCb, &model },
{ HANDLE_WATER_SCREEN, dataModel::waterScreenCb, &model },
{ IDLE, NULL, NULL }, };
