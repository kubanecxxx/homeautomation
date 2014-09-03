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

static void refresh_temp(arg_t);
/* Private functions ---------------------------------------------------------*/

//relays module config structure
static const Outputs::config_t o_cfg =
{
GPIO_HEATING_RELAY_PORT, GPIO_HEATING_RELAY_PIN, GPIO_PUMP_PORT, GPIO_PUMP_PIN };
//outputs relay instance
static Outputs outs(&o_cfg);

//temperature module instance
static Temperature t;
static Scheduler temp(refresh_temp, NULL, MS2ST(2000));

void appInit()
{
	//init temperature measuring module instance
	t.Init(&I2CD1, I2C_TEMP_ADDRESS);
	temp.Register();

	//init output relays module instance
	outs.start();

	//init input of heating really enabled - gas is burning
	palSetPadMode(GPIO_FIRE_PORT, GPIO_FIRE_PIN, PAL_MODE_INPUT_PULLDOWN);
}

//temperature measure timeout
void refresh_temp(arg_t)
{
	static int16_t old = 0;
	static uint8_t count = 0;
	int16_t tem;
	t.RefreshTemperature();
	tem = t.GetTemperature();

	static uint16_t zero = 0;
	static uint16_t one = 0;
	uint8_t a = (palReadPad(GPIO_FIRE_PORT, GPIO_FIRE_PIN));

	if (a)
		one++;
	else
		zero++;

	if (old != tem || count++ > 10)
	{
		count = 0;
		old = tem;
		ph.WriteData(KOTEL_TEMPERATURE, &tem, 2);
		bool c = outs.getCerpadlo();

		uint8_t ja = c;
		if (one > zero)
			ja |= 2;
		ja |= outs.getTopitLatch() << 2;
		ph.WriteData(KOTEL_CERPADLO, &ja, 1);

		one = 0;
		zero = 0;
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

void topit_cb(packetHandling * , nrf_commands_t, void * data, uint8_t size,
		void *)
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
