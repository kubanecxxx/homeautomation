/**
 * @file PirisPort.h
 * @author kubanec
 * @date 28. 7. 2014
 *
 */
#ifndef PIRISPORT_H_
#define PIRISPORT_H_

#include "pportingabstract.h"
#include "scheduler.hpp"

class PirisPort: public piris::PPortingAbstract
{
public:
	void start();

	virtual bool readKeyEvent(piris::PKeyEvent * evt);
	virtual bool readTouchEvent(piris::PTouchEvent * evt);

	virtual void putPixel(piris::pixel_t x, piris::pixel_t y,
			piris::PColor color);
	virtual void putText(const char * text, piris::pixel_t x, piris::pixel_t y,
			const piris::PFont & font, piris::PColor color);
	virtual void putRectangle(piris::pixel_t x1, piris::pixel_t x2,
			piris::pixel_t y1, piris::pixel_t y2, piris::PColor color,
			bool filled = false);
	virtual void fill(piris::PColor color);
	virtual void putLine(piris::pixel_t x1, piris::pixel_t x2,
			piris::pixel_t y1, piris::pixel_t y2, piris::PColor color);

	//virtual void putRectangleShaped(piris::pixel_t x1, piris::pixel_t x2, piris::pixel_t y1,
	//		piris::pixel_t y2, piris::PColor color, bool filled = false);
	//virtual void putArc()

	virtual piris::pixel_t width() const;
	virtual piris::pixel_t height() const;

private:
	uint16_t last_state;
	Scheduler backlight;
	static void timeout(arg_t data);

};

#endif /* PIRISPORT_H_ */

