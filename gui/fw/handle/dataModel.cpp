/**
 * @file dataModel.cpp
 * @author kubanec
 * @date 4. 8. 2014
 *
 */

#include "ch.h"
#include "hal.h"
#include <dataModel.h>
#include "packetHandling.h"
#include "guiinit.h"

extern packetHandling ph;
extern int16_t connection_status;

void dataModel::Init()
{
}

void dataModel::mainScreenCb(packetHandling * ph, nrf_commands_t cmd,
		void * rawdata, uint8_t size, void *diese)
{
	if (size != sizeof(dataModel_mainScreen_t))
	{
		ph->WriteData(DATA_ERROR,0);
		return;
	}
	dataModel_mainScreen_t * data = (dataModel_mainScreen_t *) rawdata;

	gui::spin_day = data->dayOfWeek;
	gui::spin_hours = data->hours;
	gui::spin_minutes = data->minutes;
	gui::main_program = data->program;
	gui::main_teplotaDoma = data->homeTemperature;
	gui::main_teplotaVoda = data->waterTemperature;
	gui::ManualTemp = data->manualTemperature;
	gui::HeatingTemp = data->heatingTemperature;
	connection_status = data->slaveConnectionStatus;
	gui::main_topi = data->heatingActive;
}

void dataModel::waterScreenCb(packetHandling * ph, nrf_commands_t cmd,
		void * data, uint8_t size, void *diese)
{
	if (size != sizeof(dataModel_waterScreen_t))
	{
		ph->WriteData(DATA_ERROR,1);
		return;
	}
}

void dataModel::heatingScreenCb(packetHandling * ph, nrf_commands_t cmd,
		void * data, uint8_t size, void *diese)
{

}

void dataModel::sendMainScreen()
{
	dataModel_mainScreen_t data;

	data.dayOfWeek = gui::spin_day;
	data.hours = gui::spin_hours;
	data.minutes = gui::spin_minutes;
	data.heatingActive = gui::main_topi;
	data.program = gui::main_program;
	data.waterTemperature = gui::main_teplotaVoda;
	data.homeTemperature = gui::main_teplotaDoma;
	data.manualTemperature = gui::ManualTemp;
	data.heatingTemperature = 0;
	data.slaveConnectionStatus = 0;

	ph.WriteData(HANDLE_MAIN_SCREEN, &data, sizeof(data));
}

void dataModel::sendWaterScreen()
{
	dataModel_waterScreen_t data;

	for (int i = 0; i < 2; i++)
	{
		data[i].hoursStart = *gui::water[2 * i].hours;
		data[i].minutesStart = *gui::water[2 * i].minutes;
		data[i].hoursStop = *gui::water[2 * i + 1].hours;
		data[i].minutesStop = *gui::water[2 * i + 1].minutes;
	}

	ph.WriteData(HANDLE_WATER_SCREEN, &data, sizeof(data) * 2);
}

void dataModel::sendHeatingScreen(bool isWeekend)
{
	const gui::heating_row_t * row = gui::heating_week;
	int size = 4;
	if (isWeekend)
	{
		size = 2;
		row = gui::heating_weekend;
	}

	dataModel_heatingScreenRow_t data[size + 1];
	data[size].hours = isWeekend;

	for (int i = 0; i < size; i++)
	{
		data[i].hours = row[i].hours->val();
		data[i].minutes = row[i].minutes->val();
		data[i].temperature = row[i].temperature->val();
	}

	ph.WriteData(HANDLE_HEATING_SCREEN, &data,
			6 * sizeof(dataModel_heatingScreenRow_t) + 2);
}
