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

//IRQ PC5
//CE PA2
//CS PA4
static const NRF24Config c =
{ CE_PORT, CS_PORT, CE_PIN, CS_PIN };

//no fear konstruktor se zavolá
RF24 rf(&SPID1, &c);
RF24_app ap(&rf, config_table.address + config_table.pipe_kotel,
		config_table.channel);

packetHandling ph(&ap, phTable);

static void mcu_conf();
static void enable_watchdog(void);

void clear_watchdog(void)
{
	IWDG->KR = 0xAAAA;
}

/*
 * Application entry point.
 */
systime_t sysTime;

int main(void)
{
	halInit();
	chSysInit();

	mcu_conf();

	for (int i = 0 ; i < 10; i++)
	{
		chThdSleepMilliseconds(100);
		palTogglePad(TEST_LED_PORT3,TEST_LED_PIN3);
	}

	ap.start();
	appInit();

	ph.StartAutoIdle();
	ph.setWatchdogResetFunction(clear_watchdog);
	enable_watchdog();

	while (TRUE)
	{
		Scheduler::Play();
		sysTime = chTimeNow();
		ph.HandlePacketLoop();
	}

	return 1;
}

void blik(arg_t)
{

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

static Scheduler s1(blik, NULL, MS2ST(1000));

void mcu_conf()
{
	//kruciální řádky - odpojit jtag; nechat jenom swd - sou na nem piny pro SPI1
	//premapovat SPI1 na PB3;4;5
	RCC->APB2ENR |= RCC_APB2ENR_AFIOEN;
	AFIO->MAPR |= AFIO_MAPR_SPI1_REMAP;
	AFIO->MAPR |= 0b010 << 24;

#if 1
	//setup SPI pins and spi itself
	const static SPIConfig spi_conf =
	{ NULL, CS_PORT, CS_PIN, SPI_BR };
	spiStart(&SPID1, &spi_conf);
	palSetPadMode(spi_conf.ssport, spi_conf.sspad, PAL_MODE_OUTPUT_PUSHPULL);
	palSetPadMode(SPI_SCK_PORT, SPI_SCK_PIN, SPI_SCK_MODE);
	palSetPadMode(SPI_MISO_PORT, SPI_MISO_PIN, SPI_MISO_MODE);
	palSetPadMode(SPI_MOSI_PORT, SPI_MOSI_PIN, SPI_MOSI_MODE);

	//SETUP I2C pins
	palSetPadMode(I2C_SDA_PORT, I2C_SDA_PIN2, PAL_MODE_INPUT);
	palSetPadMode(I2C_SCL_PORT, I2C_SCL_PIN2, PAL_MODE_INPUT);
	palSetPadMode(I2C_SDA_PORT, I2C_SDA_PIN,
			PAL_MODE_STM32_ALTERNATE_OPENDRAIN);
	palSetPadMode(I2C_SCL_PORT, I2C_SCL_PIN,
			PAL_MODE_STM32_ALTERNATE_OPENDRAIN);
	AFIO->MAPR |= AFIO_MAPR_I2C1_REMAP;

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

	palSetPadMode(TEST_LED_PORT, TEST_LED_PIN, PAL_MODE_OUTPUT_PUSHPULL);
	palSetPadMode(TEST_LED_PORT2, TEST_LED_PIN2, PAL_MODE_OUTPUT_PUSHPULL);
	palSetPadMode(TEST_LED_PORT3, TEST_LED_PIN3, PAL_MODE_OUTPUT_PUSHPULL);

	palSetPad(TEST_LED_PORT, TEST_LED_PIN);
	palSetPad(TEST_LED_PORT2, TEST_LED_PIN2);
	palClearPad(TEST_LED_PORT3, TEST_LED_PIN3);

	s1.Register();
}
