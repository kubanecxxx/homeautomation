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
#include "nRF24L01.h"
#include "uart_prot.hpp"
#include "time.h"

static SPIConfig config =
{ NULL, CS_PORT, CS_PIN, SPI_BR };

//IRQ PC5
//CE PA2
//CS PA4
static NRF24Config c =
{ CE_PORT, CS_PORT, CE_PIN, CS_PIN };

//no fear konstruktor se zavolá
RF24 rf(&SPID1, &c);

static const uint64_t pipe = 0x7878787878LL;

void blik(arg_t)
{

	static int16_t ja = 0;
	static int16_t inc = 10;
	//palTogglePad(TEST_LED_PORT, TEST_LED_PIN);

	if (ja > 800)
		inc = -10;
	if (ja < 30)
		inc = 10;

	ja = ja + inc;

	pwmEnableChannel(&PWMD2, 2, PWM_PERCENTAGE_TO_WIDTH(&PWMD2, ja));
}

/*
 * PWM configuration structure.
 * Cyclic callback enabled, channels 3 and 4 enabled without callbacks,
 * the active state is a logic one.
 */
static PWMConfig pwmcfg =
{ 1000000, /* 10kHz PWM clock frequency.   */
1000, /* PWM period 1S (in ticks).    */
NULL,
{
{ PWM_OUTPUT_DISABLED, NULL },
{ PWM_OUTPUT_DISABLED, NULL },
{ PWM_OUTPUT_ACTIVE_HIGH, NULL },
{ PWM_OUTPUT_DISABLED, NULL } },
/* HW dependent part.*/
0, 0,
#if STM32_PWM_USE_ADVANCED
		0
#endif
	};

/*
 * Application entry point.
 */
systime_t sysTime;

static Scheduler s1(blik, NULL, MS2ST(10));
static serial ser(&SD1, &rf);

int main(void)
{

	halInit();
	chSysInit();

	//kruciální řádky - odpojit jtag; nechat jenom swd - sou na nem piny pro SPI1
	//premapovat SPI1 na PB3;4;5
	RCC->APB2ENR |= RCC_APB2ENR_AFIOEN;
	AFIO->MAPR |= AFIO_MAPR_SPI1_REMAP;
	AFIO->MAPR |= 0b010 << 24;

#if 1
	spiStart(&SPID1, &config);
	palSetPadMode(config.ssport, config.sspad, PAL_MODE_OUTPUT_PUSHPULL);
	palSetPadMode(SPI_SCK_PORT, SPI_SCK_PIN, SPI_SCK_MODE);
	palSetPadMode(SPI_MISO_PORT, SPI_MISO_PIN, SPI_MISO_MODE);
	palSetPadMode(SPI_MOSI_PORT, SPI_MOSI_PIN, SPI_MOSI_MODE);

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

	palSetPadMode(TEST_LED_PORT, TEST_LED_PIN, PAL_MODE_INPUT);
	palSetPadMode(TEST_LED_PORT2, TEST_LED_PIN2, PAL_MODE_OUTPUT_PUSHPULL);

	palClearPad(TEST_LED_PORT, TEST_LED_PIN);
	palClearPad(TEST_LED_PORT2, TEST_LED_PIN2);

	s1.Register();

	palSetPadMode(GPIOA, 2, PAL_MODE_STM32_ALTERNATE_PUSHPULL);
//	palSetPad(GPIOA,2);
	//DBGMCU->CR |= DBGMCU_CR_DBG_TIM2_STOP;
	pwmStart(&PWMD2, &pwmcfg);
	pwmEnableChannel(&PWMD2,2,PWM_PERCENTAGE_TO_WIDTH(&PWMD2,5000));

	//setup watchdog
	DBGMCU->CR |= DBGMCU_CR_DBG_IWDG_STOP;
	IWDG->KR = 0x5555;
	IWDG->PR = 6;
	IWDG->RLR = 0xFFF;
	IWDG->KR = 0xCCCC;

#if 1
	ser.Init();

	rf.begin();
	rf.enableAckPayload();
	rf.enableDynamicPayloads();
	for (int i = 0; i < 5; i++)
		rf.openReadingPipe(i, pipe + i);
	rf.startListening();

#endif
	while (TRUE)
	{
		Scheduler::Play();
		ser.Loop();
		sysTime = chTimeNow();
	}

	return 1;
}

