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

#ifdef STM32F4xx_MCUCONF

#define CS_PORT GPIOA
#define CE_PORT GPIOA
#define CS_PIN	4
#define CE_PIN 	2

#define SPI_BR SPI_CR1_BR_0

#define TEST_LED_PORT 	GPIOD
#define TEST_LED_PIN	GPIOD_LED4
#define TEST_LED_PORT2	GPIOD
#define TEST_LED_PIN2	GPIOD_LED5

#define SPI_MOSI_PORT	GPIOA
#define SPI_MISO_PORT 	GPIOA
#define SPI_SCK_PORT	GPIOA
#define SPI_MOSI_PIN	5
#define SPI_MISO_PIN	6
#define SPI_SCK_PIN		7
#define SPI_SCK_MODE	PAL_MODE_ALTERNATE(5)
#define SPI_MISO_MODE	PAL_MODE_ALTERNATE(5)
#define SPI_MOSI_MODE	PAL_MODE_ALTERNATE(5)

#define UART_RX_PORT	GPIOD
#define UART_TX_PORT	GPIOC
#define UART_RX_PIN		2
#define UART_TX_PIN		12
#define UART_TX_MODE 		PAL_MODE_ALTERNATE(8)
#define UART_RX_MODE 		PAL_MODE_ALTERNATE(8)

#else

#define CS_PORT GPIOB
#define CE_PORT GPIOB
#define CS_PIN	6
#define CE_PIN 	8

#define SPI_BR (SPI_CR1_BR_0)
//#define SPI_BR 0

#define TEST_LED_PORT 	GPIOC
#define TEST_LED_PIN	13
#define TEST_LED_PORT2	GPIOC
#define TEST_LED_PIN2	14

#define SPI_MOSI_PORT	GPIOB
#define SPI_MISO_PORT 	GPIOB
#define SPI_SCK_PORT	GPIOB
#define SPI_MOSI_PIN	5
#define SPI_MISO_PIN	4
#define SPI_SCK_PIN		3
#define SPI_SCK_MODE	PAL_MODE_STM32_ALTERNATE_PUSHPULL
#define SPI_MISO_MODE	PAL_MODE_INPUT
#define SPI_MOSI_MODE	PAL_MODE_STM32_ALTERNATE_PUSHPULL

#define UART_RX_PORT	GPIOA
#define UART_TX_PORT	GPIOA
#define UART_RX_PIN		10
#define UART_TX_PIN		9
#define UART_RX_MODE	PAL_MODE_INPUT
#define UART_TX_MODE	PAL_MODE_STM32_ALTERNATE_PUSHPULL

#endif


#ifdef __cplusplus
}
#endif

#endif /* PLATFORM_H_ */
