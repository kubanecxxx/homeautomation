#ifndef TABLE_CONF__
#define TABLE_CONF__

#include "chtypes.h"

typedef enum nrf_commands_t
{
//slave wants to read value
	READ_FLAG = 0x0000,
//slave wants to write value
//master write value to slave
	WRITE_FLAG = 0x8000,

// commands
	IDLE = 0xffff,
	STARTUP = 10000,
	MCU_RESET = 10001,

//basic time commands
	TIME_HOURS = 1,
	TIME_MINUTES = 2,
	TIME_SECONDS = 3,

	DATE_DAY = 4,
	DATE_MONTH = 5,
	DATE_YEAR = 6,
	DATE_WEEK_DAY = 7,
	DATE_YEAR_DAY = 8,

//termostat
	KOTEL_TOPIT = 100,			//payload 1byte 1-topit 0-netopit
	KOTEL_TEMPERATURE = 101,	//payload 2byte temperature * 10
	KOTEL_CERPADLO = 102,		//payload 1byte 1-cerpadlo jede 0-cerpadlo nejede
	KOTEL_CERPADLO_TIMEOUT = 103, //payload 2byte - timeout v sekundach


//handle
	HANDLE_MAIN_SCREEN = 200,
	HANDLE_WATER_SCREEN = 201,
	HANDLE_HEATING_SCREEN = 202,


	DATA_ERROR = 500,
	DATA_COUNT_ERROR = 501
} nrf_commands_t;

typedef struct config_table_t
{
	uint64_t address;
	uint16_t channel;
	uint8_t pipe;

} config_table_t;

extern const config_table_t config_table_kotel;
extern const config_table_t config_table_handle;

#endif
