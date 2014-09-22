/**
 * @file PirisPort.cpp
 * @author kubanec
 * @date 28. 7. 2014
 *
 */
#include "PirisPort.h"
#include "st7735.hpp"
#include "pfont.h"
#include "pkeyevent.h"
#include "ptypes.h"
#include "PwmBacklight.h"
#include "dataModel.h"

bool processedByUser;
extern dataModel model;

extern "C" void __cxa_pure_virtual()
{
	chDbgPanic("pure virtual method called");
	while (1)
		;
}

void * operator new(size_t size)
{
	chDbgPanic("we don't want dynamic allocation");
	return NULL;
}

void PirisPort::timeout(arg_t data)
{
	static bool uz = false;
	PirisPort * o = (PirisPort*)data;
	if (uz)
		model.sendProgramManual();

	uz = true;
	processedByUser = false;
	PwmBacklight::FadeOut();
}

void PirisPort::start()
{
	St7735::Init();
	backlight.Setup(timeout,this,MS2ST(5000),ONCE);
	backlight.Register();
}


bool PirisPort::readKeyEvent(piris::PKeyEvent * evt)
{
	if (model.screensReady() != MODEL_READY_MASK)
		return false;

	uint16_t state;
	state = palReadPad(BUTTON_DOWN_PORT, BUTTON_DOWN_PIN) << 1;
	state |= palReadPad(BUTTON_UP_PORT, BUTTON_UP_PIN) ;
	state |= palReadPad(BUTTON_ENTER_PORT, BUTTON_ENTER_PIN) << 2;

	if (state != last_state)
	{
		evt->key = last_state ^ state;
		if (last_state & evt->key)
			evt->event = piris::RELEASED;
		else if (state & evt->key)
			evt->event = piris::PRESSED;

		last_state = state;
		PwmBacklight::FadeIn();
		backlight.Rearm();
		backlight.Register();

		processedByUser = true;


		return true;

	}

	return false;
}
bool PirisPort::readTouchEvent(piris::PTouchEvent *)
{
	return false;
}

#define swap(x) (x == 1) ? 0 : ((((x << 11) & 0xf100) | ((x >> 11) &0x1f) | (x & 0x7E0)))
//#define swap(x) x

void PirisPort::putPixel(piris::pixel_t x, piris::pixel_t y,
		piris::PColor color)
{
	St7735::DrawPixel(x, y, swap(color.rawData()));
}
void PirisPort::putText(const char * text, piris::pixel_t x, piris::pixel_t y,
		const piris::PFont & font, piris::PColor color)
{
	St7735::PutString(text, x, y - font.height(), swap(color.rawData()),
			font.height());
}
void PirisPort::putRectangle(piris::pixel_t x1, piris::pixel_t x2,
		piris::pixel_t y1, piris::pixel_t y2, piris::PColor color, bool filled)
{
	St7735::DrawRectangle(x1, y1, x2, y2, swap(color.rawData()));
}
void PirisPort::fill(piris::PColor color)
{
	St7735::FillRGB(swap(color.rawData()));
}
void PirisPort::putLine(piris::pixel_t x1, piris::pixel_t x2, piris::pixel_t y1,
		piris::pixel_t y2, piris::PColor color)
{
	St7735::DrawLine(x1, x2, y1, y2, swap(color.rawData()));
}

//virtual void putRectangleShaped(piris::pixel_t x1, piris::pixel_t x2, piris::pixel_t y1,
//		piris::pixel_t y2, piris::PColor color, bool filled = false);
//virtual void putArc()

piris::pixel_t PirisPort::width() const
{
	return St7735::GetWidth();
}
piris::pixel_t PirisPort::height() const
{
	return St7735::GetHeight();
}
