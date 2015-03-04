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
	int8_t hours;
	int8_t minutes;
	int8_t dayOfWeek;
	int8_t program;
	int8_t heatingTemperature;
	int8_t manualTemperature;
	int8_t homeTemperature;
	int8_t waterTemperature;
	int8_t slaveConnectionStatus;
	int8_t heatingActive;
} dataModel_mainScreen_t ;

typedef struct __attribute__((__packed__))
{
	int8_t hours;
	int8_t minutes;
	int8_t temperature;
} dataModel_heatingScreenRow_t ;

typedef struct __attribute__((__packed__))
{
	int8_t hoursStart;
	int8_t minutesStart;
	int8_t hoursStop;
	int8_t minutesStop;
} dataModel_waterScreenRow_t ;

typedef struct __attribute__ ((__packed__))
{
	dataModel_waterScreenRow_t time[2];
	int8_t temperature;
}
dataModel_waterScreen_t;

#define MODEL_READY_MAIN 1
#define MODEL_READY_HEATING_WEEK 2
#define MODEL_READY_HEATING_WEEKEND 4
#define MODEL_READY_WATER 8
#define MODEL_READY_MASK (0x0f)

class packetHandling;
class dataModel
{
public:
	void Init();
	void sendMainScreen();
	void sendWaterScreen();
	void sendHeatingScreen(bool isWeekend);
	void sendHomeTemperature();
	void sendProgramManual();
	static void mainScreenCb(packetHandling * ph, nrf_commands_t cmd,
			void * data, uint8_t size, void *userData);
	static void heatingScreenCb(packetHandling * ph, nrf_commands_t cmd,
			void * data, uint8_t size, void *userData);
	static void waterScreenCb(packetHandling * ph, nrf_commands_t cmd,
			void * data, uint8_t size, void *userData);
	inline uint8_t screensReady() const {return screens_ready;}
	inline int16_t slaveConnectionStatus() const {return connection_status;}
	inline void setScreenDirty(uint8_t mask) {screens_ready &= (~mask);}
private:
	uint8_t screens_ready;
	int16_t connection_status;
};

#endif /* DATAMODEL_H_ */
