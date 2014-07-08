/*
 * Temperature.h
 *
 *  Created on: 11.9.2012
 *      Author: kubanec
 */

#ifndef TEMPERATURE_H_
#define TEMPERATURE_H_

#define I2C_TEMP_ADDRESS 0b1001111
#include "scheduler.hpp"

class Temperature
{
private:
	int16_t temperature;
public:
	void Init(void);
	int16_t GetTemperature(void);
	void RefreshTemperature(void);

private:
	static void machine(arg_t arg);
	Scheduler s;
};

#endif /* TEMPERATURE_H_ */
