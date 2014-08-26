/*
 ChibiOS/RT - Copyright (C) 2006-2013 Giovanni Di Sirio

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 */

#include "ch.h"
#include "hal.h"
#include "RF24.h"
#include "scheduler.hpp"
#include "RF24app.h"

#include "packetHandling.h"
#include "application.h"
#include "PirisPort.h"
#include "guiinit.h"
#include "ptypes.h"

static const NRF24Config c =
{ NRF_CE_PORT, NRF_CS_PORT, NRF_CE_PIN, NRF_CS_PIN };

//constructors must be called in this order
RF24 rf(&SPID2, &c);
RF24_app rf24_ap(&rf, config_table_handle.address + config_table_handle.pipe,
		config_table_handle.channel);

packetHandling ph(&rf24_ap, phTable);

static void mcu_conf();
static void enable_watchdog(void);

void clear_watchdog(void)
{
	IWDG->KR = 0xAAAA;
}

static const packetHandling::function_table_t ph_ft =
{ clear_watchdog, NVIC_SystemReset, connection_state };

/*
 * Application entry point.
 */
systime_t sysTime;
PirisPort port;
void blik(arg_t);
static Scheduler s1(blik, NULL, MS2ST(1000));

int main(void)
{
	halInit();
	chSysInit();

	mcu_conf();

	chThdSleepMilliseconds(100);

	port.start();

	size_t memory;
	gui::guiInit(&port, memory);

	rf24_ap.start();
	appInit();

	ph.StartAutoIdle();
	ph.setFunctionTable(&ph_ft);
	enable_watchdog();
	ph.RequestData(STARTUP);
	ph.RequestData(HANDLE_GET_SCREENS);

	gui::main_teplotaDoma = -100;

	s1.Register();
	while (TRUE)
	{
		Scheduler::Play();
		sysTime = chTimeNow();
		ph.HandlePacketLoop();
		chThdSleepMilliseconds(1);
	}

	return 1;
}

#include "dataModel.h"
extern dataModel model;

void blik(arg_t)
{

//	ph.WriteData(HANDLE_GET_SCREENS,HANDLE_RELOAD_WATER_SCREEN,1);
}

void enable_watchdog(void)
{
	//setup watchdog
	DBGMCU->CR |= DBGMCU_CR_DBG_IWDG_STOP;
	IWDG->KR = 0x5555;
	IWDG->PR = 6;
	IWDG->RLR = 0xFFF;
	IWDG->KR = 0xCCCC;
}

void port_config()
{
	//enable pin remapping
	RCC->APB2ENR |= RCC_APB2ENR_AFIOEN;

	//SETUP I2C2 pins - temperature sensor ; i2c is set inside temperature module
	palSetPadMode(I2C_SDA_PORT, I2C_SDA_PIN,
			PAL_MODE_STM32_ALTERNATE_OPENDRAIN);
	palSetPadMode(I2C_SCL_PORT, I2C_SCL_PIN,
			PAL_MODE_STM32_ALTERNATE_OPENDRAIN);
	palSetPadMode(GPIOB, 10, PAL_MODE_INPUT);
	palSetPadMode(GPIOB, 11, PAL_MODE_INPUT);
	AFIO->MAPR |= AFIO_MAPR_I2C1_REMAP;

	//disable jtag - only swd will work - app needs GPIOB3,4
	AFIO->MAPR |= 0b010 << 24;
	//input buttons pin setup
	palSetPadMode(BUTTON_DOWN_PORT, BUTTON_DOWN_PIN, PAL_MODE_INPUT_PULLDOWN);
	palSetPadMode(BUTTON_UP_PORT, BUTTON_UP_PIN, PAL_MODE_INPUT_PULLDOWN);
	palSetPadMode(BUTTON_ENTER_PORT, BUTTON_ENTER_PIN, PAL_MODE_INPUT_PULLDOWN);

	//setup SPI2 pins for NRF24
	palSetPadMode(NRF_CS_PORT, NRF_CS_PIN, PAL_MODE_OUTPUT_PUSHPULL);
	palSetPadMode(SPI_SCK_PORT, SPI_SCK_PIN, SPI_SCK_MODE);
	palSetPadMode(SPI_MISO_PORT, SPI_MISO_PIN, SPI_MISO_MODE);
	palSetPadMode(SPI_MOSI_PORT, SPI_MOSI_PIN, SPI_MOSI_MODE);
	//chip enable pin nrf24
	palSetPadMode(NRF_CE_PORT, NRF_CE_PIN, PAL_MODE_OUTPUT_PUSHPULL);

	//display pins
}

void mcu_conf()
{

#if 1
	port_config();

	//setup radio SPI2
	const static SPIConfig spi_conf =
	{ NULL, NRF_CS_PORT, NRF_CS_PIN, SPI_BR };
	spiStart(&SPID2, &spi_conf);

#else
	palSetPadMode(config.ssport, config.sspad, PAL_MODE_OUTPUT_PUSHPULL);
	palSetPadMode(SPI_SCK_PORT, SPI_SCK_PIN, PAL_MODE_OUTPUT_PUSHPULL);
	palSetPadMode(SPI_MISO_PORT, SPI_MISO_PIN, PAL_MODE_OUTPUT_PUSHPULL);
	palSetPadMode(SPI_MOSI_PORT, SPI_MOSI_PIN, PAL_MODE_OUTPUT_PUSHPULL);

	palClearPad(config.ssport, config.sspad);
	palClearPad(SPI_SCK_PORT, SPI_SCK_PIN);
	palClearPad(SPI_MISO_PORT, SPI_MISO_PIN);
	palClearPad(SPI_MOSI_PORT, SPI_MOSI_PIN);

	palSetPad(config.ssport, config.sspad);
	palClearPad(config.ssport, config.sspad);
	palClearPad(SPI_SCK_PORT, SPI_SCK_PIN);
	palClearPad(SPI_MISO_PORT, SPI_MISO_PIN);
	palClearPad(SPI_MOSI_PORT, SPI_MOSI_PIN);
	palSetPad(SPI_SCK_PORT, SPI_SCK_PIN);
	palClearPad(config.ssport, config.sspad);
	palClearPad(SPI_SCK_PORT, SPI_SCK_PIN);
	palClearPad(SPI_MISO_PORT, SPI_MISO_PIN);
	palClearPad(SPI_MOSI_PORT, SPI_MOSI_PIN);
	palSetPad(SPI_MISO_PORT, SPI_MISO_PIN);
	palClearPad(config.ssport, config.sspad);
	palClearPad(SPI_SCK_PORT, SPI_SCK_PIN);
	palClearPad(SPI_MISO_PORT, SPI_MISO_PIN);
	palClearPad(SPI_MOSI_PORT, SPI_MOSI_PIN);
	palSetPad(SPI_MOSI_PORT, SPI_MOSI_PIN);
	palClearPad(config.ssport, config.sspad);
	palClearPad(SPI_SCK_PORT, SPI_SCK_PIN);
	palClearPad(SPI_MISO_PORT, SPI_MISO_PIN);
	palClearPad(SPI_MOSI_PORT, SPI_MOSI_PIN);

	//
#endif

	//palSetPad(TEST_LED_PORT, TEST_LED_PIN);

}
