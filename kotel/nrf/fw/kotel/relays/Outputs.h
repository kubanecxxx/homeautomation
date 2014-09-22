/**
 * @file Outputs.h
 * @author kubanec
 * @date 4. 5. 2014
 *
 */
#ifndef OUTPUTS_H_
#define OUTPUTS_H_

#include "ch.h"
#include "hal.h"
#include "scheduler.hpp"

class Outputs
{
public:
	typedef struct
	{
		GPIO_TypeDef * kotel_port;
		uint8_t kotel_pin;
		GPIO_TypeDef* cerpadlo_port;
		uint8_t cerpadlo_pin;
	} config_t;

	Outputs(const config_t * cnf);
	void topit(bool enable);
	inline void setCerpadloTimeout(uint16_t s)
	{
		cerpadlo.SetPeriod(S2ST(s));
	}
	inline bool getCerpadlo() const
	{
		return ((palReadLatch(c->cerpadlo_port) >> c->cerpadlo_pin) & 1);
	}
	inline bool getTopitLatch() const
	{
		return ((palReadLatch(c->kotel_port) >> c->kotel_pin) & 1);
	}
	void start();

private:
	const config_t *c;
	Scheduler timeout;
	Scheduler cerpadlo;

	static void kotel_timeout(arg_t arg);
	static void cerpadlo_timeout(arg_t arg);
};

#endif /* OUTPUTS_H_ */
