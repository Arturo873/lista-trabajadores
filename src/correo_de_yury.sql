-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 07-06-2025 a las 18:02:58
-- Versión del servidor: 8.3.0
-- Versión de PHP: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `correo_de_yury`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `area`
--

DROP TABLE IF EXISTS `area`;
CREATE TABLE IF NOT EXISTS `area` (
  `id_area` int NOT NULL AUTO_INCREMENT,
  `nombre_area` varchar(50) COLLATE latin1_spanish_ci DEFAULT NULL,
  `jefe_area` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id_area`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Volcado de datos para la tabla `area`
--

INSERT INTO `area` (`id_area`, `nombre_area`, `jefe_area`) VALUES
(1, 'Recursos Humanos', 'Claudia Martínez'),
(2, 'Producción', 'Juan Pérez');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cargafamiliar`
--

DROP TABLE IF EXISTS `cargafamiliar`;
CREATE TABLE IF NOT EXISTS `cargafamiliar` (
  `id_carga` int NOT NULL AUTO_INCREMENT,
  `id_empleado` int DEFAULT NULL,
  `nombre_carga` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `parentesco` varchar(50) COLLATE latin1_spanish_ci DEFAULT NULL,
  `genero_carga` enum('M','F','Otro') COLLATE latin1_spanish_ci DEFAULT NULL,
  `rut_carga` varchar(12) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id_carga`),
  KEY `id_empleado` (`id_empleado`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Volcado de datos para la tabla `cargafamiliar`
--

INSERT INTO `cargafamiliar` (`id_carga`, `id_empleado`, `nombre_carga`, `parentesco`, `genero_carga`, `rut_carga`) VALUES
(1, 1, 'Valentina Martínez', 'Hija', 'F', '23456789-0'),
(2, 2, 'Lucía Soto', 'Hija', 'F', '34567890-1'),
(3, 3, 'Tomás Ramírez', 'Hijo', 'M', '45678901-2');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cargo`
--

DROP TABLE IF EXISTS `cargo`;
CREATE TABLE IF NOT EXISTS `cargo` (
  `id_cargo` int NOT NULL AUTO_INCREMENT,
  `nombre_cargo` varchar(50) COLLATE latin1_spanish_ci DEFAULT NULL,
  `id_permiso` int DEFAULT NULL,
  `id_area` int DEFAULT NULL,
  PRIMARY KEY (`id_cargo`),
  KEY `id_permiso` (`id_permiso`),
  KEY `id_area` (`id_area`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Volcado de datos para la tabla `cargo`
--

INSERT INTO `cargo` (`id_cargo`, `nombre_cargo`, `id_permiso`, `id_area`) VALUES
(1, 'Jefe RRHH', 1, 1),
(2, 'RRHH', 2, 1),
(3, 'Trabajador', 3, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contactoemergencia`
--

DROP TABLE IF EXISTS `contactoemergencia`;
CREATE TABLE IF NOT EXISTS `contactoemergencia` (
  `id_contacto` int NOT NULL AUTO_INCREMENT,
  `id_empleado` int DEFAULT NULL,
  `nombre_contacto` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `relacion` varchar(50) COLLATE latin1_spanish_ci DEFAULT NULL,
  `telefono_contacto` varchar(15) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id_contacto`),
  KEY `id_empleado` (`id_empleado`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Volcado de datos para la tabla `contactoemergencia`
--

INSERT INTO `contactoemergencia` (`id_contacto`, `id_empleado`, `nombre_contacto`, `relacion`, `telefono_contacto`) VALUES
(1, 1, 'Luis Martínez', 'Hermano', '911223344'),
(2, 2, 'Ana Soto', 'Esposa', '922334455'),
(3, 3, 'María López', 'Madre', '933445566');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

DROP TABLE IF EXISTS `empleado`;
CREATE TABLE IF NOT EXISTS `empleado` (
  `id_empleado` int NOT NULL AUTO_INCREMENT,
  `rut` varchar(12) COLLATE latin1_spanish_ci DEFAULT NULL,
  `nombre` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `genero` enum('M','F','Otro') COLLATE latin1_spanish_ci DEFAULT NULL,
  `direccion` varchar(200) COLLATE latin1_spanish_ci DEFAULT NULL,
  `telefono` varchar(15) COLLATE latin1_spanish_ci DEFAULT NULL,
  `fecha_ingreso` date DEFAULT NULL,
  `id_cargo` int DEFAULT NULL,
  `usuario` varchar(50) COLLATE latin1_spanish_ci DEFAULT NULL,
  `contrasena` varchar(255) COLLATE latin1_spanish_ci DEFAULT NULL,
  `fecha_despido` date DEFAULT NULL,
  PRIMARY KEY (`id_empleado`),
  UNIQUE KEY `rut` (`rut`),
  UNIQUE KEY `usuario` (`usuario`),
  KEY `id_cargo` (`id_cargo`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`id_empleado`, `rut`, `nombre`, `genero`, `direccion`, `telefono`, `fecha_ingreso`, `id_cargo`, `usuario`, `contrasena`, `fecha_despido`) VALUES
(1, '12345678-9', 'Claudia Martínez', 'F', 'Calle 123, Ciudad', '912345678', '2022-01-10', 1, 'cmartinez', '123', NULL),
(2, '98765432-1', 'Carlos Soto', 'M', 'Av. Siempre Viva 742', '987654321', '2023-03-15', 2, 'csoto', '123', NULL),
(3, '11111111-1', 'Pedro Ramírez', 'M', 'Pasaje 45, Pueblo', '965432187', '2024-05-20', 3, 'pramirez', '12345', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permiso`
--

DROP TABLE IF EXISTS `permiso`;
CREATE TABLE IF NOT EXISTS `permiso` (
  `id_permiso` int NOT NULL AUTO_INCREMENT,
  `modulo` varchar(50) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id_permiso`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Volcado de datos para la tabla `permiso`
--

INSERT INTO `permiso` (`id_permiso`, `modulo`) VALUES
(1, 'Gestión de Personal'),
(2, 'Ver Información'),
(3, 'Acceso Limitado');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
