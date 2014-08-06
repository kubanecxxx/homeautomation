/**
 * @file dataModel.h
 * @author kubanec
 * @date 4. 8. 2014
 *
 */
#ifndef DATAMODEL_H_
#define DATAMODEL_H_

#include "packetHandling.h"

typedef  struct __attribute__((__packed__))
{
	int16_t hours;
	int16_t minutes;
	int16_t dayOfWeek;
	int16_t program;
	int16_t heatingTemperature;
	int16_t manualTemperature;
	int16_t homeTemperature;
	int16_t waterTemperature;
	int16_t slaveConnectionStatus;
	int16_t heatingActive;
} dataModel_mainScreen_t ;

typedef struct __attribute__((__packed__))
{
	int16_t hours;
	int16_t minutes;
	int16_t temperature;
} dataModel_heatingScreenRow_t ;

typedef struct __attribute__((__packed__))
{
	int16_t hoursStart;
	int16_t hoursStop;
	int16_t minutesStart;
	int16_t minutesStop;
} dataModel_waterScreenRow_t ;
typedef dataModel_waterScreenRow_t dataModel_waterScreen_t[2];

class packetHandling;
class dataModel
{
public:
	void Init();
	void sendMainScreen();
	void sendWaterScreen();
	void sendHeatingScreen(bool isWeekend);
	static void mainScreenCb(packetHandling * ph, nrf_commands_t cmd,
			void * data, uint8_t size, void *userData);
	static void heatingScreenCb(packetHandling * ph, nrf_commands_t cmd,
			void * data, uint8_t size, void *userData);
	static void waterScreenCb(packetHandling * ph, nrf_commands_t cmd,
			void * data, uint8_t size, void *userData);

private:

};

#endif /* DATAMODEL_H_ */
