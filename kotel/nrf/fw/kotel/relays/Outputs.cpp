/**
 * @file Outputs.cpp
 * @author kubanec
 * @date 4. 5. 2014
 *
 */
#include "Outputs.h"
#include "ch.h"

Outputs::Outputs(const config_t * config) :
		c(config)
{

}

void Outputs::start()
{
	chDbgAssert(c,"config struct is NULL","");
	timeout.Setup(kotel_timeout, this, S2ST(60), ONCE);
	cerpadlo.Setup(cerpadlo_timeout, this, S2ST(300), ONCE);

	palSetPadMode(c->cerpadlo_port, c->cerpadlo_pin, PAL_MODE_OUTPUT_PUSHPULL);
	palSetPadMode(c->kotel_port, c->kotel_pin, PAL_MODE_OUTPUT_PUSHPULL);
	palClearPad(c->cerpadlo_port,c->cerpadlo_pin);
	palClearPad(c->kotel_port,c->kotel_pin);
}

void Outputs::topit(bool enable)
{
	if (enable)
	{
		palSetPad(c->kotel_port, c->kotel_pin);
		palSetPad(c->cerpadlo_port, c->cerpadlo_pin);

		timeout.Register();
		cerpadlo.Unregister();
	}
	else
	{
		timeout.Unregister();
		cerpadlo.Register();

		palClearPad(c->kotel_port, c->kotel_pin);
	}
}

void Outputs::kotel_timeout(arg_t arg)
{
	Outputs * o = (Outputs*) arg;
	o->cerpadlo.Register();

	palClearPad(o->c->kotel_port, o->c->kotel_pin);
}

void Outputs::cerpadlo_timeout(arg_t arg)
{
	Outputs * o = (Outputs*) arg;

	palClearPad(o->c->cerpadlo_port, o->c->cerpadlo_pin);
}
