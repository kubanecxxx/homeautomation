/**
 * @file serial.h
 * @author kubanec
 * @date 27. 3. 2014
 *
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef SERIAL_H_
#define SERIAL_H_

class serial
{
public:
	typedef enum
	{
		RF_SEND_PIPE = 0x00,
		RF_FLUSH_TX = 0x01,
		RF_FLUSH_RX = 0x02,
		RESET_WATCHDOG = 0x03,
		DISABLE_NEW_DATA_OUTPUT = 0x04,

		RF_NEW_DATA = 0x80,
		RF_TX_END = 0x81,
		CRC_FAILED = 0x82,
		INVALID_COMMAND = 0x83,
		HARDWARE_STARTUP = 0x84

	} commands_t;

	typedef struct
	{
		commands_t command;
		uint8_t * load;
		uint8_t size;
	} packet_t;

	typedef struct
	{
		uint8_t size;
		uint8_t load[32];
		uint8_t pipe;
		bool finished;
	} rf_packet;

	serial(SerialDriver * driver, RF24 * rf);
	void Init(void);
	void Loop(void);

private:
	SerialDriver * dr;
	RF24 * rf;
	uint8_t buffer[64];
	uint8_t idx;
	uint8_t size;
	VirtualTimer vt;
	uint8_t channel;
	systime_t elapsed;

	rf_packet ack_buffer;
	bool output_enabled;

	void doPacket(const packet_t & pac);
	void sendPacket(const packet_t & pac);
	void check(void);
	void newRFData(uint8_t pipe, uint8_t * data, uint8_t size);
	void commandPacket(commands_t com, uint8_t size = 0, uint8_t * load = NULL);
	void hop();
	static void timeout(void * d);
};

#endif /* SERIAL_H_ */
