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
#include "Outputs.h"
#include "platform.h"
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

void appInit()
{
	InitTemperature();
	InitRelays();
}

static Temperature t;
static Scheduler temp(refresh_temp, NULL, MS2ST(2000));
static void InitTemperature()
{
	t.Init(&I2CD1,I2C_TEMP_ADDRESS);
	temp.Register();
}

static const Outputs::config_t o_cfg =
{
GPIOA, 10, GPIOA, 11 };

static Outputs outs(&o_cfg);
static void InitRelays()
{
	outs.start();
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
		bool ok = ph.WriteData(KOTEL_TEMPERATURE, &tem, 2);
		bool c = outs.getCerpadlo();
		ok = ph.WriteData(KOTEL_CERPADLO, &c, 1);

	}
}

/* Callbacks ---------------------------------------------------------*/
void cerpadlo_cb(packetHandling *, nrf_commands_t, void * data, uint8_t size,
		void *)
{
	if (size != 2)
		return;

	uint16_t to = *((uint16_t*) data);
	outs.setCerpadloTimeout(to);
}

void topit_cb(packetHandling * ph, nrf_commands_t cmd, void * data,
		uint8_t size, void *userData)
{
	if (size != 1)
		return;

	uint8_t topit = *((uint8_t *) data);

	outs.topit(topit);
}

/* Callbacks table-----------------------------------------------------------*/
const packetHandling::callback_table_t phTable[] =
{
{ KOTEL_CERPADLO_TIMEOUT, cerpadlo_cb, NULL },
{ KOTEL_TOPIT, topit_cb, NULL },
{ IDLE, NULL, NULL }, };
