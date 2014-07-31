/**
 * @file platform.h
 * @author kubanec
 * @date 8. 4. 2014
 *
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef PLATFORM_H_
#define PLATFORM_H_

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
/* Exported types ------------------------------------------------------------*/
/* Exported constants --------------------------------------------------------*/
/* Exported macro ------------------------------------------------------------*/
/* Exported functions --------------------------------------------------------*/



#define SPI_BR ( SPI_CR1_BR_1)
//#define SPI_BR 0

//leds
//#define TEST_LED_PORT 	GPIOB
//#define TEST_LED_PIN	6

//radio spi spi2
#define SPI_MOSI_PORT	GPIOB
#define SPI_MISO_PORT 	GPIOB
#define SPI_SCK_PORT	GPIOB
#define SPI_MOSI_PIN	15
#define SPI_MISO_PIN	14
#define SPI_SCK_PIN		13
#define SPI_SCK_MODE	PAL_MODE_STM32_ALTERNATE_PUSHPULL
#define SPI_MISO_MODE	PAL_MODE_INPUT
#define SPI_MOSI_MODE	PAL_MODE_STM32_ALTERNATE_PUSHPULL
// +nrf pins
#define NRF_CS_PORT GPIOB
#define NRF_CE_PORT GPIOA
#define NRF_CS_PIN	12
#define NRF_CE_PIN 	3

//i2c temperature pins
#define I2C_SDA_PORT GPIOB
#define I2C_SCL_PORT GPIOB
#define I2C_SDA_PIN 11
#define I2C_SCL_PIN 10
//slave address
#define I2C_TEMP_ADDRESS 0b1001000

//input buttons
//AFIO->MAPR |= 0b010 << 24;
#define BUTTON_UP_PORT GPIOB
#define BUTTON_DOWN_PORT GPIOB
#define BUTTON_ENTER_PORT GPIOB
#define BUTTON_UP_PIN 5
#define BUTTON_DOWN_PIN 3
#define BUTTON_ENTER_PIN 4


//backlight pins
#define BACKLIGHT_PORT GPIOB
#define BACKLIGHT_PIN  6

//display pins

#ifdef __cplusplus
}
#endif

#endif /* PLATFORM_H_ */
