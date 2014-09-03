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

//nrf pins
#define CS_PORT GPIOB
#define CE_PORT GPIOA
#define CS_PIN	6
#define CE_PIN 	15

#define SPI_BR ( SPI_CR1_BR_1)
//#define SPI_BR 0

//leds
#define TEST_LED_PORT 	GPIOC
#define TEST_LED_PIN	13
#define TEST_LED_PORT2	GPIOC
#define TEST_LED_PIN2	14
#define TEST_LED_PORT3	GPIOC
#define TEST_LED_PIN3	15

//radio spi
#define SPI_MOSI_PORT	GPIOB
#define SPI_MISO_PORT 	GPIOB
#define SPI_SCK_PORT	GPIOB
#define SPI_MOSI_PIN	5
#define SPI_MISO_PIN	4
#define SPI_SCK_PIN		3
#define SPI_SCK_MODE	PAL_MODE_STM32_ALTERNATE_PUSHPULL
#define SPI_MISO_MODE	PAL_MODE_INPUT
#define SPI_MOSI_MODE	PAL_MODE_STM32_ALTERNATE_PUSHPULL

//i2c temperature pins
#define I2C_SDA_PORT GPIOB
#define I2C_SCL_PORT GPIOB
#define I2C_SDA_PIN 9
#define I2C_SCL_PIN 8
#define I2C_SDA_PIN2 10
#define I2C_SCL_PIN2 11
//address of temperature sensor
#define I2C_TEMP_ADDRESS 0b1001111

//gpio pins relays
#define GPIO_HEATING_RELAY_PORT	GPIOA
#define GPIO_HEATING_RELAY_PIN 10
#define GPIO_PUMP_PORT	GPIOA
#define GPIO_PUMP_PIN	11
#define GPIO_FIRE_PORT	GPIOA
#define GPIO_FIRE_PIN	9



#define KOTEL_RELAYS_MODULE

#ifdef __cplusplus
}
#endif

#endif /* PLATFORM_H_ */
