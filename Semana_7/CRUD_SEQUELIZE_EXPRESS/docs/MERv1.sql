-- MySQL Script generated by MySQL Workbench
-- Mon Mar  8 21:04:46 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`t_usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`t_usuario` (
  `usu_id` INT NOT NULL,
  `usu_email` VARCHAR(45) NULL,
  `usu_tipo` VARCHAR(45) NULL,
  `usu_password` VARCHAR(45) NULL,
  PRIMARY KEY (`usu_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`t_cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`t_cliente` (
  `cli_dni` VARCHAR(9) NOT NULL,
  `cli_nombre` VARCHAR(45) NULL,
  `cli_direccion` VARCHAR(45) NULL,
  `cli_fono` VARCHAR(10) NULL,
  PRIMARY KEY (`cli_dni`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`t_cab_nota`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`t_cab_nota` (
  `cab_id` INT NOT NULL,
  `cab_serie` VARCHAR(4) NULL,
  `cab_fecha` DATE NULL,
  `cab_total` FLOAT(5,2) NULL,
  `cab_dscto` FLOAT(5,2) NULL,
  `cab_subtotal` FLOAT(5,2) NULL,
  `cli_dni` INT NOT NULL,
  `usu_id` VARCHAR(9) NOT NULL,
  UNIQUE INDEX `cab_id_UNIQUE` (`cab_id` ASC) VISIBLE,
  INDEX `fk_t_cab_nota_t_usuario1_idx` (`cli_dni` ASC) VISIBLE,
  INDEX `fk_t_cab_nota_t_cliente1_idx` (`usu_id` ASC) VISIBLE,
  PRIMARY KEY (`cab_id`),
  CONSTRAINT `fk_t_cab_nota_t_usuario1`
    FOREIGN KEY (`cli_dni`)
    REFERENCES `mydb`.`t_usuario` (`usu_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_cab_nota_t_cliente1`
    FOREIGN KEY (`usu_id`)
    REFERENCES `mydb`.`t_cliente` (`cli_dni`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`t_categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`t_categoria` (
  `cat_id` INT NOT NULL,
  `cat_nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`cat_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`t_producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`t_producto` (
  `prod_id` INT NOT NULL,
  `prod_nombre` VARCHAR(45) NULL,
  `prod_precio` FLOAT(5,2) NULL,
  `prod_cantidad` INT NULL,
  `prod_fecvec` DATE NULL,
  `prod_estado` TINYINT NULL,
  `cat_id` INT NOT NULL,
  PRIMARY KEY (`prod_id`),
  INDEX `fk_t_producto_t_categoria1_idx` (`cat_id` ASC) VISIBLE,
  CONSTRAINT `fk_t_producto_t_categoria1`
    FOREIGN KEY (`cat_id`)
    REFERENCES `mydb`.`t_categoria` (`cat_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`t_det_nota`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`t_det_nota` (
  `det_id` INT NOT NULL,
  `det_cantidad` VARCHAR(45) NULL,
  `det_subtotal` FLOAT(5,2) NULL,
  `prod_id` INT NOT NULL,
  `cab_id` INT NOT NULL,
  PRIMARY KEY (`det_id`),
  UNIQUE INDEX `det_id_UNIQUE` (`det_id` ASC) VISIBLE,
  INDEX `fk_t_det_nota_t_producto1_idx` (`prod_id` ASC) VISIBLE,
  INDEX `fk_t_det_nota_t_cab_nota1_idx` (`cab_id` ASC) VISIBLE,
  CONSTRAINT `fk_t_det_nota_t_producto1`
    FOREIGN KEY (`prod_id`)
    REFERENCES `mydb`.`t_producto` (`prod_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_t_det_nota_t_cab_nota1`
    FOREIGN KEY (`cab_id`)
    REFERENCES `mydb`.`t_cab_nota` (`cab_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`t_promocion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`t_promocion` (
  `prom_id` INT NOT NULL,
  `prom_fecdesde` DATE NULL,
  `prom_fechasta` DATE NULL,
  `prom_descuento` FLOAT(5,2) NULL,
  `prom_estado` TINYINT NOT NULL,
  `t_producto_prod_id` INT NOT NULL,
  PRIMARY KEY (`prom_id`),
  INDEX `fk_t_promocion_t_producto_idx` (`t_producto_prod_id` ASC) VISIBLE,
  CONSTRAINT `fk_t_promocion_t_producto`
    FOREIGN KEY (`t_producto_prod_id`)
    REFERENCES `mydb`.`t_producto` (`prod_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
