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
typedef dataModel_waterScreenRow_t dataModel_waterScreen_t[3];

#define MODEL_READY_MAIN 1
#define MODEL_READY_HEATING_WEEK 2
#define MODEL_READY_HEATING_WEEKEND 4
#define MODEL_READY_WATER 8
#define MODEL_READY_HEATING_WEEK_P2 16
#define MODEL_READY_WATER_TEMP 32
#define MODEL_READY_MASK (0x3f)

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
