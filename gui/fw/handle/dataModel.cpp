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
#include "pkeyevent.h"

extern packetHandling ph;
extern bool processedByUser;

void dataModel::Init()
{
	screens_ready = 0;
}

void dataModel::mainScreenCb(packetHandling * ph, nrf_commands_t,
		void * rawdata, uint8_t size, void *t)
{
	if (size != sizeof(dataModel_mainScreen_t))
	{
		ph->WriteData(DATA_ERROR, (uint32_t) 0, 1);
		return;
	}
	dataModel_mainScreen_t * data = (dataModel_mainScreen_t *) rawdata;

	gui::spin_day = data->dayOfWeek;
	gui::spin_hours = data->hours;
	gui::spin_minutes = data->minutes;
	//gui::main_teplotaDoma = data->homeTemperature;
	gui::main_teplotaVoda = data->waterTemperature * 5;
	gui::HeatingTemp = data->heatingTemperature * 5;
	((dataModel *) t)->connection_status = data->slaveConnectionStatus;
	gui::main_topi = data->heatingActive;

	//if not procesed by user
	if (!processedByUser)
	{
		((dataModel *) t)->screens_ready |= MODEL_READY_MAIN;
		piris::PKeyEvent evt;
		evt.event = piris::RELEASED;
		evt.key = kUP;

		gui::main_program = data->program;
		gui::ManualTemp = data->manualTemperature * 5;

		gui::cb_programSwitcher(&evt, &gui::main_program);
	}
}

void dataModel::sendHomeTemperature()
{
	ph.WriteData(HANDLE_HOME_TEMPERATURE, gui::main_teplotaDoma / 5, 2);
}

void dataModel::sendProgramManual()
{
	if (screens_ready & MODEL_READY_MAIN)
	{
		int16_t p[2];
		p[0] = gui::ManualTemp / 5;
		p[1] = gui::main_program;

		ph.WriteData(HANDLE_PROGRAM_MANUAL, p, 4);
	}
}

void dataModel::waterScreenCb(packetHandling * ph, nrf_commands_t,
		void * rawdata, uint8_t size, void * t)
{
	if (size != 16 && size != 2)
	{
		ph->WriteData(DATA_ERROR, 1, 1);
		return;
	}

	if (size == 2)
	{
		if (processedByUser)
			return;
		gui::voda_temperature = *((int16_t*) rawdata) * 5;
		((dataModel *) t)->screens_ready |= MODEL_READY_WATER_TEMP;
		return;
	}

	dataModel_waterScreenRow_t * data = (dataModel_waterScreenRow_t *) rawdata;

	if (!processedByUser)
	{
		((dataModel *) t)->screens_ready |= MODEL_READY_WATER;
		for (int i = 0; i < 2; i++)
		{
			*gui::water[2 * i].hours = data->hoursStart;
			*gui::water[2 * i].minutes = data->minutesStart;
			*gui::water[2 * i + 1].hours = data->hoursStop;
			*gui::water[2 * i + 1].minutes = data->minutesStop;
			data++;
		}
	}
}

void dataModel::heatingScreenCb(packetHandling * ph, nrf_commands_t,
		void * rawdata, uint8_t size, void *t)
{
	const gui::heating_row_t * row = NULL;
	dataModel_heatingScreenRow_t * data =
			(dataModel_heatingScreenRow_t*) rawdata;
	if (size == sizeof(dataModel_heatingScreenRow_t) * 3)
	{
		row = gui::heating_week;
		if (!processedByUser)
			((dataModel *) t)->screens_ready |= MODEL_READY_HEATING_WEEK_P2;
	}
	else if (size == sizeof(dataModel_heatingScreenRow_t))
	{
		row = &gui::heating_week[3];
		if (!processedByUser)
			((dataModel *) t)->screens_ready |= MODEL_READY_HEATING_WEEK;
	}
	else if (size == sizeof(dataModel_heatingScreenRow_t) * 2)
	{
		row = gui::heating_weekend;
		if (!processedByUser)
			((dataModel *) t)->screens_ready |= MODEL_READY_HEATING_WEEKEND;
	}
	else
	{
		ph->WriteData(DATA_ERROR, 2, 1);
		return;
	}

	if (!processedByUser)
	{
		for (uint8_t i = 0; i < size / sizeof(dataModel_heatingScreenRow_t);
				i++)
		{
			*(row->hours) = data[i].hours;
			*row->minutes = data[i].minutes;
			*row->temperature = data[i].temperature * 5;
			row++;
		}
	}
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
	data.homeTemperature = gui::main_teplotaDoma / 5;
	data.manualTemperature = gui::ManualTemp / 5;
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
	data[2].hoursStart = gui::voda_temperature / 5;
	if (screens_ready & MODEL_READY_WATER
			&& screens_ready & MODEL_READY_WATER_TEMP)
		ph.WriteData(HANDLE_WATER_SCREEN, &data, 18);
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

	dataModel_heatingScreenRow_t data[size];

	for (int i = 0; i < size; i++)
	{
		data[i].hours = row[i].hours->val();
		data[i].minutes = row[i].minutes->val();
		data[i].temperature = row[i].temperature->val() / 5;
	}

	ph.WriteData(HANDLE_HEATING_SCREEN, &data,
			size * sizeof(dataModel_heatingScreenRow_t));
}
