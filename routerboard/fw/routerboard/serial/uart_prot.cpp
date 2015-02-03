/**
 * @file serial.c
 * @author kubanec
 * @date 27. 3. 2014
 *
 */

/* Includes ------------------------------------------------------------------*/
#include "ch.h"
#include "hal.h"
#include "RF24.h"
#include "uart_prot.hpp"
#include <string.h>
#include "crc8.h"

static SerialConfig sdc =
{ 9600, 0, 0, 0 };

#define PREAMBLE 0x44

serial::serial(SerialDriver * driver, RF24 * r) :
		dr(driver), rf(r), idx(0), size(0), channel(0), output_enabled(true)
{
	ack_buffer.pipe = 0;
	ack_buffer.size = 0;
	ack_buffer.finished = true;
}

void serial::Init(void)
{
	palSetPadMode(UART_RX_PORT, UART_RX_PIN, UART_RX_MODE);
	palSetPadMode(UART_TX_PORT, UART_TX_PIN, UART_TX_MODE);
	sdStart(dr, &sdc);
	init_crc8();

	chThdSleepMilliseconds(1000);
	elapsed = chTimeNow();
	commandPacket(HARDWARE_STARTUP,0);
}

void serial::timeout(void *d)
{
	serial * inst = (serial*) d;
	inst->idx = 0;
}

void serial::hop(void)
{
	if (!(chTimeNow() - elapsed > MS2ST(20)))
		return;

	channel++;
	channel &= 0b1;

	rf->stopListening();
	rf->setChannel(channel + 76);
	rf->startListening();

	if ((ack_buffer.pipe / 6) == channel && ack_buffer.finished == false)
	{
		rf->writeAckPayload(ack_buffer.pipe % 6, ack_buffer.load,
				ack_buffer.size);
	}

	elapsed = chTimeNow();

	/*
	 * flush tx / load zpátky podle kanálu
	 */
}

void serial::Loop(void)
{
	check();
	//hop();

	if (sdGetWouldBlock(dr))
		return;

	uint8_t c = sdGet(dr);
	//sdPut(dr, c);
	buffer[idx++] = c;

	if (idx == 1)
	{
		if (chVTIsArmedI(&vt))
			chVTReset(&vt);
		chVTSet(&vt, MS2ST(30), timeout, this);

		if (c != PREAMBLE)
			idx = 0;
	}

	if (idx == 3)
	{
		size = c;
	}

	if (idx - 4 == size)
	{
		packet_t pac;
		if (chVTIsArmedI(&vt))
			chVTReset(&vt);
		pac.command = static_cast<commands_t>(buffer[1]);
		pac.load = &buffer[3];
		pac.size = size;
		uint8_t crc = 0;
		for (int i = 1; i < size + 4; i++)
			crc8(&crc, buffer[i]);

		if (crc == 0)
			doPacket(pac);
		else
			commandPacket(CRC_FAILED);
		idx = 0;
	}
}


void serial::ledTimeout(void * t)
{
	palClearPad(TEST_LED_PORT2, TEST_LED_PIN2);
}

void serial::check(void)
{
	uint8_t p;
	uint8_t payload[32];
	uint8_t ize;
	bool fin;
	if (rf->available(&p, &fin))
	{
		bool done = false;
		while (!done)
		{
			ize = rf->getDynamicPayloadSize();
			done = rf->read(payload, ize);
		}

		/*
		 bool rx,fail;
		 if (ack_buffer.finished == false && channel * 6 + p == ack_buffer.pipe)
		 {
		 chThdSleepMilliseconds(1500);
		 rf->whatHappened(fin,fail,rx);
		 }
		 */
		if (chVTIsArmedI(&ledVt))
		{
			chVTReset(&ledVt);
		}
		chVTSet(&ledVt,MS2ST(50),ledTimeout,this);
		palSetPad(TEST_LED_PORT2, TEST_LED_PIN2);

		if (output_enabled)
			newRFData(p, payload, ize);

	}
	if (fin)
	{
		ack_buffer.finished = true;
		commandPacket(RF_TX_END,1,&p);
	}
}

void serial::sendPacket(const packet_t & pac)
{
	uint8_t crc = 0;

	sdPut(dr, PREAMBLE);

	crc8(&crc, pac.command);
	sdPut(dr, pac.command);

	crc8(&crc, pac.size);
	sdPut(dr, pac.size);

	for (int i = 0; i < pac.size; i++)
	{
		crc8(&crc, pac.load[i]);
		sdPut(dr, pac.load[i]);
	}
	sdPut(dr, crc);
}

void serial::newRFData(uint8_t pipe, uint8_t * data, uint8_t size)
{
	packet_t pac;
	pac.command = RF_NEW_DATA;
	uint8_t load[32 + 1];
	load[0] = pipe;
	memcpy(load + 1, data, size);
	pac.load = load;
	pac.size = size + 1;

	sendPacket(pac);
}

void serial::commandPacket(commands_t com, uint8_t size, uint8_t * load)
{
	packet_t pac;
	pac.command = com;
	pac.size = size;
	pac.load = load;

	sendPacket(pac);
}

void serial::doPacket(const packet_t & pac)
{
	switch (pac.command)
	{
	case RF_SEND_PIPE:
		ack_buffer.pipe = pac.load[0];
		ack_buffer.size = pac.size - 1;
		ack_buffer.finished = false;
		memcpy(ack_buffer.load, pac.load + 1, pac.size - 1);
		rf->writeAckPayload(ack_buffer.pipe, ack_buffer.load, ack_buffer.size);
		break;
	case RF_FLUSH_RX:
		rf->flush_rx();
		break;
	case RF_FLUSH_TX:
		rf->flush_tx();
		ack_buffer.finished = true;
		break;
	case RESET_WATCHDOG:
		IWDG->KR = 0xAAAA;
		break;
	case DISABLE_NEW_DATA_OUTPUT:
		if (pac.size > 0)
			output_enabled = pac.load[0];
		break;
	default:
		commandPacket(INVALID_COMMAND);
		break;
	}
}
